import importlib.util
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "scripts" / "analyze_metrics.py"
spec = importlib.util.spec_from_file_location("diazverso_metrics", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def sample():
    return {"production_id": "VD_0010",
            "youtube_url": "https://www.youtube.com/watch?v=abcdef12345",
            "as_of": "2026-11-10T10:00:00-03:00",
            "source": "YouTube Studio, exportação conferida pelo criador",
            "views": 200, "impressions": 400, "clicks": 20,
            "video_duration_seconds": 100,
            "average_view_duration_seconds": 70}


class MetricsTests(unittest.TestCase):
    def test_valid_metrics_are_observations(self):
        r = mod.analyze(sample())
        self.assertEqual(r["derived_ctr_percent"], 5.0)
        self.assertEqual(r["avg_view_duration_percent"], 70.0)
        self.assertFalse(r["writes_performed"])
        self.assertTrue(r["metrics_are_observations_not_causality"])

    def test_no_source_rejected(self):
        d = sample()
        d["source"] = ""
        with self.assertRaises(ValueError):
            mod.analyze(d)

    def test_future_date_rejected(self):
        d = sample()
        d["as_of"] = "2099-01-01T00:00:00+00:00"
        with self.assertRaises(ValueError):
            mod.analyze(d)

    def test_negative_views_rejected(self):
        d = sample()
        d["views"] = -1
        with self.assertRaises(ValueError):
            mod.analyze(d)

    def test_clicks_over_impressions_rejected(self):
        d = sample()
        d["clicks"] = 500
        with self.assertRaises(ValueError):
            mod.analyze(d)

    def test_missing_analytics_does_not_fabricate_ctr(self):
        d = sample()
        d.pop("impressions")
        d.pop("clicks")
        r = mod.analyze(d)
        self.assertNotIn("derived_ctr_percent", r)


    def test_infinite_metric_rejected(self):
        d = sample()
        d["views"] = float("inf")
        with self.assertRaises(ValueError):
            mod.analyze(d)

    def test_zero_duration_rejected(self):
        d = sample()
        d["video_duration_seconds"] = 0
        with self.assertRaises(ValueError):
            mod.analyze(d)

    def test_no_impressions_no_ctr(self):
        d = sample()
        d["impressions"] = 0
        d["clicks"] = 0
        r = mod.analyze(d)
        self.assertNotIn("derived_ctr_percent", r)



if __name__ == "__main__":
    unittest.main()
