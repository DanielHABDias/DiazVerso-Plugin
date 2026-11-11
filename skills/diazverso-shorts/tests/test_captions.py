import importlib.util
import unittest
from pathlib import Path

PATH = Path(__file__).resolve().parents[1] / "scripts" / "captions.py"
spec = importlib.util.spec_from_file_location("diazverso_captions", PATH)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def words():
    return [{"start_ms":0,"end_ms":300,"text":"Esse"},
            {"start_ms":320,"end_ms":650,"text":"herói"},
            {"start_ms":660,"end_ms":900,"text":"mudou."},
            {"start_ms":1200,"end_ms":1450,"text":"Por"},
            {"start_ms":1460,"end_ms":1800,"text":"quê?"}]


class CaptionTests(unittest.TestCase):
    def test_srt_and_frame_cues(self):
        result=mod.build_captions(words())
        self.assertEqual(len(result["cues"]),2)
        self.assertEqual(result["cues"][0]["text"],"Esse herói mudou.")
        self.assertIn("00:00:00,000 --> 00:00:00,900",result["srt"])
        self.assertEqual(result["cues"][0]["duration_frames"],27)
        self.assertFalse(result["audio_sync_verified"])

    def test_typographic_scene_without_spoken_words(self):
        x=mod.build_captions(words(),visual_text_only=[{"start_ms":2000,"end_ms":3000}])
        self.assertEqual(len(x["cues"]),2)

    def test_spoken_text_cannot_be_suppressed_as_visual_only(self):
        with self.assertRaises(ValueError):
            mod.build_captions(words(),visual_text_only=[{"start_ms":200,"end_ms":500}])

    def test_overlapping_words_rejected(self):
        a=words();a[1]["start_ms"]=200
        with self.assertRaises(ValueError):mod.build_captions(a)

    def test_unsorted_words_rejected(self):
        with self.assertRaises(ValueError):mod.build_captions(list(reversed(words())))

    def test_invalid_ms_rejected(self):
        a=words();a[0]["start_ms"]=-1
        with self.assertRaises(ValueError):mod.build_captions(a)

    def test_bad_text_rejected(self):
        a=words();a[0]["text"]="\n"
        with self.assertRaises(ValueError):mod.build_captions(a)

    def test_missing_timestamps_rejected(self):
        with self.assertRaises(ValueError):mod.build_captions([{"text":"falei"}])

    def test_invalid_fps_rejected(self):
        with self.assertRaises(ValueError):mod.build_captions(words(),fps=0)

    def test_long_sentence_splits(self):
        w=[{"start_ms":i*250,"end_ms":i*250+180,"text":"palavra"} for i in range(12)]
        self.assertEqual(len(mod.build_captions(w,max_words=6)["cues"]),2)


if __name__ == "__main__":
    unittest.main()
