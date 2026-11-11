"""J01 tests: isolated filesystem and mocked external probes, no actual video."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("technical_review", ROOT/"scripts"/"review_technical.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def sample():
    return json.loads((ROOT/"examples"/"short-remotion-props.example.json").read_text("utf-8"))


class TechnicalReviewTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.src = self.root/"src"/"index.tsx"
        self.src.parent.mkdir()
        self.src.write_text("export const Demo = () => null;\n", encoding="utf-8")
        for asset in sample()["assets"]:
            path = self.root / asset["path"]
            path.parent.mkdir(parents=True,exist_ok=True)
            path.write_bytes(b"synthetic-test-fixture")

    def check(self, **kwargs):
        return mod.review(sample(), project_root=self.root, tsx_files=[self.src], **kwargs)

    def test_contract_assets_source_only(self):
        r=self.check()
        self.assertEqual(r["status"],"CONTRACT_ASSETS_CHECKED")
        self.assertEqual(r["assets_checked"],2)
        self.assertEqual(r["sources_checked"],1)
        self.assertFalse(r["typescript_compiled"])
        self.assertFalse(r["render_inspected"])
        self.assertFalse(r["human_qa_complete"])
        self.assertFalse(r["publishing_performed"])

    def test_missing_asset_is_blocker(self):
        (self.root/"assets"/"local"/"voice-example.wav").unlink()
        r=self.check()
        self.assertEqual(r["status"],"BLOCKED")
        self.assertIn("ASSET_MISSING",[x["code"] for x in r["findings"]])

    def test_invalid_timeline_contract_is_blocker(self):
        d=sample();d["duration_frames"]=999
        r=mod.review(d,project_root=self.root,tsx_files=[self.src])
        self.assertIn("INVALID_H01_CONTRACT",[x["code"] for x in r["findings"]])

    def test_suspicious_dynamic_code_blocks(self):
        self.src.write_text("export const X = eval('1+1');\n",encoding="utf-8")
        self.assertIn("DYNAMIC_CODE_EXECUTION",[x["code"] for x in self.check()["findings"]])

    def test_source_outside_root_blocks(self):
        p=self.root.parent/"not-a-project-source.tsx"
        r=mod.review(sample(),project_root=self.root,tsx_files=[p])
        self.assertIn("SOURCE_OUTSIDE_PROJECT",[x["code"] for x in r["findings"]])

    def test_render_missing_is_blocker(self):
        r=self.check(render_file=self.root/"not-there.mp4")
        self.assertIn("RENDER_FILE_INVALID",[x["code"] for x in r["findings"]])

    def test_tsc_without_project_is_blocker(self):
        r=self.check(run_tsc=True)
        self.assertIn("TSCONFIG_MISSING",[x["code"] for x in r["findings"]])

    def test_tsc_receipt_does_not_claim_render(self):
        (self.root/"tsconfig.json").write_text("{}",encoding="utf-8")
        with patch.object(mod.shutil,"which",return_value="/bin/npx"), patch.object(
                mod.subprocess,"run",return_value=SimpleNamespace(returncode=0,stdout="",stderr="")) as call:
            result=self.check(run_tsc=True)
        self.assertTrue(result["typescript_compiled"])
        self.assertFalse(result["render_inspected"])
        self.assertEqual(call.call_args.kwargs["cwd"],self.root.resolve())
        self.assertEqual(call.call_args.args[0][0:3],["npx","--no-install","tsc"])

    def test_ffprobe_metadata_is_checked_not_visual_qa(self):
        target=self.root/"output.mp4"
        target.write_bytes(b"0"*300)
        probe={"streams":[{"codec_name":"h264","width":1080,"height":1920}],
               "format":{"duration":"6.0"}}
        with patch.object(mod.shutil,"which",return_value="/usr/bin/ffprobe"), patch.object(
                mod.subprocess,"run",return_value=SimpleNamespace(returncode=0,stdout=json.dumps(probe),stderr="")):
            result=self.check(render_file=target)
        self.assertTrue(result["render_inspected"])
        self.assertFalse(result["human_qa_complete"])

    def test_ffprobe_wrong_resolution_blocks(self):
        target=self.root/"output.mp4"
        target.write_bytes(b"0"*300)
        probe={"streams":[{"codec_name":"h264","width":720,"height":1280}],
               "format":{"duration":"6.0"}}
        with patch.object(mod.shutil,"which",return_value="/usr/bin/ffprobe"), patch.object(
                mod.subprocess,"run",return_value=SimpleNamespace(returncode=0,stdout=json.dumps(probe),stderr="")):
            result=self.check(render_file=target)
        self.assertIn("RENDER_METADATA_MISMATCH",[x["code"] for x in result["findings"]])


if __name__=="__main__":
    unittest.main()
