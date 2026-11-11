import importlib.util
import unittest
from pathlib import Path

FILE=Path(__file__).resolve().parents[1]/"scripts"/"review_short.py"
spec=importlib.util.spec_from_file_location("diazverso_review_short",FILE)
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def sample():
    return {"hook_seconds":1.0,"duration_seconds":65.0,"has_payoff":True,
            "has_cta":True,"captions":"VERIFIED_SYNC","has_speech":True,
            "audio_checked":True,"links_checked":True,"safe_area_checked":True,
            "render_checked":True,"rights_checked":True}


class ReviewShortTests(unittest.TestCase):
    def test_ready_still_requires_creator(self):
        x=mod.review(sample())
        self.assertEqual(x["status"],"READY_FOR_CREATOR_APPROVAL")
        self.assertTrue(x["requires_creator_approval"])
        self.assertFalse(x["publishing_performed"])

    def test_missing_render_blocks(self):
        d=sample();d["render_checked"]=False
        self.assertEqual(mod.review(d)["status"],"REVIEW_REQUIRED")

    def test_captions_not_verified_blocks(self):
        d=sample();d["captions"]="NOT_VERIFIED"
        self.assertGreater(mod.review(d)["blocker_count"],0)

    def test_text_only_scene_requires_no_speech(self):
        d=sample();d["captions"]="TEXT_ONLY_WITHOUT_SPEECH"
        with self.assertRaises(ValueError):mod.review(d)
        d["has_speech"]=False
        self.assertEqual(mod.review(d)["status"],"READY_FOR_CREATOR_APPROVAL")

    def test_short_duration_editorial_not_platform_limit(self):
        d=sample();d["duration_seconds"]=43
        x=mod.review(d)
        self.assertEqual(x["status"],"EDITORIAL_REVIEW")
        self.assertTrue(any(z["field"]=="duration_seconds" for z in x["issues"]))

    def test_late_hook_editorial(self):
        d=sample();d["hook_seconds"]=4
        self.assertEqual(mod.review(d)["status"],"EDITORIAL_REVIEW")

    def test_missing_payoff_blocks(self):
        d=sample();d["has_payoff"]=False
        self.assertGreater(mod.review(d)["blocker_count"],0)

    def test_unknown_caption_mode_rejected(self):
        d=sample();d["captions"]="MADE_UP"
        with self.assertRaises(ValueError):mod.review(d)

    def test_no_real_render_claim(self):
        self.assertFalse(mod.review(sample())["render_performed"])


if __name__ == "__main__":
    unittest.main()
