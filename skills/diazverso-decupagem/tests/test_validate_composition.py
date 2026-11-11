import copy
import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("composition_check", ROOT/"scripts"/"validate_composition.py")
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)


def sample():
    return json.loads((ROOT/"examples"/"short-remotion-props.example.json").read_text(encoding="utf-8"))


class CompositionContractTests(unittest.TestCase):
    def test_example_valid_without_claiming_render(self):
        result = mod.validate(sample())
        self.assertEqual(result["status"], "VALID_CONTRACT")
        self.assertEqual(result["duration_frames"], 180)
        self.assertFalse(result["runtime_render_verified"])

    def test_wrong_aspect(self):
        data=sample();data["width"]=1920
        with self.assertRaises(ValueError):mod.validate(data)

    def test_gap_in_timeline(self):
        data=sample();data["scenes"][1]["start_frame"]=91
        with self.assertRaises(ValueError):mod.validate(data)

    def test_total_duration_mismatch(self):
        data=sample();data["duration_frames"]=200
        with self.assertRaises(ValueError):mod.validate(data)

    def test_unsafe_absolute_asset(self):
        data=sample();data["assets"][0]["path"]="/private/nox.png"
        with self.assertRaises(ValueError):mod.validate(data)

    def test_asset_path_traversal(self):
        data=sample();data["assets"][0]["path"]="../secrets.png"
        with self.assertRaises(ValueError):mod.validate(data)

    def test_unapproved_rights(self):
        data=sample();data["assets"][0]["rights"]="PENDING"
        with self.assertRaises(ValueError):mod.validate(data)

    def test_missing_asset_id(self):
        data=sample();data["scenes"][0]["layers"][0]["asset_id"]="unknown"
        with self.assertRaises(ValueError):mod.validate(data)

    def test_audio_asset_type(self):
        data=sample();data["scenes"][0]["audio"][0]["asset_id"]="nox"
        with self.assertRaises(ValueError):mod.validate(data)

    def test_cue_overflow(self):
        data=sample();data["scenes"][0]["captions"][0]["duration_frames"]=100
        with self.assertRaises(ValueError):mod.validate(data)

    def test_output_path_safety(self):
        data=sample();data["output"]["basename"]="../../escape"
        with self.assertRaises(ValueError):mod.validate(data)

    def test_long_format(self):
        data=sample();data["production_id"]="VD_0001";data["format"]="LONGO"
        data["width"]=1920;data["height"]=1080
        self.assertEqual(mod.validate(data)["status"], "VALID_CONTRACT")

    def test_duplicate_scene(self):
        data=sample();data["scenes"][1]["id"]="S01"
        with self.assertRaises(ValueError):mod.validate(data)


if __name__ == "__main__":
    unittest.main()
