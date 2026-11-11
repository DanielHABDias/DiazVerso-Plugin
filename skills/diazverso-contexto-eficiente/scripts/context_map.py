#!/usr/bin/env python3
"""Experimental M01 local graph: scoped paths, links and change-aware metadata.

No network, LLM, subprocess, credentials, or automatic installation. This is
an evaluation aid, NOT evidence of token savings or a Work host capability.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
from pathlib import Path

VERSION = 1
EXTENSIONS = {".md", ".py", ".json", ".yaml", ".yml", ".ts", ".tsx", ".js", ".mjs"}
SKIP_PARTS = {"node_modules", "__pycache__", ".git", ".venv", "dist", "build", ".diazverso-cache"}
MAX_BYTES = 250_000
LINK = re.compile(
    r"(?<![\w./-])((?:\.\./|\./)?(?:skills|docs|schemas|templates|assets|references|scripts|tests)"
    r"/[\w./-]+\.(?:md|py|json|yaml|yml|ts|tsx|js|mjs|png))"
)


def safe_files(root: Path, include_docs: bool = False) -> list[Path]:
    roots = [root / n for n in ("skills", "schemas", "templates")]
    if include_docs:
        roots.append(root / "docs")
    files = [root / "plugin.json", root / "assets" / "manifest.json"]
    for anchor in roots:
        if anchor.is_dir() and not anchor.is_symlink():
            files.extend(p for p in anchor.rglob("*") if p.is_file())
    selected = []
    for p in files:
        if not p.is_file() or p.is_symlink() or p.suffix not in EXTENSIONS:
            continue
        if any(part in SKIP_PARTS or part.startswith(".") for part in p.relative_to(root).parts):
            continue
        if p.stat().st_size > MAX_BYTES:
            continue
        if p.resolve().is_relative_to(root.resolve()):
            selected.append(p)
    return sorted(set(selected))


def parse_node(root: Path, file: Path, digest: str, content: str) -> dict:
    lines = content.splitlines()
    headings = [{"line": i, "text": line.lstrip("# ").strip()[:140]}
                for i, line in enumerate(lines, 1)
                if line.startswith("# ") or line.startswith("## ")][:8]
    description = next((line.strip().strip('"')[:180] for line in lines[:12]
                        if line.startswith("description:")), "")
    references = []
    for num, line in enumerate(lines, 1):
        for hit in LINK.finditer(line):
            target = hit.group(1)
            candidates = (root / target, file.parent / target)
            dest = next((p for p in candidates
                         if p.resolve().is_relative_to(root.resolve())
                         and p.is_file() and not p.is_symlink()), None)
            if dest is not None:
                references.append({"target": dest.relative_to(root).as_posix(),
                                   "line": num, "evidence": "EXTRACTED"})
    return {"sha256": digest, "title": headings[0]["text"] if headings else file.stem,
            "description": description, "headings": headings, "references": references}


def build(root: Path, old: dict | None = None, include_docs: bool = False) -> dict:
    root = root.resolve()
    old = old if isinstance(old, dict) and old.get("schema_version") == VERSION else {}
    scope = "with-docs" if include_docs else "runtime"
    project = hashlib.sha256(str(root).encode()).hexdigest()[:16]
    can_reuse = old.get("project_key") == project and old.get("scope") == scope
    previous = old.get("nodes", {}) if can_reuse else {}
    nodes = {}
    parsed = reused = 0
    for file in safe_files(root, include_docs):
        rel = file.relative_to(root).as_posix()
        data = file.read_bytes()
        digest = hashlib.sha256(data).hexdigest()
        if rel in previous and previous[rel].get("sha256") == digest:
            nodes[rel] = previous[rel]
            reused += 1
        else:
            nodes[rel] = parse_node(root, file, digest, data.decode("utf-8", errors="replace"))
            parsed += 1
    return {"schema_version": VERSION, "project_key": project, "scope": scope,
            "nodes": nodes, "stats": {"files": len(nodes), "parsed": parsed,
                                     "reused": reused,
                                     "removed": len(set(previous) - set(nodes))}}


def find(graph: dict, query: str, limit: int = 8) -> list[dict]:
    terms = [term for term in re.findall(r"[\w-]+", query.casefold()) if len(term) > 1]
    if not terms:
        return []
    found = []
    for path, item in graph["nodes"].items():
        haystack = " ".join([path, item["title"], item["description"]] +
                            [h["text"] for h in item["headings"]]).casefold()
        score = sum(3 if term in path.casefold() else 1
                    for term in terms if term in haystack)
        if score:
            found.append((score, path, {"path": path, "title": item["title"],
                                        "headings": item["headings"][:3],
                                        "references": [ref for ref in item["references"]
                                                       if ref["target"] in graph["nodes"]][:6]}))
    found.sort(key=lambda entry: (-entry[0], entry[1]))
    return [entry[2] for entry in found[:max(1, min(limit, 12))]]


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--root", type=Path, default=Path.cwd())
    p.add_argument("--index", type=Path, help="Optional LOCAL JSON cache path; do not commit")
    p.add_argument("--include-docs", action="store_true", help="Opt in to development docs")
    p.add_argument("--query", help="Bounded search through metadata, titles and headings")
    args = p.parse_args()
    old = {}
    if args.index and args.index.is_file():
        try:
            old = json.loads(args.index.read_text(encoding="utf-8"))
        except (ValueError, OSError):
            old = {}
    result = build(args.root, old, args.include_docs)
    if args.index:
        args.index.parent.mkdir(parents=True, exist_ok=True)
        args.index.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    response = {"stats": result["stats"], "scope": result["scope"],
                "matches": find(result, args.query) if args.query else []}
    print(json.dumps(response, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
