import importlib.util
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "scripts" / "review_pacing.py"
spec = importlib.util.spec_from_file_location("diazverso_pacing", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def sample():
    return {"format": "SHORT", "fps": 30, "total_frames": 1860,
            "scenes": [
                {"id": "S01", "start_frame": 0, "duration_frames": 150,
                 "role": "HOOK", "narration": "O que mudou?", "visual_change": True},
                {"id": "S02", "start_frame": 150, "duration_frames": 1200,
                 "role": "EVIDENCE", "narration": "A história da mudança.", "visual_change": True},
                {"id": "S03", "start_frame": 1350, "duration_frames": 360,
                 "role": "PAYOFF", "narration": "Essa é a resposta.", "visual_change": True},
                {"id": "S04", "start_frame": 1710, "duration_frames": 150,
                 "role": "CTA", "narration": "Veja outras análises.", "visual_change": True},
            ]}


class PacingTests(unittest.TestCase):
    def test_good_plan_no_rule_based_findings(self):
        r = mod.review(sample())
        self.assertEqual(r["status"], "NO_RULE_BASED_FINDINGS")
        self.assertEqual(r["total_seconds"], 62.0)
        self.assertIsNone(r["retention_prediction"])

    def test_static_long_scene_flagged(self):
        d = sample()
        d["scenes"][1]["visual_change"] = False
        self.assertIn("STATIC_LONG_SCENE", [x["code"] for x in mod.review(d)["issues"]])

    def test_exact_adjacent_repeat_only(self):
        d = sample()
        d["scenes"][2]["narration"] = "A história da mudança!"
        self.assertIn("ADJACENT_EXACT_REPEAT", [x["code"] for x in mod.review(d)["issues"]])

    def test_barely_similar_not_claimed(self):
        d = sample()
        d["scenes"][2]["narration"] = "A história mudou."
        self.assertNotIn("ADJACENT_EXACT_REPEAT", [x["code"] for x in mod.review(d)["issues"]])

    def test_cta_before_payoff(self):
        d = sample()
        d["scenes"][2]["role"] = "CTA"
        d["scenes"][3]["role"] = "PAYOFF"
        self.assertIn("CTA_BEFORE_PAYOFF", [x["code"] for x in mod.review(d)["issues"]])

    def test_no_payoff_is_blocker(self):
        d = sample()
        d["scenes"][2]["role"] = "CONTEXT"
        self.assertIn("PAYOFF_MISSING", [x["code"] for x in mod.review(d)["issues"]])

    def test_missing_cta_editorial(self):
        d = sample()
        d["scenes"][3]["role"] = "EVIDENCE"
        self.assertIn("CTA_MISSING", [x["code"] for x in mod.review(d)["issues"]])

    def test_below_sixty_is_preference_not_rule(self):
        d = sample()
        d["total_frames"] = 1200
        d["scenes"][1]["duration_frames"] = 540
        d["scenes"][2]["start_frame"] = 690
        d["scenes"][3]["start_frame"] = 1050
        self.assertIn("SHORT_BELOW_PREFERENCE", [x["code"] for x in mod.review(d)["issues"]])

    def test_timeline_gap_rejected(self):
        d = sample()
        d["scenes"][2]["start_frame"] = 1400
        with self.assertRaises(ValueError):
            mod.review(d)

    def test_duplicate_id_rejected(self):
        d = sample()
        d["scenes"][1]["id"] = "S01"
        with self.assertRaises(ValueError):
            mod.review(d)

    def test_unsupported_role_rejected(self):
        d = sample()
        d["scenes"][0]["role"] = "HYPE"
        with self.assertRaises(ValueError):
            mod.review(d)


if __name__ == "__main__":
    unittest.main()
