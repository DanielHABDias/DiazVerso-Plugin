#!/usr/bin/env python3
"""J01: review H01 composition, local assets, TSX sources and render evidence.

No install, no network, no posting and no content modifications. JSON contract
validation is real; a TSX source scan is NOT TypeScript compilation. Optionally
run a local preinstalled tsc and inspect a real MP4 via preinstalled ffprobe.
"""
from __future__ import annotations

import argparse
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

_SPEC = importlib.util.spec_from_file_location(
    "diazverso_h01_validator", Path(__file__).with_name("validate_composition.py")
)
_MOD = importlib.util.module_from_spec(_SPEC)
_SPEC.loader.exec_module(_MOD)
DANGEROUS_TSX = (
    (re.compile(r"\b(?:eval|new\s+Function)\s*\("), "DYNAMIC_CODE_EXECUTION"),
    (re.compile(r"\b(?:fetch|XMLHttpRequest|WebSocket)\s*\("), "NETWORK_IN_RENDER"),
)
SUPPORTED_EXT = {".ts", ".tsx", ".mjs", ".mts", ".js", ".jsx"}


def _finding(code: str, detail: str, severity: str = "BLOCKER") -> dict:
    return {"code": code, "severity": severity, "detail": detail}


def review(
    props: dict, *, project_root: Path, tsx_files: list[Path],
    render_file: Path | None = None, run_tsc: bool = False,
    tsc_timeout_s: int = 120,
) -> dict:
    findings = []
    try:
        result = _MOD.validate(props)
    except (ValueError, TypeError, KeyError) as exc:
        return {"status": "BLOCKED", "findings": [_finding("INVALID_H01_CONTRACT", str(exc))],
                "contract_valid": False, "typescript_compiled": False,
                "render_inspected": False, "human_qa_complete": False,
                "publishing_performed": False}
    root = project_root.resolve(strict=True)
    if not root.is_dir():
        raise ValueError("Project root must be a directory")

    # Existence and containment are separate from the H01 logical asset catalog.
    assets_checked = 0
    for asset in props["assets"]:
        candidate = (root / asset["path"]).resolve()
        if not candidate.is_relative_to(root):
            findings.append(_finding("ASSET_OUTSIDE_PROJECT", asset["id"]))
        elif not candidate.is_file():
            findings.append(_finding("ASSET_MISSING", f"{asset['id']}: {asset['path']}"))
        else:
            assets_checked += 1

    if not isinstance(tsx_files, list) or not tsx_files:
        raise ValueError("At least one TSX/TS source must be supplied")
    source_files_checked = 0
    for source in tsx_files:
        source = source.resolve()
        if not source.is_relative_to(root) or source.suffix not in SUPPORTED_EXT:
            findings.append(_finding("SOURCE_OUTSIDE_PROJECT", str(source)))
            continue
        if not source.is_file():
            findings.append(_finding("SOURCE_MISSING", str(source)))
            continue
        source_files_checked += 1
        data = source.read_text(encoding="utf-8")
        for pattern, code in DANGEROUS_TSX:
            if pattern.search(data):
                findings.append(_finding(code, source.name))
        if source.suffix == ".tsx" and not re.search(r"\b(?:export|const|function|class)\b", data):
            findings.append(_finding("SOURCE_REVIEW", f"No obvious component declaration: {source.name}", "REVIEW"))

    typescript_compiled = False
    if run_tsc:
        if type(tsc_timeout_s) is not int or not 1 <= tsc_timeout_s <= 600:
            raise ValueError("Invalid TypeScript check timeout")
        if not (root / "tsconfig.json").is_file():
            findings.append(_finding("TSCONFIG_MISSING", "tsconfig.json not found"))
        elif shutil.which("npx") is None:
            findings.append(_finding("TSC_UNAVAILABLE", "npx unavailable"))
        else:
            try:
                completed = subprocess.run(
                    ["npx", "--no-install", "tsc", "--noEmit", "--project", "tsconfig.json"],
                    cwd=root, capture_output=True, text=True, timeout=tsc_timeout_s, check=False)
                typescript_compiled = completed.returncode == 0
                if not typescript_compiled:
                    findings.append(_finding("TSC_FAILED", (completed.stderr or completed.stdout)[-1200:]))
            except (subprocess.TimeoutExpired, OSError) as exc:
                findings.append(_finding("TSC_FAILED", str(exc)))

    render_inspected = False
    if render_file is not None:
        clip = render_file.resolve()
        if not clip.is_file() or clip.suffix.lower() != ".mp4" or clip.stat().st_size < 128:
            findings.append(_finding("RENDER_FILE_INVALID", "MP4 missing/empty/too small"))
        elif shutil.which("ffprobe") is None:
            findings.append(_finding("FFPROBE_UNAVAILABLE", "Cannot verify render metadata"))
        else:
            try:
                done = subprocess.run([
                    "ffprobe", "-v", "error", "-select_streams", "v:0",
                    "-show_entries", "stream=codec_name,width,height,r_frame_rate",
                    "-show_entries", "format=duration",
                    "-of", "json", str(clip)
                ], capture_output=True, text=True, timeout=30, check=False)
                if done.returncode != 0:
                    raise ValueError(done.stderr[-500:] or "ffprobe failed")
                probe = json.loads(done.stdout)
                stream = probe.get("streams", [{}])[0]
                secs = float(probe.get("format", {}).get("duration", 0))
                expected_seconds = props["duration_frames"] / props["fps"]
                if (stream.get("codec_name") != "h264" or stream.get("width") != props["width"]
                    or stream.get("height") != props["height"]
                    or not 0 < secs <= expected_seconds + 0.5
                    or abs(secs-expected_seconds) > max(0.25, 2/props["fps"])):
                    findings.append(_finding("RENDER_METADATA_MISMATCH",
                                             f"Codec/dimensions/duration mismatch ({secs:.3f}s)"))
                else:
                    render_inspected = True
            except (OSError, ValueError, KeyError, IndexError, json.JSONDecodeError, subprocess.TimeoutExpired) as exc:
                findings.append(_finding("RENDER_PROBE_FAILED", str(exc)))

    blockers = [x for x in findings if x["severity"] == "BLOCKER"]
    return {
        "status": "BLOCKED" if blockers else ("REVIEW" if findings else "CONTRACT_ASSETS_CHECKED"),
        "contract_valid": result["status"] == "VALID_CONTRACT",
        "assets_checked": assets_checked, "sources_checked": source_files_checked,
        "typescript_compiled": typescript_compiled,
        "render_inspected": render_inspected,
        "render_requested": render_file is not None,
        "findings": findings, "human_qa_complete": False,
        "publishing_performed": False,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("props_json", type=Path)
    p.add_argument("--project-root", required=True, type=Path)
    p.add_argument("--source", action="append", required=True, type=Path)
    p.add_argument("--render", type=Path)
    p.add_argument("--run-tsc", action="store_true")
    args = p.parse_args()
    try:
        props = json.loads(args.props_json.read_text(encoding="utf-8"))
        result = review(props, project_root=args.project_root,
                        tsx_files=args.source, render_file=args.render,
                        run_tsc=args.run_tsc)
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0 if result["status"] != "BLOCKED" else 1
    except (OSError, ValueError, KeyError, TypeError) as exc:
        print(f"TECH_REVIEW_FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
