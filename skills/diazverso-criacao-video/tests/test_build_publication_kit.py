import importlib.util
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "scripts" / "build_publication_kit.py"
spec = importlib.util.spec_from_file_location("diazverso_kit", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def sample():
    return {"production_id":"VD_0001", "title":"Por que a HQ mudou?",
            "description":"Uma análise com base na obra.",
            "sources":["HQ, edição 12"], "tags":["hq", "análise"],
            "video_file":"final.mp4", "thumbnail_file":"thumb.png",
            "creator_approved":True, "render_verified":True, "qa_approved":True}


class KitTests(unittest.TestCase):
    def test_ready_manual_no_publish(self):
        r=mod.build_kit(sample())
        self.assertEqual(r["status"],"KIT PRONTO PARA POSTAGEM MANUAL")
        self.assertEqual(r["posting_mode"],"MANUAL_BY_CREATOR")
        self.assertFalse(r["publishing_performed"])

    def test_pending_if_not_rendered(self):
        d=sample();d["render_verified"]=False
        self.assertEqual(mod.build_kit(d)["status"],"KIT PARCIAL — PENDÊNCIAS")

    def test_unverified_affiliate_blocked(self):
        d=sample();d["affiliate_links"]=[{"name":"Livro","url":"https://example.com/","verified_for_production":False}]
        with self.assertRaises(ValueError):mod.build_kit(d)

    def test_affiliate_disclosure(self):
        d=sample();d["affiliate_links"]=[{"name":"Livro","url":"https://example.com/","verified_for_production":True}]
        self.assertIn("comissão",mod.build_kit(d)["description"])

    def test_chapters_require_render_review(self):
        d=sample();d["chapters"]=[{"seconds":0,"title":"Abertura"}]
        with self.assertRaises(ValueError):mod.build_kit(d)

    def test_chapters_in_order_and_verified(self):
        d=sample();d["chapters_verified"]=True;d["chapters"]=[{"seconds":0,"title":"Abertura"},{"seconds":65,"title":"Motivos"}]
        self.assertIn("00:01:05",mod.build_kit(d)["description"])

    def test_no_fabricated_sources(self):
        d=sample();d["sources"]=[]
        with self.assertRaises(ValueError):mod.build_kit(d)


if __name__ == "__main__":
    unittest.main()
