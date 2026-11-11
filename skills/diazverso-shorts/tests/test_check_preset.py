import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("preset_checker", ROOT/"scripts"/"check_preset.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


def preset():
    return json.loads((ROOT/"references"/"preset-vertical-v1.json").read_text(encoding="utf-8"))


class VerticalPresetTests(unittest.TestCase):
    def test_canonical_preset(self):
        result=module.check(preset())
        self.assertEqual(result["status"],"PASS")
        self.assertFalse(result["render_verified"])

    def test_text_in_safe_area(self):
        r=module.check(preset(),[{"name":"title","x":130,"y":350,"width":500,"height":200}])
        self.assertEqual(r["status"],"PASS")

    def test_bottom_caption_outside(self):
        r=module.check(preset(),[{"name":"caption","x":130,"y":1500,"width":500,"height":240}])
        self.assertEqual(r["invalid_boxes"],["caption"])

    def test_frame_edge_rejected(self):
        r=module.check(preset(),[{"name":"top-left","x":0,"y":0,"width":100,"height":100}])
        self.assertEqual(r["status"],"OUTSIDE_SAFE_AREA")

    def test_wrong_aspect_rejected(self):
        p=preset();p["height"]=1080
        with self.assertRaises(ValueError): module.check(p)

    def test_regions_must_be_within_safe_area(self):
        p=preset();p["caption_region"]["y_max"]=1900
        with self.assertRaises(ValueError): module.check(p)

    def test_float_coordinates_rejected(self):
        with self.assertRaises(ValueError):
            module.check(preset(),[{"x":1.5,"y":350,"width":500,"height":200}])


if __name__ == "__main__":
    unittest.main()
