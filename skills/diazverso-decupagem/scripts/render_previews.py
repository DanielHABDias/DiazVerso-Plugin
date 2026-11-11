#!/usr/bin/env python3
"""H08: render scene excerpts and 3 still previews with an independent Remotion CLI.

Explicit --execute is required. The script does NOT render the final film,
publish to YouTube, download assets or claim visual QA. It records outputs and
failures; a human must inspect previews before any full render.
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

VALIDATOR_PATH = Path(__file__).with_name("validate_composition.py")
_spec = importlib.util.spec_from_file_location("diazverso_validate_composition", VALIDATOR_PATH)
_validator = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_validator)


def _slug(value: str) -> str:
    if not re.fullmatch(r"[a-zA-Z0-9_-]+", value):
        raise ValueError("Composition ID contains unsafe characters")
    return value


def build_plan(props: dict, props_path: Path, entrypoint: Path,
               composition_id: str, output_dir: Path, *, project_root: Path | None = None) -> dict:
    """Return deterministic commands. No writes or process execution."""
    _validator.validate(props)
    _slug(composition_id)
    if not isinstance(entrypoint, Path) or entrypoint.suffix not in (".ts", ".tsx", ".js", ".jsx"):
        raise ValueError("Remotion entrypoint must be a source code file")
    props_path = props_path.resolve()
    entrypoint = entrypoint.resolve()
    output_dir = output_dir.resolve()
    project_root = (project_root or entrypoint.parent).resolve()
    if output_dir == Path(output_dir.anchor):
        raise ValueError("Refusing to output to filesystem root")
    scenes = []
    for scene in props["scenes"]:
        start = scene["start_frame"]
        end = start + scene["duration_frames"] - 1
        stem = f'{props["production_id"]}_{scene["id"]}_{start}-{end}'
        mp4 = output_dir / (stem + ".mp4")
        remotion = ["npx", "--no-install", "remotion"]
        shared = [str(entrypoint), composition_id]
        segments = [
            {
                "kind": "scene_clip",
                "start_frame": start, "end_frame": end,
                "output": str(mp4),
                "command": remotion + ["render"] + shared + [
                    str(mp4), f"--props={props_path}",
                    f"--frames={start}-{end}", "--codec=h264",
                    "--overwrite=false",
                ],
            }
        ]
        distinct = sorted({start, start + (end-start)//2, end})
        for frame in distinct:
            png = output_dir / f"{stem}_f{frame:06d}.png"
            segments.append({
                "kind": "preview_still", "frame": frame,
                "output": str(png),
                "command": remotion + ["still"] + shared + [
                    str(png), f"--props={props_path}", f"--frame={frame}",
                    "--overwrite=false",
                ],
            })
        scenes.append({
            "scene_id": scene["id"],
            "range": [start, end],
            "steps": segments,
        })
    return {
        "status": "READY_TO_EXECUTE", "scene_count": len(scenes),
        "project_root": str(project_root),
        "scenes": scenes, "writes_performed": False,
        "render_verified": False, "visual_qa_verified": False,
        "final_render_performed": False, "publishing_performed": False,
    }


def execute_plan(plan: dict, *, timeout_s: int = 180) -> dict:
    """Run only known planned CLI commands; stop immediately on first failure."""
    if type(timeout_s) is not int or not 1 <= timeout_s <= 1800:
        raise ValueError("Render timeout must be 1..1800 seconds")
    project_root = Path(plan["project_root"])
    if not project_root.is_dir():
        raise FileNotFoundError("Independent Remotion project root missing")
    if shutil.which("npx") is None:
        raise RuntimeError("Node/npx missing; no render attempted")
    actions = [step for scene in plan["scenes"] for step in scene["steps"]]
    for step in actions:
        cmd = step["command"]
        if cmd[:3] != ["npx", "--no-install", "remotion"]:
            raise ValueError("Only the pinned local Remotion CLI is allowed")
        if Path(step["output"]).exists():
            raise FileExistsError(f"Refusing to replace existing output: {step['output']}")
    outputs = []
    for step in actions:
        target = Path(step["output"])
        target.parent.mkdir(parents=True, exist_ok=True)
        try:
            proc = subprocess.run(step["command"], capture_output=True, cwd=str(project_root),
                                  text=True, timeout=timeout_s, check=False)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"Render timeout for {step['kind']} {target.name}") from exc
        if proc.returncode != 0 or not target.is_file() or target.stat().st_size == 0:
            raise RuntimeError(
                f"Render failed for {step['kind']} {target.name}; "
                f"exit={proc.returncode}; stderr={proc.stderr[-1200:]}"
            )
        outputs.append({"kind": step["kind"], "output": str(target),
                        "size_bytes": target.stat().st_size})
    return {
        "status": "PREVIEWS_RENDERED_AWAITING_HUMAN_REVIEW",
        "outputs": outputs, "writes_performed": True,
        "render_verified": True,
        "visual_qa_verified": False, "final_render_performed": False,
        "publishing_performed": False,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--props", required=True, type=Path, help="H01 composition JSON")
    parser.add_argument("--entrypoint", required=True, type=Path, help="Independent Remotion entry .tsx")
    parser.add_argument("--composition-id", required=True)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument("--project-root", type=Path,
                        help="Remotion independent project directory, required with --execute")
    parser.add_argument("--execute", action="store_true",
                        help="Run local Remotion; default is safe dry-run plan")
    args = parser.parse_args()
    try:
        if not args.props.is_file():
            raise FileNotFoundError("Props JSON missing")
        if args.execute and args.project_root is None:
            raise ValueError("--execute requires --project-root")
        if args.execute and not args.entrypoint.is_file():
            raise FileNotFoundError("Independent Remotion entrypoint missing")
        props = json.loads(args.props.read_text(encoding="utf-8"))
        plan = build_plan(props, args.props, args.entrypoint, args.composition_id,
                          args.out, project_root=args.project_root)
        result = execute_plan(plan) if args.execute else plan
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 0
    except (ValueError, OSError, RuntimeError, KeyError) as exc:
        print(f"PREVIEW_FAILED: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())
