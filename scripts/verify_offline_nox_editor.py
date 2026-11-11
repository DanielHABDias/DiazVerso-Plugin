#!/usr/bin/env python3
"""Developer-only offline image-editor smoke for canonical Diazverso Nox.

Requires Pillow in the test environment, not in the plugin installation.
Checks real pixels and creates 16:9/9:16 frames without Drive or network.
Not a Remotion/MP4 render, React test or full ZIP audit.
"""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path
from PIL import Image


def verify(asset: Path, manifest: Path, out: Path) -> dict:
    info = json.loads(manifest.read_text("utf-8"))
    entries = [a for a in info.get("assets", []) if a.get("id") == "brand.nox.canonical"]
    if len(entries) != 1:
        raise ValueError("Canonical Nox entry missing or duplicated")
    expected = entries[0]
    if expected.get("path") != "assets/brand/nox/Nox.png":
        raise ValueError("Unexpected canonical path")
    raw = asset.read_bytes()
    blob = hashlib.sha1(b"blob " + str(len(raw)).encode() + b"\0" + raw).hexdigest()
    if len(raw) != expected.get("size_bytes") or blob != expected.get("git_blob_sha1"):
        raise ValueError("Original Nox bytes disagree with manifest")
    with Image.open(asset) as read:
        read.load()
        original = read.convert("RGBA")
    dims = expected.get("dimensions", {})
    if original.size != (dims.get("width"), dims.get("height")):
        raise ValueError("Original Nox dimensions disagree with manifest")
    bbox = original.getchannel("A").getbbox()
    if not bbox:
        raise ValueError("Original Nox is fully transparent")
    cropped = original.crop(bbox)
    out.mkdir(parents=True, exist_ok=True)
    proof = []
    for label, size in [("16x9", (1920, 1080)), ("9x16", (1080, 1920))]:
        width, height = size
        bg = (17, 24, 39)
        image = Image.new("RGB", size, bg)
        ratio = min(width * .55 / cropped.width, height * .77 / cropped.height)
        character = cropped.resize((round(cropped.width * ratio),
                                    round(cropped.height * ratio)), Image.Resampling.LANCZOS)
        image.paste(character, ((width - character.width) // 2,
                                (height - character.height) // 2), character)
        result = out / f"nox-offline-{label}.png"
        image.save(result, optimize=True)
        with Image.open(result) as reread:
            reread.load()
            if reread.size != size or reread.getpixel((width//2, height//2)) == bg:
                raise ValueError(f"Offline composition failed: {label}")
        proof.append({"format": label, "width": width, "height": height,
                      "path": str(result), "sha256": hashlib.sha256(result.read_bytes()).hexdigest()})
    return {"status": "OFFLINE_IMAGE_EDITOR_PASS",
            "canonical_sha256": hashlib.sha256(raw).hexdigest(),
            "canonical_bounds": list(bbox), "frames": proof,
            "drive_accessed": False, "remotion_rendered": False, "published": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--asset", type=Path, required=True)
    p.add_argument("--manifest", type=Path, required=True)
    p.add_argument("--out", type=Path, required=True)
    args = p.parse_args()
    print(json.dumps(verify(args.asset, args.manifest, args.out), indent=2))


if __name__ == "__main__":
    main()
