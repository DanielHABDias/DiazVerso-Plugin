#!/usr/bin/env python3
"""D07/L06: read-only offline integrity/safety audit of a Diazverso ZIP.

Tests availability of critical packaged media and skills WITHOUT Google Drive,
GitHub or editor integrations. ZIP validity is not proof of actual Remotion
rendering, visual identity, host installation or creator approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import sys
import zipfile
import zlib
from pathlib import Path, PurePosixPath

MAX_TOTAL = 150 * 1024 * 1024
MAX_MEMBER = 30 * 1024 * 1024
REQUIRED = (
    "plugin.json",
    "assets/manifest.json",
    "assets/brand/nox/Nox.png",
    "skills/diazverso-setup/SKILL.md",
    "skills/diazverso-core/SKILL.md",
    "skills/diazverso-nox/SKILL.md",
    "skills/diazverso-decupagem/SKILL.md",
    "skills/diazverso-thumbnail/SKILL.md",
)
EXTERNAL = ("context-optimization", "video-editing", "analyze-video-editing", "find-broll")
PNG_SIG = b"\x89PNG\r\n\x1a\n"


def _png_geometry(data: bytes) -> tuple[int, int]:
    if len(data) < 33 or data[:8] != PNG_SIG:
        raise ValueError("Missing PNG magic")
    if data[8:16] != b"\x00\x00\x00\x0dIHDR":
        raise ValueError("Missing PNG IHDR")
    if zlib.crc32(data[12:29]) != struct.unpack(">I", data[29:33])[0]:
        raise ValueError("Invalid PNG IHDR CRC")
    w, h, depth, color, compression, filt, interlace = struct.unpack(">IIBBBBB",data[16:29])
    if not w or not h or w*h > 20_000_000 or depth != 8 or color not in (2,6) or compression or filt or interlace:
        raise ValueError("Unsupported PNG layout")
    return w, h


def verify(path: Path) -> dict:
    if not path.is_file():
        raise FileNotFoundError("Actual package ZIP missing")
    with zipfile.ZipFile(path, "r") as z:
        members=z.infolist()
        names=[m.filename for m in members]
        if not names or len(names)!=len(set(names)):
            raise ValueError("ZIP empty or duplicate entries")
        compressed_total=0
        for member in members:
            name=member.filename
            pure=PurePosixPath(name)
            if (name.startswith("/") or "\\" in name or pure.is_absolute() or
                ".." in pure.parts or "." in pure.parts or
                any(not component for component in name.split("/")) or
                member.is_dir() or member.file_size > MAX_MEMBER):
                raise ValueError("Unsafe ZIP path/member")
            if (member.external_attr >> 16) & 0o170000 == 0o120000:
                raise ValueError("Symlink in ZIP")
            compressed_total += member.file_size
            if compressed_total > MAX_TOTAL:
                raise ValueError("Uncompressed ZIP too large")
        if z.testzip() is not None:
            raise ValueError("ZIP CRC mismatch")
        missing=[name for name in REQUIRED if name not in names]
        if missing:
            raise ValueError("Critical offline content missing: " + ", ".join(missing))
        for external in EXTERNAL:
            for suffix in ("SKILL.md", "LICENSE"):
                label=f"skills/{external}/{suffix}"
                if label not in names:
                    raise ValueError("Redistributed skill/license missing: "+label)
        plugin=json.loads(z.read("plugin.json"))
        if (plugin.get("name")!="diazverso" or
            plugin.get("extensions",{}).get("com.openai",{}).get("onboardingSkill")
             != "./skills/diazverso-setup/SKILL.md"):
            raise ValueError("Plugin/onboarding manifest mismatch")
        catalog=json.loads(z.read("assets/manifest.json"))
        items=[x for x in catalog.get("assets",[]) if x.get("id")=="brand.nox.canonical"]
        if len(items)!=1:
            raise ValueError("Canonical Nox manifest entry missing/ambiguous")
        item=items[0]
        if item.get("path")!="assets/brand/nox/Nox.png":
            raise ValueError("Noncanonical Nox path")
        png=z.read(item["path"])
        if len(png)!=item.get("size_bytes"):
            raise ValueError("Nox size mismatch")
        blob=hashlib.sha1(b"blob "+str(len(png)).encode()+b"\0"+png).hexdigest()
        if blob!=item.get("git_blob_sha1"):
            raise ValueError("Nox Git blob hash mismatch")
        w,h=_png_geometry(png)
        if {"width":w,"height":h}!=item.get("dimensions"):
            raise ValueError("Nox geometry mismatch")
        # No runtime or account accesses. ZIP contents are proof of local bytes only.
        return {"status":"OFFLINE_MEDIA_AND_PACKAGE_STRUCTURE_VALID",
                "package_sha256":hashlib.sha256(path.read_bytes()).hexdigest(),
                "file_count":len(members),
                "nox":{"size_bytes":len(png),"width":w,"height":h,"git_blob_sha1":blob},
                "critical_paths_present":list(REQUIRED),
                "external_licenses_present":list(EXTERNAL),
                "drive_accessed":False,"runtime_rendered":False,
                "nox_visually_reviewed":False,"host_installed":False,
                "publishing_performed":False}


def main() -> int:
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("zip",type=Path)
    args=parser.parse_args()
    try:
        print(json.dumps(verify(args.zip),ensure_ascii=False,indent=2))
        return 0
    except (OSError,ValueError,KeyError,TypeError,zipfile.BadZipFile,
            json.JSONDecodeError,zlib.error) as exc:
        print("OFFLINE_PACKAGE_AUDIT_FAILED: "+str(exc),file=sys.stderr)
        return 1


if __name__=="__main__":
    raise SystemExit(main())
