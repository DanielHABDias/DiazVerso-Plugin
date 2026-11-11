#!/usr/bin/env python3
"""discovery: pure, read-only resolver for paginated Google Drive folder listings.

Consumes JSON metadata returned by an authorized Drive adapter. It NEVER calls
Google APIs or creates folders. See ../references/deteccao-idempotente.md.
"""
from __future__ import annotations

import argparse
import json
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
    if not pages:
        raise ValueError("Nenhuma página fornecida: ausência de resultados não comprovada")
    last = pages[-1]
    if last.get("next_page_token") or last.get("nextPageToken"):
        raise ValueError("Listagem paginada ainda tem próxima página")
    for page in pages:
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
    output: dict[str, Any] = {"root": root, "folders": {}, "missing": [], "optional_missing": [],
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
                (output["optional_missing"] if key in OPTIONAL else output["missing"]).append(key)
            elif selected["status"] != "EXISTS":
                output["ambiguous"].append(key)
            if name in ("Roteiros", "Thumbnails") and selected["status"] == "EXISTS":
                walk(selected["id"], key, SUBFOLDERS)

    root_expected = {**REQUIRED, **{name: FOLDER for name in sorted(OPTIONAL)}}
    walk(root_id, "", root_expected)
    output["status"] = ("BLOCKED" if output["ambiguous"]
                        else "INCOMPLETE" if output["missing"] else "COMPLETE")
    return output



def plan_repairs(result: Mapping[str, Any], *, include_optional: bool = False) -> dict[str, Any]:
    """provisioning: produce a no-write creation plan for verified MISSING folders only.

    Actions are proposals, NOT authorizations. Caller must re-read the exact
    parent folder immediately before any authorized create, then read back the
    created ID and resume discovery. Existing sheets are never overwritten.
    """
    status = result.get("status")
    root = result.get("root", {})
    if root.get("status") != "EXISTS":
        return {"status": "BLOCKED", "reason": "Selecionar/validar raiz e pai antes de criar", "actions": []}
    if status == "BLOCKED" or result.get("ambiguous"):
        return {"status": "BLOCKED", "reason": "Resolver caminhos ambíguos e IDs inválidos", "actions": []}
    if status not in ("COMPLETE", "INCOMPLETE"):
        return {"status": "BLOCKED", "reason": "Descoberta não validada", "actions": []}
    folders = result.get("folders", {})
    proposed = list(result.get("missing", []))
    if include_optional:
        proposed.extend(result.get("optional_missing", []))
    actions = []
    deferred = []
    for key in proposed:
        item = folders.get(key)
        if not item or item.get("status") != "MISSING":
            raise ValueError(f"Estado inconsistente no caminho {key}")
        parent_path, _, name = key.rpartition("/")
        parent = folders.get(parent_path) if parent_path else root
        if not parent or parent.get("status") != "EXISTS":
            deferred.append(key)
            continue
        if key == "Canal do YT — V1.0 (Diazverso)":
            # Creating a native spreadsheet needs the proper Sheets/Drive
            # workflow, including schema sheet-schema; do not create a blank file.
            deferred.append(key)
            continue
        actions.append({"operation": "CREATE_FOLDER_IF_STILL_MISSING",
                        "path": key, "name": name, "parent_id": parent["id"],
                        "requires_authorization": True, "requires_readback": True})
    return {"status": "READY_FOR_AUTHORIZATION" if actions else "NO_FOLDER_ACTIONS",
            "actions": actions, "deferred": deferred, "writes_performed": False}



def preflight_folder_create(action: Mapping[str, Any], *, fresh_parent: Mapping[str, Any],
                            authorized: bool = False) -> dict[str, Any]:
    """provisioning: fail-closed just-in-time readback before a folder create.

    This function never writes. Its caller must independently authenticate that
    fresh_parent metadata came from a new complete Drive listing.
    """
    if not isinstance(action, dict) or set(action) != {
            "operation", "path", "name", "parent_id", "requires_authorization",
            "requires_readback"}:
        raise ValueError("Formato de ação provisioning inválido")
    if (action["operation"] != "CREATE_FOLDER_IF_STILL_MISSING" or
        action["requires_authorization"] is not True or
        action["requires_readback"] is not True):
        raise ValueError("Ação não autorizável")
    if not isinstance(action["name"], str) or not action["name"].strip():
        raise ValueError("Nome de pasta inválido")
    if not isinstance(action["parent_id"], str) or not action["parent_id"]:
        raise ValueError("Pai ausente")
    if not isinstance(action["path"], str) or action["path"].split("/")[-1] != action["name"]:
        raise ValueError("Caminho de pasta incoerente")
    if not isinstance(fresh_parent, dict) or set(fresh_parent) != {
            "parent_id", "parent_mime", "complete", "new_read", "pages"}:
        raise ValueError("Metadados de releitura do pai incompletos")
    if (fresh_parent["parent_id"] != action["parent_id"] or
        fresh_parent["parent_mime"] != FOLDER or
        fresh_parent["new_read"] is not True):
        return {"status": "BLOCKED_PARENT_NOT_VERIFIED",
                "reason": "Conferir pai exato em nova leitura", "writes_performed": False}
    entries = _records(fresh_parent["pages"], parent=action["parent_id"],
                       complete=fresh_parent["complete"])
    # Any same-name object blocks: creating another with the same name could
    # shadow a file, wrong-MIME item or folder from a concurrent writer.
    collisions = [item for item in entries if _name(item) == action["name"]]
    if collisions:
        return {"status": "BLOCKED_ALREADY_EXISTS_OR_CONFLICT",
                "existing_ids": [item["id"] for item in collisions],
                "writes_performed": False}
    if authorized is not True:
        return {"status": "AWAITING_EXPLICIT_AUTHORIZATION",
                "writes_performed": False}
    return {"status": "SAFE_TO_ATTEMPT_CREATE_NOW", "parent_id": action["parent_id"],
            "name": action["name"], "expected_mime": FOLDER,
            "writes_performed": False,
            "mandatory_after_action": "Verificar ID/nome/MIME/pai por readback e redescobrir antes da próxima criação"}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path, help="JSON da listagem de Drive já paginada")
    parser.add_argument("--plan", action="store_true", help="Exibir plano provisioning sem executar escrita")
    parser.add_argument("--include-optional", action="store_true", help="Planejar também bibliotecas opcionais")
    args = parser.parse_args()
    value = json.loads(args.snapshot.read_text(encoding="utf-8"))
    result = discover(value)
    if args.plan:
        result = plan_repairs(result, include_optional=args.include_optional)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
