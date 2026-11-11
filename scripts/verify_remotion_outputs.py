#!/usr/bin/env python3
"""Verify locally rendered Remotion test frames and MP4 video geometry.

Uses only Python stdlib: reads PNG IHDR+CRC and ISO BMFF moov/trak/tkhd.
This is a smoke verifier, not content/legibility QA or a full video decoder.
"""
from __future__ import annotations
import argparse
import struct
import zlib
from pathlib import Path

DIMENSIONS = {"16x9": (1920, 1080), "9x16": (1080, 1920)}
PNG_MAGIC = bytes.fromhex("89504e470d0a1a0a")


def boxes(data: bytes, begin: int, end: int):
    pos = begin
    while pos + 8 <= end:
        size, kind = struct.unpack_from(">I4s", data, pos)
        header = 8
        if size == 1:
            if pos + 16 > end:
                raise ValueError("Truncated extended MP4 box")
            size = struct.unpack_from(">Q", data, pos + 8)[0]
            header = 16
        elif size == 0:
            size = end - pos
        if size < header or pos + size > end:
            raise ValueError("Invalid MP4 box length")
        yield kind, pos + header, pos + size
        pos += size
    if pos != end:
        raise ValueError("Unaligned MP4 box data")


def video_dimensions(path: Path) -> tuple[int, int]:
    data = path.read_bytes()
    if len(data) < 120 or not any(k == b"ftyp" for k, _, _ in boxes(data, 0, len(data))):
        raise ValueError("Missing valid MP4 file type")
    for typ, start, end in boxes(data, 0, len(data)):
        if typ != b"moov":
            continue
        for track, ts, te in boxes(data, start, end):
            if track != b"trak":
                continue
            for box, bs, be in boxes(data, ts, te):
                if box == b"tkhd" and be - bs >= 84:
                    width_fixed, height_fixed = struct.unpack_from(">II", data, be - 8)
                    width, height = width_fixed >> 16, height_fixed >> 16
                    if width > 0 and height > 0:
                        return width, height
    raise ValueError("No video track geometry in MP4")


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as f:
        header = f.read(33)
    if len(header) != 33 or header[:8] != PNG_MAGIC or header[8:16] != b"\0\0\0\rIHDR":
        raise ValueError("PNG missing signature/IHDR")
    if zlib.crc32(header[12:29]) != struct.unpack_from(">I", header, 29)[0]:
        raise ValueError("PNG bad IHDR checksum")
    return struct.unpack_from(">II", header, 16)


def verify_folder(folder: Path) -> list[str]:
    results = []
    for kind, expected in DIMENSIONS.items():
        still = folder / f"smoke-{kind}.png"
        clip = folder / f"smoke-{kind}.mp4"
        hq = folder / f"hq-migration-{kind}.png"
        for path, read_dimensions in ((still, png_dimensions), (clip, video_dimensions), (hq, png_dimensions)):
            if not path.is_file() or path.stat().st_size < 100:
                raise ValueError(f"Missing or empty render: {path}")
            actual = read_dimensions(path)
            if actual != expected:
                raise ValueError(f"Unexpected dimensions {path}: {actual}, expected {expected}")
            results.append(f"RENDER_VERIFIED {path.name}: {actual[0]}x{actual[1]}")
    return results


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("folder", type=Path)
    args = p.parse_args()
    for line in verify_folder(args.folder):
        print(line)


if __name__ == "__main__":
    main()
