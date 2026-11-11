#!/usr/bin/env python3
"""E02: pure, read-only resolver for paginated Google Drive folder listings.

Consumes JSON metadata returned by an authorized Drive adapter. It NEVER calls
Google APIs or creates folders. See ../references/deteccao-idempotente.md.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Mapping

FOLDER = "application/vnd.google-apps.folder"
SHEET = "application/vnd.google-apps.spreadsheet"
REQUIRED = {
    "Roteiros": FOLDER,
    "Thumbnails": FOLDER,
    "Canal do YT — V1.0 (Diazverso)": SHEET,
}
SUBFOLDERS = {"Longos": FOLDER, "Shorts": FOLDER}
OPTIONAL = {"Assets", "Backgrounds", "Memes", "Músicas", "Sounds"}


def _items(page: Mapping[str, Any]) -> list[dict[str, Any]]:
    if "results" in page:
        entries = page["results"]
    elif "result" in page and isinstance(page["result"], dict):
        entries = page["result"].get("results", [])
    else:
        entries = page.get("files", [])
    if not isinstance(entries, list):
        raise ValueError("Uma página deve conter uma lista results/files")
    return entries


def _name(item: Mapping[str, Any]) -> str | None:
    return item.get("name") or item.get("title")


def _mime(item: Mapping[str, Any]) -> str | None:
    return item.get("mimeType") or item.get("mime_type")


def _parents(item: Mapping[str, Any]) -> list[str]:
    value = item.get("parents", item.get("parent_ids", []))
    return value if isinstance(value, list) else []


def _records(pages: list[Mapping[str, Any]], parent: str | None,
             *, complete: bool) -> list[dict[str, Any]]:
    if not complete:
        raise ValueError("Listagem incompleta: resolver next_page_token antes de decidir")
    result: dict[str, dict[str, Any]] = {}
    for page in pages:
        if page.get("next_page_token") or page.get("nextPageToken"):
            raise ValueError("Listagem paginada ainda tem próxima página")
        for item in _items(page):
            if not isinstance(item, dict):
                raise ValueError("Metadado de arquivo inválido")
            fid = item.get("id")
            if not isinstance(fid, str) or not fid:
                continue
            if item.get("trashed", False):
                continue
            if parent is not None and parent not in _parents(item):
                continue
            result[fid] = item
    return list(result.values())


def _choose(items: list[dict[str, Any]], name: str, mime: str,
            preferred_id: str | None = None) -> dict[str, Any]:
    found = [i for i in items if _name(i) == name and _mime(i) == mime]
    if preferred_id:
        selected = [i for i in found if i["id"] == preferred_id]
        if len(selected) == 1:
            return {"status": "EXISTS", "id": selected[0]["id"]}
        return {"status": "CONFIG_ID_INVALID", "candidates": [i["id"] for i in found]}
    if not found:
        return {"status": "MISSING"}
    if len(found) == 1:
        return {"status": "EXISTS", "id": found[0]["id"]}
    return {"status": "AMBIGUOUS", "candidates": sorted(i["id"] for i in found)}


def discover(snapshot: Mapping[str, Any]) -> dict[str, Any]:
    """Resolve one installation; no missing item is created or silently selected.

    Input snapshot:
      root_pages: [metadata page(s) with root candidates]
      children: {parent_id: [page(s) directly in that folder]}
      complete: {parent_id or 'roots': bool}
      preferred_root_id: optional, verified by exact name and type
      preferred_ids: optional {canonical relative path: current installation id}

    Adapter must paginate to exhaustion. Ambiguity blocks all downstream writes.
    """
    complete = snapshot.get("complete", {})
    if not isinstance(complete, dict):
        raise ValueError("complete deve ser um objeto")
    roots = _records(snapshot.get("root_pages", []), parent=None,
                     complete=complete.get("roots", False))
    # Name and MIME plus a trusted installation ID, if supplied; never accept
    # a stale ID just because it appears in the search response.
    root = _choose(roots, "Diazverso", FOLDER, snapshot.get("preferred_root_id"))
    output: dict[str, Any] = {"root": root, "folders": {}, "missing": [],
                              "ambiguous": [], "writes_performed": False}
    if root["status"] != "EXISTS":
        output["status"] = "BLOCKED" if root["status"] != "MISSING" else "ROOT_MISSING"
        return output
    root_id = root["id"]
    children = snapshot.get("children", {})
    preferred = snapshot.get("preferred_ids", {})
    if not isinstance(children, dict) or not isinstance(preferred, dict):
        raise ValueError("children/preferred_ids devem ser objetos")

    def walk(parent_id: str, prefix: str, expected: Mapping[str, str]) -> None:
        pages = children.get(parent_id)
        if pages is None:
            raise ValueError(f"Listagem não fornecida para {prefix or 'Diazverso'}")
        entries = _records(pages, parent=parent_id, complete=complete.get(parent_id, False))
        for name, mime in expected.items():
            key = f"{prefix}/{name}" if prefix else name
            selected = _choose(entries, name, mime, preferred.get(key))
            output["folders"][key] = selected
            if selected["status"] == "MISSING":
                output["missing"].append(key)
            elif selected["status"] != "EXISTS":
                output["ambiguous"].append(key)
            if name in ("Roteiros", "Thumbnails") and selected["status"] == "EXISTS":
                walk(selected["id"], key, SUBFOLDERS)

    root_expected = {**REQUIRED, **{name: FOLDER for name in sorted(OPTIONAL)}}
    walk(root_id, "", root_expected)
    output["status"] = ("BLOCKED" if output["ambiguous"]
                        else "INCOMPLETE" if output["missing"] else "COMPLETE")
    return output


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="JSON da listagem de Drive já paginada")
    args = parser.parse_args()
    value = json.loads(args.snapshot.read_text(encoding="utf-8"))
    print(json.dumps(discover(value), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
