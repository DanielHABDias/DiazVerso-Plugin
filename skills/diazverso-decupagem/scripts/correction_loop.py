#!/usr/bin/env python3
"""J07: one-issue-at-a-time correction workflow with render and review gates.

Pure JSON state transitions, no asset edits, no rendering, no Drive writes,
no posting. Evidence IDs/hashes are caller supplied; their authenticity still
requires checking the actual files and review outputs.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

VALID_SOURCES = {"J01", "J03", "J04", "J05", "J06", "I05"}
PRIORITIES = {"BLOCKER": 0, "REVIEW": 1, "EDITORIAL": 2, "NOTICE": 3}
STAGES = ("OPEN", "FIX_APPLIED", "RERENDERED", "REVIEWED", "CLOSED")
SHA256 = re.compile(r"[a-f0-9]{64}\Z")
PRODUCTION = re.compile(r"(?:VD|SH)_\d{4,}\Z")


def _nonempty(value: object, field: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field} must be nonempty text")
    return value.strip()


def _sha(value: object, field: str) -> str:
    if not isinstance(value, str) or not SHA256.fullmatch(value):
        raise ValueError(f"{field} must be a sha256 digest")
    return value


def collect(production_id: str, source_reports: list[dict], base_render_sha256: str) -> dict:
    """Build an ordered queue; never claim source findings are human verified."""
    if not isinstance(production_id, str) or not PRODUCTION.fullmatch(production_id):
        raise ValueError("Invalid production ID")
    _sha(base_render_sha256, "base_render_sha256")
    if not isinstance(source_reports, list) or not source_reports:
        raise ValueError("At least one real review report is required")
    issues = []
    unique = set()
    for report in source_reports:
        if not isinstance(report, dict) or set(report) != {"source", "findings", "evidence_ref"}:
            raise ValueError("Each report requires source, findings, evidence_ref")
        source = report["source"]
        if source not in VALID_SOURCES or not isinstance(report["findings"], list):
            raise ValueError("Unsupported review source or findings")
        evidence = _nonempty(report["evidence_ref"], "evidence_ref")
        for finding in report["findings"]:
            if not isinstance(finding, dict):
                raise ValueError("Invalid finding")
            code = _nonempty(finding.get("code"), "finding.code")
            severity = finding.get("severity", "REVIEW")
            if severity not in PRIORITIES:
                raise ValueError("Invalid finding severity")
            scene = finding.get("scene")
            if scene is not None and (not isinstance(scene, str) or not re.fullmatch(r"S\d{2,4}", scene)):
                raise ValueError("Invalid scene identifier")
            identity = (source, code, scene)
            if identity in unique:
                continue
            unique.add(identity)
            issues.append({"source": source, "code": code, "scene": scene,
                           "severity": severity, "evidence_ref": evidence})
    issues.sort(key=lambda issue: (PRIORITIES[issue["severity"]], issue["source"],
                                  issue["scene"] or "", issue["code"]))
    for i, issue in enumerate(issues, start=1):
        issue["task_id"] = f"FIX_{i:04d}"
        issue["stage"] = "OPEN"
        issue["fix"] = None
        issue["rerender"] = None
        issue["recheck"] = None
        issue["render_history"] = []
    return {"schema": "diazverso-correction-loop-v1",
            "production_id": production_id, "base_render_sha256": base_render_sha256,
            "tasks": issues, "event_index": 0, "writes_performed": False,
            "render_performed": False, "publishing_performed": False}


def _assert_state(data: dict) -> None:
    if (not isinstance(data, dict) or
        set(data) != {"schema", "production_id", "base_render_sha256", "tasks",
                      "event_index", "writes_performed", "render_performed", "publishing_performed"} or
        data["schema"] != "diazverso-correction-loop-v1"):
        raise ValueError("Invalid correction state")
    if not isinstance(data["production_id"], str) or not PRODUCTION.fullmatch(data["production_id"]):
        raise ValueError("Invalid production in state")
    _sha(data["base_render_sha256"], "base render")
    if type(data["event_index"]) is not int or data["event_index"] < 0:
        raise ValueError("Invalid event index")
    if not isinstance(data["tasks"], list):
        raise ValueError("Invalid task collection")
    active = 0
    seen_ids = set()
    for task in data["tasks"]:
        if not isinstance(task, dict) or set(task) != {
                "source", "code", "scene", "severity", "evidence_ref", "task_id",
                "stage", "fix", "rerender", "recheck", "render_history"}:
            raise ValueError("Invalid task shape")
        if task["stage"] not in STAGES or task["task_id"] in seen_ids:
            raise ValueError("Invalid task stage/identity")
        seen_ids.add(task["task_id"])
        if not isinstance(task["render_history"], list) or any(
                not isinstance(h, str) or not SHA256.fullmatch(h) for h in task["render_history"]):
            raise ValueError("Invalid previous render receipts")
        if task["stage"] in ("FIX_APPLIED", "RERENDERED", "REVIEWED"):
            active += 1
    if active > 1:
        raise ValueError("Two active fixes are forbidden")


def next_task(state: dict) -> dict | None:
    _assert_state(state)
    return next((copy.deepcopy(task) for task in state["tasks"] if task["stage"] not in ("CLOSED",)), None)


def advance(state: dict, task_id: str, action: str, evidence: dict) -> dict:
    """Pure transition. Caller must persist returned JSON only after approval."""
    _assert_state(state)
    if not isinstance(evidence, dict):
        raise ValueError("Evidence must be a JSON object")
    pending = next_task(state)
    if pending is None or pending["task_id"] != task_id:
        raise ValueError("Only the first unfinished task may advance")
    new_state = copy.deepcopy(state)
    task = next(t for t in new_state["tasks"] if t["task_id"] == task_id)
    stage = task["stage"]
    if stage == "OPEN" and action == "record_fix":
        if set(evidence) != {"change_ref", "description", "new_source_sha256"}:
            raise ValueError("Fix needs change reference, explanation and source hash")
        _nonempty(evidence["change_ref"], "change_ref")
        _nonempty(evidence["description"], "description")
        _sha(evidence["new_source_sha256"], "new_source_sha256")
        task["fix"] = evidence
        task["stage"] = "FIX_APPLIED"
    elif stage == "FIX_APPLIED" and action == "record_rerender":
        if set(evidence) != {"render_ref", "render_sha256", "source_sha256", "scope", "verified_file"}:
            raise ValueError("Rerender requires a verifiable file receipt")
        _nonempty(evidence["render_ref"], "render_ref")
        _sha(evidence["render_sha256"], "render_sha256")
        _sha(evidence["source_sha256"], "source_sha256")
        if evidence["source_sha256"] != task["fix"]["new_source_sha256"]:
            raise ValueError("Render used different source revision")
        old = new_state["base_render_sha256"] if not any(
            t["stage"] == "CLOSED" for t in new_state["tasks"]) else next(
                t["rerender"]["render_sha256"] for t in reversed(new_state["tasks"])
                if t["stage"] == "CLOSED")
        if evidence["render_sha256"] == old or evidence["render_sha256"] in task["render_history"]:
            raise ValueError("Rerender receipt matches a prior render")
        if evidence["scope"] not in ("SCENE", "FULL") or evidence["verified_file"] is not True:
            raise ValueError("File must be checked and scope declared")
        task["rerender"] = evidence
        task["stage"] = "RERENDERED"
    elif stage == "RERENDERED" and action == "record_recheck":
        if set(evidence) != {"review_ref", "render_sha256", "reviewed_source",
                             "reviewed_code", "reviewed_scene", "result", "review_evidence"}:
            raise ValueError("Recheck needs complete reviewer evidence")
        _nonempty(evidence["review_ref"], "review_ref")
        _nonempty(evidence["review_evidence"], "review_evidence")
        _sha(evidence["render_sha256"], "recheck render")
        if evidence["render_sha256"] != task["rerender"]["render_sha256"]:
            raise ValueError("Recheck did not use the new render")
        if (evidence["reviewed_source"], evidence["reviewed_code"], evidence["reviewed_scene"]) != (
            task["source"], task["code"], task["scene"]):
            raise ValueError("Recheck does not address the original issue")
        if evidence["result"] not in ("PASSED", "FAILED"):
            raise ValueError("Recheck requires an explicit outcome")
        task["recheck"] = evidence
        task["stage"] = "REVIEWED"
    elif stage == "REVIEWED" and action == "close":
        if evidence != {}:
            raise ValueError("Close takes no new evidence")
        if task["recheck"]["result"] != "PASSED":
            raise ValueError("A failed review cannot close an issue")
        task["stage"] = "CLOSED"
    elif stage == "REVIEWED" and action == "retry":
        if evidence != {} or task["recheck"]["result"] != "FAILED":
            raise ValueError("Retry only follows a failed recheck")
        task["render_history"].append(task["rerender"]["render_sha256"])
        task["stage"] = "OPEN"
        task["fix"] = task["rerender"] = task["recheck"] = None
    else:
        raise ValueError(f"Unsupported transition: {stage} -> {action}")
    new_state["event_index"] += 1
    return new_state


def summary(state: dict) -> dict:
    _assert_state(state)
    todo = next_task(state)
    return {"status": "ALL_ISSUES_CLOSED" if todo is None else "CORRECTION_PENDING",
            "production_id": state["production_id"],
            "task_count": len(state["tasks"]),
            "closed": sum(t["stage"] == "CLOSED" for t in state["tasks"]),
            "next_task": todo, "ready_for_creator_approval": todo is None,
            "creator_approved": False, "actual_render_verified_by_script": False,
            "publishing_performed": False}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("state", type=Path, help="Existing correction state JSON")
    parser.add_argument("--task-id")
    parser.add_argument("--action", choices=["record_fix", "record_rerender",
                                             "record_recheck", "close", "retry"])
    parser.add_argument("--evidence", type=Path)
    parser.add_argument("--out", type=Path)
    args = parser.parse_args()
    try:
        current = json.loads(args.state.read_text(encoding="utf-8"))
        if args.action:
            if not args.task_id or not args.out or (args.action not in ("close","retry") and not args.evidence):
                raise ValueError("Transitions require task-id, out, and evidence as appropriate")
            payload = json.loads(args.evidence.read_text(encoding="utf-8")) if args.evidence else {}
            changed = advance(current, args.task_id, args.action, payload)
            if args.out.exists():
                raise FileExistsError("Refusing to replace existing state file")
            args.out.write_text(json.dumps(changed, ensure_ascii=False, indent=2)+"\n",encoding="utf-8")
            current = changed
        print(json.dumps(summary(current), ensure_ascii=False, indent=2))
        return 0
    except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
        print("CORRECTION_LOOP_FAILED: "+str(exc), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
