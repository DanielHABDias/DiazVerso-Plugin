#!/usr/bin/env python3
"""capabilities - conservative offline capability gate for a Diazverso host.

Capabilities are supplied as verified facts about the CURRENT session, never
inferred from installed skill files. No connector, renderer or audio-analysis
action is invoked. Unsupported work remains blocked, not simulated.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

CAPABILITIES = ("drive_read", "drive_write", "docs_write", "sheets_read",
                "sheets_write", "render_runtime", "ffmpeg")
ACTIONS = {
    "ideation": (),
    "research_outline": (),
    "draft_script_local": (),
    "draft_thumbnail_brief": (),
    "prepare_decupagem": (),
    "plan_render_commands": (),
    "inspect_local_wav_pcm16": (),
    "discover_drive": ("drive_read",),
    "read_sheet": ("sheets_read",),
    "create_native_doc": ("drive_write", "docs_write"),
    "write_production_row": ("sheets_read", "sheets_write"),
    "render_preview": ("render_runtime",),
    "extract_frames": ("ffmpeg",),
}
# Steps cannot be claimed complete just because the required connector exists.
EVIDENCE_GATES = {
    "create_native_doc": "DOC_WRITE_AND_READBACK",
    "write_production_row": "SHEET_WRITE_AND_READBACK",
    "render_preview": "REAL_RENDER_AND_FRAME_INSPECTION",
    "extract_frames": "REAL_MEDIA_AND_EXTRACTED_PNG",
}
PRODUCTION_RE = re.compile(r"(VD|SH)_\d{4,}\Z")


def evaluate(snapshot: dict, requested: list[str]) -> dict:
    if not isinstance(snapshot, dict) or set(snapshot) != {"session_id", "verified_at", "capabilities"}:
        raise ValueError("Snapshot requires session_id, verified_at and capabilities")
    if not isinstance(snapshot["session_id"], str) or not snapshot["session_id"].strip():
        raise ValueError("Current-session ID required")
    if not isinstance(snapshot["verified_at"], str) or not snapshot["verified_at"].strip():
        raise ValueError("Verification time/reference required")
    caps = snapshot["capabilities"]
    if not isinstance(caps, dict) or set(caps) != set(CAPABILITIES):
        raise ValueError("All capabilities must be explicitly reported")
    if any(type(caps[key]) is not bool for key in CAPABILITIES):
        raise ValueError("Capability states must be explicit booleans")
    if not isinstance(requested, list) or not requested:
        raise ValueError("At least one action must be requested")
    if any(not isinstance(x, str) or x not in ACTIONS for x in requested):
        raise ValueError("Unknown/forbidden action; no posting or upload supported")
    unique = list(dict.fromkeys(requested))
    results = []
    for name in unique:
        missing = [cap for cap in ACTIONS[name] if not caps[cap]]
        allowed = not missing
        results.append({
            "action": name,
            "status": "AVAILABLE_FOR_ATTEMPT" if allowed else "BLOCKED_MISSING_CAPABILITY",
            "missing": missing,
            "evidence_required": EVIDENCE_GATES.get(name),
            "performed": False,
            "completed": False,
        })
    return {
        "status": "DEGRADED" if any(x["missing"] for x in results) else "CAPABILITY_PLAN_ONLY",
        "session_id": snapshot["session_id"],
        "verified_at": snapshot["verified_at"],
        "actions": results,
        "available": [x["action"] for x in results if not x["missing"]],
        "blocked": [x["action"] for x in results if x["missing"]],
        "fallback_rule": "Execute independent editorial tasks only; never fake storage, render, listening or approval",
        "creator_approval_required": True,
        "host_actions_performed": False,
        "publishing_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot_json", type=Path)
    parser.add_argument("--action", required=True, action="append",
                        help="Repeat --action to evaluate multiple tasks")
    args = parser.parse_args()
    try:
        record = json.loads(args.snapshot_json.read_text(encoding="utf-8"))
        print(json.dumps(evaluate(record, args.action), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(f"CAPABILITY_PLAN_FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
