"""J06: pre-publication rights, attribution and affiliate disclosure gate.

This evaluates supplied records; neither a license oracle nor Content ID scan.
Transformations (mirror, crop, CRT, borders) NEVER waive copyright.
No downloading, uploading, posting or spreadsheet writes.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

KINDS = {"image", "video", "audio", "font", "clip", "music", "sfx"}
APPROVAL = {"APPROVED", "PENDING", "REJECTED"}
RULES = {"CREATOR_OWNED", "LICENSED", "PERMISSION", "OTHER_REVIEWED"}
KEYS = {"id", "kind", "source", "rights_status", "basis", "evidence",
        "attribution_required", "attribution_text", "content_id_review",
        "transformations"}


def _https_url(value: str) -> bool:
    if not isinstance(value, str):
        return False
    try:
        parsed = urlsplit(value)
        return (parsed.scheme == "https" and bool(parsed.hostname)
                and not parsed.username and not parsed.password
                and parsed.hostname.lower() not in {"localhost", "127.0.0.1", "::1"})
    except ValueError:
        return False


def review(record: dict) -> dict:
    if not isinstance(record, dict):
        raise ValueError("Record must be an object")
    assets = record.get("assets")
    if not isinstance(assets, list):
        raise ValueError("assets must be a list, even if empty")
    seen = set()
    findings = []
    for index, asset in enumerate(assets):
        if not isinstance(asset, dict) or set(asset) != KEYS:
            raise ValueError(f"Asset {index} missing required rights fields")
        ident = asset["id"]
        if not isinstance(ident, str) or not ident.strip() or ident in seen:
            raise ValueError("Missing or duplicated asset id")
        seen.add(ident)
        if asset["kind"] not in KINDS or asset["rights_status"] not in APPROVAL:
            raise ValueError("Unknown kind/status")
        if not isinstance(asset["source"], str) or not asset["source"].strip():
            raise ValueError("Source and provenance must be recorded")
        if type(asset["attribution_required"]) is not bool:
            raise ValueError("attribution_required must be boolean")
        if not isinstance(asset["attribution_text"], str):
            raise ValueError("attribution_text must be a string")
        if not isinstance(asset["transformations"], list) or any(
                not isinstance(x, str) for x in asset["transformations"]):
            raise ValueError("transformations must be a list of descriptions")
        if asset["content_id_review"] not in ("REVIEWED", "NOT_CHECKED", "NOT_APPLICABLE"):
            raise ValueError("Invalid Content ID review state")
        basis, evidence = asset["basis"], asset["evidence"]
        if basis not in RULES and basis is not None:
            raise ValueError("Unknown rights basis")
        if not isinstance(evidence, str):
            raise ValueError("Rights evidence must be text")

        if asset["rights_status"] != "APPROVED" or basis is None or not evidence.strip():
            findings.append({"asset_id": ident, "severity": "BLOCKER",
                             "code": "RIGHTS_NOT_DOCUMENTED",
                             "detail": "Document applicable rights and verify with a human"})
        if asset["attribution_required"] and not asset["attribution_text"].strip():
            findings.append({"asset_id": ident, "severity": "BLOCKER",
                             "code": "ATTRIBUTION_MISSING",
                             "detail": "Required attribution text is missing"})
        if asset["kind"] in {"video", "clip", "music", "audio", "sfx"} and (
                asset["content_id_review"] == "NOT_CHECKED"):
            findings.append({"asset_id": ident, "severity": "REVIEW",
                             "code": "CONTENT_ID_NOT_REVIEWED",
                             "detail": "Check platform claim risk; no code can guarantee absence"})
        if asset["transformations"] and asset["kind"] in {"video", "clip", "image"}:
            findings.append({"asset_id": ident, "severity": "NOTICE",
                             "code": "TRANSFORMATIONS_DO_NOT_WAIVE_COPYRIGHT",
                             "detail": "Mirroring, cropping, CRT and framing do not confer rights"})

    affiliates = record.get("affiliates", [])
    if not isinstance(affiliates, list):
        raise ValueError("affiliates must be a list")
    affiliate_ids = set()
    for item in affiliates:
        if not isinstance(item, dict) or set(item) != {"id", "url", "verified_for_video"}:
            raise ValueError("Affiliate entries require ID, URL, per-video validation")
        if not isinstance(item["id"], str) or not item["id"].strip() or item["id"] in affiliate_ids:
            raise ValueError("Affiliate ID missing/duplicate")
        affiliate_ids.add(item["id"])
        if not _https_url(item["url"]) or item["verified_for_video"] is not True:
            findings.append({"asset_id": item["id"], "severity": "BLOCKER",
                             "code": "AFFILIATE_NOT_VERIFIED",
                             "detail": "Verify current destination and terms for this video"})
    disclosure = record.get("affiliate_disclosure", "")
    if not isinstance(disclosure, str):
        raise ValueError("affiliate_disclosure must be text")
    if affiliates and not disclosure.strip():
        findings.append({"asset_id": None, "severity": "BLOCKER",
                         "code": "AFFILIATE_DISCLOSURE_MISSING",
                         "detail": "Disclose financial relation clearly in the final kit"})

    blockers = sum(x["severity"] == "BLOCKER" for x in findings)
    reviews = sum(x["severity"] == "REVIEW" for x in findings)
    return {
        "status": "BLOCKED" if blockers else ("REVIEW_REQUIRED" if reviews else "READY_FOR_HUMAN_RIGHTS_APPROVAL"),
        "assets_checked": len(assets),
        "affiliate_links_checked": len(affiliates),
        "findings": findings,
        "rights_verification_performed": False,
        "content_id_scan_performed": False,
        "human_approval_required": True,
        "publishing_performed": False,
        "writes_performed": False
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_json", type=Path)
    args = parser.parse_args()
    try:
        result = review(json.loads(args.input_json.read_text(encoding="utf-8")))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"RIGHTS_REVIEW_FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
