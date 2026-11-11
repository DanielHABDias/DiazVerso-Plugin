"""Validate the vertical preset and optional element boxes against design safe area.

Does not render or claim actual social-platform UI clearances.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

PRESET = Path(__file__).resolve().parents[1] / "references" / "preset-vertical-v1.json"


def check(preset: dict, boxes: list[dict] | None = None) -> dict:
    if (preset.get("width"), preset.get("height"), preset.get("fps"), preset.get("aspect_ratio")) != (1080, 1920, 30, "9:16"):
        raise ValueError("Preset vertical incompatível")
    s = preset["design_safe_area"]
    w, h = preset["width"], preset["height"]
    left, right, top, bottom = [s[k] for k in ("left", "right", "top", "bottom")]
    if not all(type(v) is int and v >= 0 for v in (left, right, top, bottom)):
        raise ValueError("Margens devem ser inteiros positivos")
    bounds = {"x_min":left, "x_max":w - right, "y_min":top, "y_max":h - bottom}
    if bounds != preset["content_bounds"] or bounds["x_min"] >= bounds["x_max"] or bounds["y_min"] >= bounds["y_max"]:
        raise ValueError("Content bounds inconsistentes")
    for region_name in ("caption_region", "headline_region"):
        region = preset[region_name]
        if not (bounds["x_min"] <= region["x_min"] < region["x_max"] <= bounds["x_max"] and
                bounds["y_min"] <= region["y_min"] < region["y_max"] <= bounds["y_max"]):
            raise ValueError(f"{region_name} fora da área segura")
    failures = []
    for item in boxes or []:
        if not isinstance(item, dict) or not all(type(item.get(k)) is int for k in ("x", "y", "width", "height")):
            raise ValueError("Box inválida")
        x, y, bw, bh = [item[k] for k in ("x", "y", "width", "height")]
        if bw <= 0 or bh <= 0 or not (left <= x and x + bw <= w - right and top <= y and y + bh <= h - bottom):
            failures.append(item.get("name", "unnamed"))
    return {"status":"PASS" if not failures else "OUTSIDE_SAFE_AREA",
            "invalid_boxes":failures, "checked_boxes":len(boxes or []),
            "render_verified":False, "publishing_performed":False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--boxes", type=Path, help="JSON array of boxes x/y/width/height")
    args = parser.parse_args()
    preset = json.loads(PRESET.read_text(encoding="utf-8"))
    boxes = json.loads(args.boxes.read_text(encoding="utf-8")) if args.boxes else None
    print(json.dumps(check(preset, boxes), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
