import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("thumb_brief", ROOT/"scripts"/"validate_thumbnail_brief.py")
mod=importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)

def fixture():
    return json.loads((ROOT/"examples"/"thumbnail-brief.example.json").read_text(encoding="utf-8"))

class ThumbnailBriefTests(unittest.TestCase):
    def test_distinct_variants_are_ready_for_human_review(self):
        result=mod.validate(fixture())
        self.assertEqual(result["status"],"BRIEF_READY_FOR_HUMAN_CREATIVE_REVIEW")
        self.assertFalse(result["image_generated"])
        self.assertFalse(result["pixel_contrast_verified"])
        self.assertFalse(result["publishing_performed"])

    def test_same_angle_and_layout_is_not_true_ab(self):
        d=fixture()
        d["variants"]["B"]["angle"]=d["variants"]["A"]["angle"]
        d["variants"]["B"]["layout"]=d["variants"]["A"]["layout"]
        self.assertEqual(mod.validate(d)["status"],"BRIEF_NEEDS_REVISION")

    def test_missing_variant_rejected(self):
        d=fixture();d["variants"].pop("B")
        with self.assertRaises(ValueError):mod.validate(d)

    def test_too_many_words_flagged(self):
        d=fixture();d["variants"]["A"]["on_image_text"]="UM TEXTO MUITO LONGO PARA CELULAR"
        self.assertIn("LONG_THUMBNAIL_TEXT",[x["code"] for x in mod.validate(d)["issues"]])

    def test_title_repetition_flagged(self):
        d=fixture();d["variants"]["A"]["on_image_text"]=d["title"]
        self.assertIn("TEXT_REPEATS_TITLE",[x["code"] for x in mod.validate(d)["issues"]])

    def test_rights_pending_blocks(self):
        d=fixture();d["assets"][0]["rights_status"]="PENDING"
        self.assertEqual(mod.validate(d)["status"],"BRIEF_NEEDS_REVISION")

    def test_empty_approval_evidence_blocks(self):
        d=fixture();d["assets"][0]["rights_evidence"]=""
        self.assertEqual(mod.validate(d)["status"],"BRIEF_NEEDS_REVISION")

    def test_missing_media_blocks(self):
        d=fixture();d["assets"][0]["available"]=False
        self.assertEqual(mod.validate(d)["status"],"BRIEF_NEEDS_REVISION")

    def test_unknown_asset_rejected(self):
        d=fixture();d["variants"]["A"]["assets_used"]=["unknown"]
        with self.assertRaises(ValueError):mod.validate(d)

    def test_nox_requires_canonical_reference(self):
        d=fixture();d["variants"]["A"]["nox"]="CANONICAL_ONLY"
        self.assertIn("NOX_CANONICAL_ASSET_NOT_REFERENCED",
                      [x["code"] for x in mod.validate(d)["issues"]])

    def test_nox_pose_needs_character_lock_review(self):
        d=fixture()
        d["assets"].append({"id":"nox","source":"assets/brand/nox/Nox.png",
            "rights_status":"APPROVED","rights_evidence":"Asset canônico conferido","available":True})
        d["variants"]["A"]["nox"]="POSE_REQUIRES_REVIEW"
        d["variants"]["A"]["assets_used"].append("nox")
        self.assertIn("NOX_POSE_REQUIRES_CHARACTER_LOCK",
                      [x["code"] for x in mod.validate(d)["issues"]])

    def test_unapproved_script_remains_preliminary(self):
        d=fixture();d["script_approved"]=False
        self.assertEqual(mod.validate(d)["status"],"PRELIMINARY_BRIEF")

    def test_wrong_production_format_rejected(self):
        d=fixture();d["production_id"]="SH_0001"
        with self.assertRaises(ValueError):mod.validate(d)

    def test_asset_duplicate_id_rejected(self):
        d=fixture();d["assets"].append(copy.deepcopy(d["assets"][0]))
        with self.assertRaises(ValueError):mod.validate(d)

if __name__=="__main__":unittest.main()
