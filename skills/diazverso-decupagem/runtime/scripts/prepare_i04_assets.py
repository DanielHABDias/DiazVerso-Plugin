#!/usr/bin/env python3
"""Prepare canonical Nox and an ORIGINAL procedural whoosh for the I04 test.

Runtime/public/ contains only generated test material. No third-party sound,
TTS, network service, publication action or Content Lab dependency.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import shutil
import struct
import wave
from pathlib import Path

SAMPLE_RATE = 48_000
SOUND_SECONDS = 1.2


def verify_nox(repo: Path) -> Path:
    manifest = json.loads((repo / "assets/manifest.json").read_text(encoding="utf-8"))
    entries = [a for a in manifest["assets"] if a["id"] == "brand.nox.canonical"]
    if len(entries) != 1:
        raise ValueError("Expected exactly one canonical Nox in manifest")
    record = entries[0]
    path = repo / record["path"]
    raw = path.read_bytes()
    expected = record["git_blob_sha1"]
    actual = hashlib.sha1(b"blob " + str(len(raw)).encode("ascii") + b"\0" + raw).hexdigest()
    if actual != expected or len(raw) != record["size_bytes"]:
        raise ValueError("Canonical Nox hash or byte length mismatch")
    if raw[:8] != bytes.fromhex("89504e470d0a1a0a") or raw[12:16] != b"IHDR":
        raise ValueError("Nox is not a PNG")
    width, height = struct.unpack_from(">II", raw, 16)
    if (width, height) != (record["dimensions"]["width"], record["dimensions"]["height"]):
        raise ValueError("Canonical Nox dimensions mismatch")
    return path


def build_original_whoosh(path: Path) -> None:
    """Deterministic band-limited noise sweep with a smooth silence envelope."""
    rng = random.Random(88)
    samples = []
    state = 0.0
    count = round(SAMPLE_RATE * SOUND_SECONDS)
    for n in range(count):
        t = n / count
        # Smooth attack / release, never an abrupt click.
        envelope = math.sin(math.pi * t) ** 2
        # Moving low-pass response creates a short sweep without borrowed media.
        alpha = 0.045 + 0.31 * math.sin(math.pi * t) ** 2
        state += alpha * (rng.uniform(-1, 1) - state)
        value = max(-1, min(1, 0.56 * envelope * state))
        samples.append(int(value * 32767))
    path.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(path), "wb") as wav:
        wav.setnchannels(1)
        wav.setsampwidth(2)
        wav.setframerate(SAMPLE_RATE)
        wav.writeframes(struct.pack("<" + "h" * count, *samples))


def prepare(repo: Path, public: Path) -> dict:
    source = verify_nox(repo)
    public.mkdir(parents=True, exist_ok=True)
    destination = public / "i04-nox-canonical.png"
    shutil.copyfile(source, destination)
    whoosh = public / "i04-whoosh-original.wav"
    build_original_whoosh(whoosh)
    (public / "i04-background.svg").write_text("<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 1080 1920\" width=\"1080\" height=\"1920\">\n  <defs>\n    <linearGradient id=\"night\" x1=\"0\" y1=\"0\" x2=\"1\" y2=\"1\">\n      <stop offset=\"0\" stop-color=\"#0b1423\"/>\n      <stop offset=\".55\" stop-color=\"#223857\"/>\n      <stop offset=\"1\" stop-color=\"#0d1728\"/>\n    </linearGradient>\n    <pattern id=\"halftone\" patternUnits=\"userSpaceOnUse\" width=\"36\" height=\"36\">\n      <circle cx=\"18\" cy=\"18\" r=\"2.2\" fill=\"#a3c4fa\" opacity=\".12\"/>\n    </pattern>\n  </defs>\n  <rect width=\"1080\" height=\"1920\" fill=\"url(#night)\"/>\n  <rect width=\"1080\" height=\"1920\" fill=\"url(#halftone)\"/>\n  <path d=\"M-150 1190 L1200 420\" stroke=\"#a3c4fa\" stroke-opacity=\".15\" stroke-width=\"8\"/>\n  <path d=\"M-150 1250 L1200 480\" stroke=\"#a3c4fa\" stroke-opacity=\".08\" stroke-width=\"4\"/>\n</svg>\n", encoding="utf-8")
    return {
        "canonical_nox": source.as_posix(),
        "copied_nox": destination.as_posix(),
        "source_blob_sha1": hashlib.sha1(
            b"blob " + str(source.stat().st_size).encode("ascii") + b"\0" + source.read_bytes()
        ).hexdigest(),
        "whoosh": whoosh.as_posix(),
        "whoosh_source": "original deterministic procedural PCM; no external license",
        "sample_rate": SAMPLE_RATE,
        "seconds": SOUND_SECONDS,
    }


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--repo", type=Path, default=Path(__file__).resolve().parents[4])
    p.add_argument("--public", type=Path, default=Path(__file__).resolve().parents[1] / "public")
    opts = p.parse_args()
    print(json.dumps(prepare(opts.repo.resolve(), opts.public.resolve()), ensure_ascii=False))


if __name__ == "__main__":
    main()
