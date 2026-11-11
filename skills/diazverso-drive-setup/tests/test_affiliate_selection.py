import importlib.util
import unittest
from pathlib import Path

P = Path(__file__).resolve().parents[1] / "scripts" / "affiliate_selection.py"
spec = importlib.util.spec_from_file_location("diazverso_affiliates", P)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def item(ident="AF_01", status="ATIVO", applicable="Marvel;HQ", link="https://example.com/product"):
    return [ident, "Produto", "Livros", "Loja", link, applicable,
            status, "2026-10-15", "Fonte", ""]


class AffiliateSelectionTests(unittest.TestCase):
    def test_only_active_relevant_reverified(self):
        rows = [mod.HEADERS, item(), item("AF_02", "A CONFERIR"),
                item("AF_03", "ATIVO", "DC")]
        r = mod.select_affiliates(rows, ["Marvel"], verified_ids=["AF_01", "AF_02", "AF_03"])
        self.assertEqual([x["id"] for x in r["selected"]], ["AF_01"])
        self.assertTrue(r["requires_disclosure"])
        self.assertFalse(r["writes_performed"])
        self.assertFalse(r["publishing_performed"])

    def test_no_video_reverification_no_link(self):
        r = mod.select_affiliates([mod.HEADERS, item()], ["Marvel"], verified_ids=[])
        self.assertEqual(r["selected"], [])
        self.assertFalse(r["requires_disclosure"])

    def test_unrelated_no_insertion(self):
        r = mod.select_affiliates([mod.HEADERS, item()], ["Ben 10"], verified_ids=["AF_01"])
        self.assertEqual(r["selected"], [])

    def test_http_and_local_links_rejected(self):
        for link in ["http://example.com/p", "https://localhost/p",
                     "https://user:secret@example.com/p", "file:///etc/passwd"]:
            with self.subTest(link=link):
                r = mod.select_affiliates([mod.HEADERS, item(link=link)],
                                         ["Marvel"], verified_ids=["AF_01"])
                self.assertFalse(r["selected"])

    def test_duplicate_ids_block(self):
        with self.assertRaises(ValueError):
            mod.select_affiliates([mod.HEADERS, item(), item()], ["Marvel"], verified_ids=["AF_01"])

    def test_invalid_headers_block(self):
        with self.assertRaises(ValueError):
            mod.select_affiliates([["ID", "WRONG"], item()], ["Marvel"], verified_ids=[])

    def test_limit_and_disclosure(self):
        r = mod.select_affiliates([mod.HEADERS, item(), item("AF_02")],
                                  ["HQ"], verified_ids=["AF_01", "AF_02"], max_items=1)
        self.assertEqual(len(r["selected"]), 1)
        self.assertTrue(r["review_overflow"])
        self.assertIn("comissão", r["disclosure_suggestion"])


if __name__ == "__main__":
    unittest.main()
