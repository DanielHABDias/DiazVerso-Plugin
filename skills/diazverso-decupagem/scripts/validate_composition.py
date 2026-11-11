"""composition: validate portable Remotion composition props; stdlib only.

This is a pre-render contract check, NOT a Remotion runtime test. Never
download remote assets, access accounts, publish, or render video.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path


def validate(data: dict) -> dict:
    if not isinstance(data, dict):
        raise ValueError("Composition props must be an object")
    required = {"contract_version", "production_id", "script_version", "format",
                "fps", "width", "height", "duration_frames", "assets", "scenes", "output"}
    if set(data) != required or data["contract_version"] != "1.0":
        raise ValueError("Version or keys do not match composition contract")
    kind = data["format"]
    if kind not in ("SHORT", "LONGO"):
        raise ValueError("Unknown format")
    if not isinstance(data["production_id"], str) or not re.fullmatch(
        r"(?:SH|VD)_\d{4,}", data["production_id"]):
        raise ValueError("Invalid production ID")
    if (kind == "SHORT") != data["production_id"].startswith("SH_"):
        raise ValueError("Production ID and format disagree")
    if not isinstance(data["script_version"], str) or not data["script_version"].strip():
        raise ValueError("Missing approved script version")
    if any(type(data[k]) is not int or data[k] <= 0 for k in ("fps", "width", "height", "duration_frames")):
        raise ValueError("Frame dimensions, FPS and duration must be positive integers")
    if data["fps"] > 120:
        raise ValueError("Unsupported FPS")
    expected = (1080, 1920) if kind == "SHORT" else (1920, 1080)
    if (data["width"], data["height"]) != expected:
        raise ValueError("Output must use exact Diazverso format dimensions")
    output = data["output"]
    if not isinstance(output, dict) or set(output) != {"basename", "container", "video_codec"}:
        raise ValueError("Invalid output configuration")
    if output["container"] != "mp4" or output["video_codec"] != "h264" or not isinstance(output["basename"], str) or not re.fullmatch(r"[a-zA-Z0-9_-]+", output["basename"]):
        raise ValueError("Unsafe or unsupported output")
    assets = data["assets"]
    scenes = data["scenes"]
    if not isinstance(assets, list) or not isinstance(scenes, list) or not scenes:
        raise ValueError("Assets/scenes missing")
    registered = {}
    for asset in assets:
        if not isinstance(asset, dict) or set(asset) != {"id", "path", "kind", "rights"}:
            raise ValueError("Invalid asset descriptor")
        ident, rawpath = asset["id"], asset["path"]
        if not isinstance(ident, str) or not ident or ident in registered:
            raise ValueError("Duplicate or missing asset ID")
        if not isinstance(rawpath, str) or not rawpath or "\\" in rawpath or rawpath.startswith(("/", "~")) or "://" in rawpath:
            raise ValueError("Assets must be local paths in the independent renderer")
        parts = rawpath.split("/")
        if any(p in ("", ".", "..") for p in parts):
            raise ValueError("Unsafe asset relative path")
        if asset["kind"] not in ("image", "video", "audio", "font"):
            raise ValueError("Unsupported asset type")
        if asset["rights"] != "APPROVED":
            raise ValueError("All packaged assets must have approved rights")
        registered[ident] = asset["kind"]
    previous_end, ids = 0, set()
    scene_total = len(scenes)
    for i, scene in enumerate(scenes):
        fields = {"id", "start_frame", "duration_frames", "objective", "visual",
                  "layers", "captions", "audio"}
        if not isinstance(scene, dict) or set(scene) != fields:
            raise ValueError("Scene props invalid")
        sid = scene["id"]
        if not isinstance(sid, str) or not re.fullmatch(r"S\d{2,4}", sid) or sid in ids:
            raise ValueError("Duplicate/invalid scene ID")
        ids.add(sid)
        start, duration = scene["start_frame"], scene["duration_frames"]
        if type(start) is not int or type(duration) is not int or start != previous_end or duration < 1:
            raise ValueError("Scenes must cover timeline contiguously in order")
        previous_end = start + duration
        if not all(isinstance(scene[k], str) and scene[k].strip() for k in ("objective", "visual")):
            raise ValueError("Scene objective/visual required")
        for key in ("layers", "captions", "audio"):
            if not isinstance(scene[key], list):
                raise ValueError(f"{sid}.{key} is not a list")
        for layer in scene["layers"]:
            if not isinstance(layer, dict) or set(layer) != {"asset_id", "motion", "z_index"}:
                raise ValueError("Invalid layer")
            if layer["asset_id"] not in registered or registered[layer["asset_id"]] not in ("image", "video", "font"):
                raise ValueError("Missing or wrong visual asset")
            if layer["motion"] not in ("static", "pan", "zoom", "reframe", "parallax", "kinetic-text") or type(layer["z_index"]) is not int:
                raise ValueError("Invalid motion/layer order")
        for key in ("captions", "audio"):
            for cue in scene[key]:
                expected_keys = {"text", "start_frame", "duration_frames"} if key == "captions" else {"asset_id", "start_frame", "duration_frames", "volume"}
                if not isinstance(cue, dict) or set(cue) != expected_keys:
                    raise ValueError("Invalid timed cue")
                s, d = cue["start_frame"], cue["duration_frames"]
                if type(s) is not int or type(d) is not int or s < 0 or d < 1 or s + d > duration:
                    raise ValueError("Cue outside scene bounds; offsets are scene-relative")
                if key == "captions":
                    if not isinstance(cue["text"], str) or not cue["text"].strip():
                        raise ValueError("Empty caption")
                else:
                    if cue["asset_id"] not in registered or registered[cue["asset_id"]] != "audio":
                        raise ValueError("Unknown/non-audio asset")
                    v = cue["volume"]
                    if type(v) not in (int, float) or not 0 <= v <= 1:
                        raise ValueError("Audio volume out of range")
    if previous_end != data["duration_frames"]:
        raise ValueError("Timeline end does not match output duration")
    return {"status": "VALID_CONTRACT", "scenes": scene_total,
            "assets": len(assets), "duration_frames": previous_end,
            "runtime_render_verified": False, "publishing_performed": False}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("props", type=Path)
    args = parser.parse_args()
    props = json.loads(args.props.read_text(encoding="utf-8"))
    print(json.dumps(validate(props), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
