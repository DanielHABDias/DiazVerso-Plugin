"""J02: dry-run and simulated FFmpeg tests, without real video."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("diazverso_frames",ROOT/"scripts"/"extract_review_frames.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def props():
    return json.loads((ROOT/"examples"/"short-remotion-props.example.json").read_text("utf-8"))


class FrameExtractorTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name)
        self.video=self.root/"render.mp4"
        self.out=self.root/"frames"

    def plan(self,events=None):
        return mod.plan(props(),self.video,self.out,events)

    def test_first_middle_last_for_each_scene(self):
        r=self.plan()
        self.assertEqual([x["frame"] for x in r["steps"]],[0,44,89,90,134,179])
        self.assertFalse(r["frames_extracted"])
        self.assertFalse(self.out.exists())

    def test_transition_event_deduplicates_frame(self):
        r=self.plan([{"kind":"transition","frame":90}])
        self.assertEqual(len(r["steps"]),6)
        self.assertIn("transition",r["steps"][3]["reasons"])

    def test_pose_event_adds_frame(self):
        r=self.plan([{"kind":"pose","frame":55}])
        self.assertEqual(len(r["steps"]),7)

    def test_out_of_bounds_events_rejected(self):
        with self.assertRaises(ValueError):
            self.plan([{"kind":"pose","frame":180}])

    def test_unknown_event_type_rejected(self):
        with self.assertRaises(ValueError):
            self.plan([{"kind":"random","frame":10}])

    def test_missing_real_mp4_is_blocker(self):
        with self.assertRaises(FileNotFoundError):
            mod.extract(self.plan())

    def test_invalid_contract_rejected(self):
        d=props();d["duration_frames"]=1
        with self.assertRaises(ValueError):
            mod.plan(d,self.video,self.out)

    def test_ffprobe_frame_rate_mismatch_blocks(self):
        self.video.write_bytes(b"mock")
        probe=json.dumps({"streams":[{"width":1080,"height":1920,"avg_frame_rate":"24/1","nb_frames":"180"}]})
        with patch.object(mod.shutil,"which",return_value="/bin/ffmpeg"), patch.object(
                mod.subprocess,"run",return_value=SimpleNamespace(returncode=0,stdout=probe,stderr="")):
            with self.assertRaises(RuntimeError):
                mod.extract(self.plan())
        self.assertFalse(self.out.exists())

    def test_mock_ffmpeg_extracts_valid_png(self):
        self.video.write_bytes(b"mock")
        probe=json.dumps({"streams":[{"width":1080,"height":1920,"avg_frame_rate":"30/1","nb_frames":"180"}]})
        signature=b"\x89PNG\r\n\x1a\n"+"synthetic".encode()
        def runner(cmd,**kw):
            if cmd[0]=="ffprobe":
                return SimpleNamespace(returncode=0,stdout=probe,stderr="")
            Path(cmd[-1]).write_bytes(signature)
            return SimpleNamespace(returncode=0,stdout="",stderr="")
        with patch.object(mod.shutil,"which",return_value="/bin/ffmpeg"), patch.object(
                mod.subprocess,"run",side_effect=runner) as call:
            result=mod.extract(self.plan())
        self.assertEqual(len(result["frames"]),6)
        self.assertTrue(result["frames_extracted"])
        self.assertFalse(result["visual_review_performed"])
        self.assertEqual(call.call_count,7)

    def test_does_not_overwrite_existing_image(self):
        self.video.write_bytes(b"mock")
        first=self.out/"frame_000000.png"
        first.parent.mkdir()
        first.write_bytes(b"previous")
        probe=json.dumps({"streams":[{"width":1080,"height":1920,"avg_frame_rate":"30/1","nb_frames":"180"}]})
        with patch.object(mod.shutil,"which",return_value="/bin/ffmpeg"), patch.object(
                mod.subprocess,"run",return_value=SimpleNamespace(returncode=0,stdout=probe,stderr="")):
            with self.assertRaises(FileExistsError):
                mod.extract(self.plan())
        self.assertEqual(first.read_bytes(),b"previous")


if __name__=="__main__":
    unittest.main()
