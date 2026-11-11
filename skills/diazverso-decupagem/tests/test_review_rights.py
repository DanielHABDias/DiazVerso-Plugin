import importlib.util
import unittest
from pathlib import Path

FILE = Path(__file__).resolve().parents[1] / "scripts" / "review_rights.py"
spec = importlib.util.spec_from_file_location("diazverso_rights", FILE)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def asset():
    return {"id": "clip01", "kind": "clip", "source": "Criador — material autorizado",
            "rights_status": "APPROVED", "basis": "PERMISSION",
            "evidence": "Registro documental conferido pelo responsável",
            "attribution_required": True, "attribution_text": "Crédito aprovado",
            "content_id_review": "REVIEWED", "transformations": []}


def record():
    return {"assets": [asset()], "affiliates": [], "affiliate_disclosure": ""}


class RightsTests(unittest.TestCase):
    def test_reviewed_asset_ready_only_for_human_gate(self):
        out = mod.review(record())
        self.assertEqual(out["status"], "READY_FOR_HUMAN_RIGHTS_APPROVAL")
        self.assertFalse(out["rights_verification_performed"])
        self.assertFalse(out["content_id_scan_performed"])
        self.assertFalse(out["publishing_performed"])

    def test_pending_license_blocks(self):
        d = record()
        d["assets"][0]["rights_status"] = "PENDING"
        self.assertEqual(mod.review(d)["status"], "BLOCKED")

    def test_approval_without_evidence_blocks(self):
        d = record()
        d["assets"][0]["evidence"] = ""
        self.assertIn("RIGHTS_NOT_DOCUMENTED", [x["code"] for x in mod.review(d)["findings"]])

    def test_missing_required_attribution_blocks(self):
        d = record()
        d["assets"][0]["attribution_text"] = ""
        self.assertIn("ATTRIBUTION_MISSING", [x["code"] for x in mod.review(d)["findings"]])

    def test_crt_does_not_remove_rights(self):
        d = record()
        d["assets"][0]["transformations"] = ["CRT", "espelhar"]
        self.assertIn("TRANSFORMATIONS_DO_NOT_WAIVE_COPYRIGHT",
                      [x["code"] for x in mod.review(d)["findings"]])

    def test_content_id_not_checked_needs_review(self):
        d = record()
        d["assets"][0]["content_id_review"] = "NOT_CHECKED"
        self.assertEqual(mod.review(d)["status"], "REVIEW_REQUIRED")

    def test_affiliate_without_disclosure_blocks(self):
        d = record()
        d["affiliates"] = [{"id": "AF_0001", "url": "https://example.com/link",
                            "verified_for_video": True}]
        self.assertEqual(mod.review(d)["status"], "BLOCKED")

    def test_affiliate_link_needs_current_verification(self):
        d = record()
        d["affiliates"] = [{"id": "AF_0001", "url": "https://example.com/link",
                            "verified_for_video": False}]
        d["affiliate_disclosure"] = "Posso receber comissão."
        self.assertIn("AFFILIATE_NOT_VERIFIED", [x["code"] for x in mod.review(d)["findings"]])

    def test_duplicate_asset_id_invalid(self):
        d = record()
        d["assets"].append(asset())
        with self.assertRaises(ValueError):
            mod.review(d)

    def test_empty_asset_list_does_not_invent_evidence(self):
        out = mod.review({"assets": [], "affiliates": [], "affiliate_disclosure": ""})
        self.assertEqual(out["assets_checked"], 0)
        self.assertTrue(out["human_approval_required"])

    def test_unknown_basis_rejected(self):
        d = record()
        d["assets"][0]["basis"] = "FAIR_USE_AUTOMATIC"
        with self.assertRaises(ValueError):
            mod.review(d)


if __name__ == "__main__":
    unittest.main()
