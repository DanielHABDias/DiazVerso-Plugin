"""Build deterministic original PCM effects, without samples or external services.

Technical candidates: require listening before editorial approval. No music,
third-party assets or voice. Refuse to overwrite existing files by default.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import math
import random
import struct
import wave
from pathlib import Path

RATE = 48000
SPECS = {"whoosh-short": .28, "whoosh-long": 1.2, "ding": .65,
         "boom": .75, "riser": 1.5}


def samples(kind: str) -> list[int]:
    duration = SPECS[kind]
    rng = random.Random(710 + list(SPECS).index(kind))
    count = round(duration * RATE)
    raw = []
    lowpass = 0.0
    phase = 0.0
    for i in range(count):
        t = i / RATE
        x = i / (count - 1)
        envelope = math.sin(math.pi * x) ** 2
        noise = rng.uniform(-1, 1)
        if kind.startswith("whoosh"):
            alpha = .04 + .35 * envelope
            lowpass += alpha * (noise - lowpass)
            value = envelope * lowpass
        elif kind == "ding":
            value = envelope * math.exp(-4*x) * (
                math.sin(2*math.pi*1046.5*t) + .23*math.sin(2*math.pi*2093*t))
        elif kind == "boom":
            phase += 2*math.pi*(100-65*x) / RATE
            value = envelope * math.exp(-4*x) * (math.sin(phase) + .12*noise)
        else:
            phase += 2*math.pi*(180 + 1600*x*x) / RATE
            value = envelope * (.24*math.sin(phase) + .12*noise)
        raw.append(value)
    peak = max(abs(v) for v in raw)
    return [round(v / peak * .32 * 32767) for v in raw]


def build(output: Path) -> dict:
    output.mkdir(parents=True, exist_ok=True)
    targets = [output / (name + ".wav") for name in SPECS] + [output / "catalog.json"]
    if any(p.exists() for p in targets):
        raise FileExistsError("Refuse to overwrite an existing SFX pack")
    records = []
    for kind, seconds in SPECS.items():
        path = output / (kind + ".wav")
        pcm = samples(kind)
        with wave.open(str(path), "wb") as writer:
            writer.setnchannels(1); writer.setsampwidth(2); writer.setframerate(RATE)
            writer.writeframes(struct.pack("<" + "h" * len(pcm), *pcm))
        data = path.read_bytes()
        rms = math.sqrt(sum(v*v for v in pcm) / len(pcm)) / 32767
        records.append({"id": "sfx.original." + kind, "name": path.name,
            "kind": "sfx", "path": "assets/sfx/" + path.name,
            "mime_type": "audio/wav", "size_bytes": len(data),
            "duration_seconds": seconds, "sample_rate": RATE, "channels": 1,
            "peak_dbfs": round(20*math.log10(max(map(abs, pcm))/32767), 2),
            "rms_dbfs": round(20*math.log10(rms), 2),
            "sha256": hashlib.sha256(data).hexdigest(),
            "git_blob_sha1": hashlib.sha1(b"blob " + str(len(data)).encode() + b"\0" + data).hexdigest(),
            "rights": "ORIGINAL_PROCEDURAL_NO_THIRD_PARTY_SAMPLES",
            "source": "skills/diazverso-decupagem/scripts/build_original_sfx.py",
            "status": "TECHNICAL_CANDIDATE_LISTENING_PENDING"})
    catalog = {"schema": "diazverso-original-sfx-v1", "assets": records,
               "listening_performed": False, "editorially_approved": False}
    (output / "catalog.json").write_text(json.dumps(catalog, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    return catalog


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("output", type=Path)
    args = parser.parse_args()
    print(json.dumps(build(args.output), ensure_ascii=False))
