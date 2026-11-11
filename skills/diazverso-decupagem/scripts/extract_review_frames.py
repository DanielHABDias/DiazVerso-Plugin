#!/usr/bin/env python3
"""J02: extract representative real PNG frames with ffprobe+ffmpeg.

Sampling is deterministic and based on verified H01 scene frames and optional
event frames. Dry run is default. No synthetic pictures, network or posting.
"""
from __future__ import annotations
import argparse
import hashlib
import importlib.util
import json
import re
import shutil
import subprocess
import sys
from pathlib import Path

spec = importlib.util.spec_from_file_location(
    "diazverso_h01_for_frame_extraction", Path(__file__).with_name("validate_composition.py"))
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)

def plan(props: dict, clip: Path, output: Path, events: list[dict] | None = None) -> dict:
    validator.validate(props)
    samples = {}
    max_frame = props["duration_frames"] - 1
    def add(frame: int, reason: str):
        if type(frame) is not int or not 0 <= frame <= max_frame:
            raise ValueError("Frame outside composition")
        samples.setdefault(frame, set()).add(reason)
    for scene in props["scenes"]:
        start = scene["start_frame"]
        end = start + scene["duration_frames"] - 1
        add(start, scene["id"]+":entry")
        add((start + end)//2, scene["id"]+":middle")
        add(end, scene["id"]+":exit")
    if events is not None:
        if not isinstance(events, list):
            raise ValueError("events must be an array")
        for event in events:
            if not isinstance(event, dict) or set(event) != {"frame", "kind"}:
                raise ValueError("Event needs frame and kind")
            if event["kind"] not in ("pose", "transition", "caption", "effect"):
                raise ValueError("Unknown sample event type")
            add(event["frame"], event["kind"])
    if len(samples) > 120:
        raise ValueError("Sampling exceeds 120 images; split the review")
    dst = output.resolve()
    if dst == Path(dst.anchor):
        raise ValueError("Output directory cannot be filesystem root")
    steps = [{"frame": n, "reasons": sorted(why),
              "target": str(dst / f"frame_{n:06d}.png")}
             for n,why in sorted(samples.items())]
    return {"status":"SAMPLING_PLAN","video":str(clip.resolve()),
            "output_dir":str(dst), "duration_frames":props["duration_frames"],
            "width":props["width"],"height":props["height"],"fps":props["fps"],
            "steps":steps,"frames_extracted":False,
            "visual_review_performed":False,"publishing_performed":False}


def extract(planned: dict, timeout_s: int = 45) -> dict:
    if type(timeout_s) is not int or not 1 <= timeout_s <= 600:
        raise ValueError("Invalid ffmpeg timeout")
    src = Path(planned["video"])
    if not src.is_file() or src.suffix.lower() != ".mp4" or src.stat().st_size == 0:
        raise FileNotFoundError("Actual rendered MP4 required")
    if not shutil.which("ffprobe") or not shutil.which("ffmpeg"):
        raise RuntimeError("Installed ffprobe and ffmpeg required")
    try:
        p = subprocess.run(["ffprobe","-v","error","-select_streams","v:0",
            "-show_entries","stream=width,height,avg_frame_rate,nb_frames",
            "-of","json",str(src)], capture_output=True,text=True,
            check=False,timeout=timeout_s)
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError("ffprobe timed out") from exc
    if p.returncode != 0:
        raise RuntimeError("ffprobe failed: "+p.stderr[-500:])
    metadata = json.loads(p.stdout)
    stream = metadata.get("streams",[{}])[0]
    fraction = stream.get("avg_frame_rate","0/1")
    from fractions import Fraction
    try:
        frame_rate = float(Fraction(fraction))
    except (ValueError, ZeroDivisionError) as exc:
        raise RuntimeError("Invalid probed video FPS") from exc
    if (stream.get("width") != planned["width"] or stream.get("height") != planned["height"]
            or abs(frame_rate-planned["fps"]) > 0.02):
        raise RuntimeError("Actual render dimensions/FPS disagree with props")
    num_frames = stream.get("nb_frames")
    if num_frames not in (None, "N/A") and int(num_frames) < planned["duration_frames"]:
        raise RuntimeError("Rendered clip is shorter than planned composition")
    for step in planned["steps"]:
        if Path(step["target"]).exists():
            raise FileExistsError("Refusing to overwrite frame: "+step["target"])
    results=[]
    for step in planned["steps"]:
        output = Path(step["target"])
        output.parent.mkdir(parents=True,exist_ok=True)
        # ffmpeg select(n) indexes decoded frames, rather than relying on VFR seek.
        filter_expression = f"select=eq(n\\,{step['frame']})"
        try:
            p=subprocess.run(["ffmpeg","-nostdin","-v","error","-i",str(src),
                "-vf",filter_expression,"-frames:v","1","-vsync","0","-n",str(output)],
                capture_output=True,text=True,check=False,timeout=timeout_s)
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError("ffmpeg timed out on "+str(step["frame"])) from exc
        if p.returncode != 0 or not output.is_file():
            raise RuntimeError("ffmpeg failed at frame "+str(step["frame"])+": "+p.stderr[-500:])
        payload=output.read_bytes()
        if not payload.startswith(b"\x89PNG\r\n\x1a\n"):
            raise RuntimeError("Extracted frame is not PNG")
        results.append({"frame":step["frame"],"reasons":step["reasons"],
                        "path":str(output),"sha256":hashlib.sha256(payload).hexdigest()})
    return {"status":"FRAMES_EXTRACTED_AWAITING_HUMAN_REVIEW",
        "frames":results,"frames_extracted":True,
        "visual_review_performed":False,"publishing_performed":False}


def main() -> int:
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("--props",type=Path,required=True)
    p.add_argument("--video",type=Path,required=True)
    p.add_argument("--out",type=Path,required=True)
    p.add_argument("--events",type=Path)
    p.add_argument("--execute",action="store_true")
    args=p.parse_args()
    try:
        data=json.loads(args.props.read_text(encoding="utf-8"))
        events=json.loads(args.events.read_text(encoding="utf-8")) if args.events else None
        planned=plan(data,args.video,args.out,events)
        result=extract(planned) if args.execute else planned
        print(json.dumps(result,ensure_ascii=False,indent=2))
        return 0
    except (ValueError,OSError,RuntimeError,KeyError,IndexError,json.JSONDecodeError) as exc:
        print("EXTRACT_FRAMES_FAILED: "+str(exc),file=sys.stderr)
        return 1

if __name__=="__main__":
    raise SystemExit(main())
