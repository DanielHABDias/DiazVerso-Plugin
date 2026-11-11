#!/usr/bin/env python3
"""G02: conservative contract check for two distinct editorial thumbnails.

A plan is not an image. No generation, API use, rights certification, CTR
prediction or YouTube posting is performed.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = re.compile(r"(VD|SH)_\d{4,}\Z")
WORD = re.compile(r"\S+")
ANGLES = {"CONTRADICTION", "COMPARISON", "CONSEQUENCE", "REVELATION",
          "QUESTION", "TRANSFORMATION"}
LAYOUTS = {"SPLIT", "FOCAL_LEFT", "FOCAL_RIGHT", "CENTER_FOCUS", "DIAGONAL"}
STATUS = {"APPROVED", "PENDING", "REJECTED"}


def _required_text(value: object, label: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{label} must be nonempty text")
    return value.strip()


def validate(data: dict) -> dict:
    if not isinstance(data, dict) or set(data) != {
            "production_id", "format", "thesis", "promise", "title",
            "subject", "script_approved", "assets", "variants"}:
        raise ValueError("Invalid G02 brief fields")
    prod = data["production_id"]
    if not isinstance(prod, str) or not ROOT.fullmatch(prod):
        raise ValueError("Invalid production ID")
    if data["format"] not in ("LONGO", "SHORT") or (
            data["format"] == "LONGO") != prod.startswith("VD_"):
        raise ValueError("Production ID/format mismatch")
    for field in ("thesis", "promise", "title", "subject"):
        _required_text(data[field], field)
    if type(data["script_approved"]) is not bool:
        raise ValueError("script_approved must be explicit boolean")
    if not isinstance(data["assets"], list):
        raise ValueError("assets must be a list")
    assets = {}
    issues = []
    for item in data["assets"]:
        if not isinstance(item, dict) or set(item) != {
                "id", "source", "rights_status", "rights_evidence", "available"}:
            raise ValueError("Malformed asset")
        aid = _required_text(item["id"], "asset.id")
        if aid in assets:
            raise ValueError("Duplicate asset ID")
        _required_text(item["source"], "asset.source")
        if item["rights_status"] not in STATUS:
            raise ValueError("Invalid asset rights status")
        if not isinstance(item["rights_evidence"], str) or type(item["available"]) is not bool:
            raise ValueError("Invalid asset evidence/availability")
        assets[aid] = item

    variants = data["variants"]
    if not isinstance(variants, dict) or set(variants) != {"A", "B"}:
        raise ValueError("Exactly A and B are required")
    signatures = {}
    for name in ("A", "B"):
        variant = variants[name]
        required = {"angle", "visual_metaphor", "layout", "on_image_text",
                    "focus", "contrast_plan", "nox", "assets_used", "rationale"}
        if not isinstance(variant, dict) or set(variant) != required:
            raise ValueError(f"Variant {name} fields invalid")
        if variant["angle"] not in ANGLES or variant["layout"] not in LAYOUTS:
            raise ValueError("Unknown editorial angle/layout")
        for key in ("visual_metaphor", "focus", "contrast_plan", "rationale"):
            _required_text(variant[key], f"{name}.{key}")
        text = variant["on_image_text"]
        if not isinstance(text, str):
            raise ValueError("On-image text must be a string")
        if len(WORD.findall(text.strip())) > 4:
            issues.append({"code": "LONG_THUMBNAIL_TEXT", "variant": name,
                           "detail": "Prefer <=4 words; review mobile legibility"})
        if text.strip().casefold() == data["title"].strip().casefold() and text.strip():
            issues.append({"code": "TEXT_REPEATS_TITLE", "variant": name,
                           "detail": "Consider complementary rather than identical text"})
        if variant["nox"] not in ("NONE", "CANONICAL_ONLY", "POSE_REQUIRES_REVIEW"):
            raise ValueError("Unknown Nox use")
        if variant["nox"] == "POSE_REQUIRES_REVIEW":
            issues.append({"code": "NOX_POSE_REQUIRES_CHARACTER_LOCK", "variant": name,
                           "detail": "G01 identity review before producing new pose"})
        refs = variant["assets_used"]
        if not isinstance(refs, list) or len(set(refs)) != len(refs):
            raise ValueError("Assets used must be unique IDs")
        for ref in refs:
            if not isinstance(ref, str) or ref not in assets:
                raise ValueError("Unknown asset ID in variant")
            asset = assets[ref]
            if asset["rights_status"] != "APPROVED" or not asset["rights_evidence"].strip() or not asset["available"]:
                issues.append({"code": "UNAPPROVED_OR_MISSING_ASSET", "variant": name,
                               "asset_id": ref, "detail": "Require current source and rights review"})
        if variant["nox"] != "NONE":
            if "nox" not in refs:
                issues.append({"code": "NOX_CANONICAL_ASSET_NOT_REFERENCED", "variant": name,
                               "detail": "Use canonical Nox PNG reference"})
            elif assets["nox"]["source"] != "assets/brand/nox/Nox.png":
                issues.append({"code": "NOX_SOURCE_NOT_CANONICAL", "variant": name,
                               "detail": "Use assets/brand/nox/Nox.png"})
        signatures[name] = (variant["angle"], variant["layout"],
                            " ".join(variant["visual_metaphor"].casefold().split()))
    if signatures["A"] == signatures["B"] or (
            variants["A"]["angle"] == variants["B"]["angle"]
            and variants["A"]["layout"] == variants["B"]["layout"]):
        issues.append({"code": "AB_VARIANTS_TOO_SIMILAR", "variant": None,
                       "detail": "Change editorial angle and layout, not only colors"})
    if not data["script_approved"]:
        issues.append({"code": "SCRIPT_NOT_APPROVED", "variant": None,
                       "detail": "Concepts must remain preliminary"})
    hard = {"UNAPPROVED_OR_MISSING_ASSET", "NOX_CANONICAL_ASSET_NOT_REFERENCED",
            "NOX_SOURCE_NOT_CANONICAL", "AB_VARIANTS_TOO_SIMILAR"}
    return {"status": "BRIEF_NEEDS_REVISION" if any(x["code"] in hard for x in issues)
            else ("PRELIMINARY_BRIEF" if not data["script_approved"]
                  else "BRIEF_READY_FOR_HUMAN_CREATIVE_REVIEW"),
            "production_id": prod, "issues": issues,
            "variants": ["A", "B"], "image_generated": False,
            "pixel_contrast_verified": False, "license_verified_by_code": False,
            "ctr_prediction": None, "drive_write_performed": False,
            "publishing_performed": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("brief_json", type=Path)
    args = parser.parse_args()
    try:
        result = validate(json.loads(args.brief_json.read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] == "BRIEF_READY_FOR_HUMAN_CREATIVE_REVIEW" else 2
    except (ValueError, TypeError, KeyError, OSError) as exc:
        print(f"THUMBNAIL_BRIEF_INVALID: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
