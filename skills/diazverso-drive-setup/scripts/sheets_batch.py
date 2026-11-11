"""Native Sheets batches with persistent ID ledger and uncertain-response recovery.

No credentials or network. The authorized host executes the returned batch,
reads it back, and serializes ALL writers for this installation. Sheets has no
compare-and-swap: this is deliberately NOT a distributed lock implementation.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import re
from pathlib import Path
from validate_sheet_schema import HEADERS, plan_new_idea
from promotion import plan_promotion


def cells(sheet_id: int, row: int, values: list[str], column: int = 0) -> dict:
    return {"updateCells": {
        "range": {"sheetId": sheet_id, "startRowIndex": row,
                  "endRowIndex": row + 1, "startColumnIndex": column,
                  "endColumnIndex": column + len(values)},
        "rows": [{"values": [{"userEnteredValue": {"stringValue": v}} for v in values]}],
        "fields": "userEnteredValue"}}


def reserve_insert(snapshot: dict, prefix: str, operation_id: str, fields: dict,
                   *, historical_ids: list[str], single_writer: bool = False) -> dict:
    """Reserve ID, persist operation and insert data in ONE atomic API batch.

    snapshot.sheets contains full, fresh rows (header first), sheet_id and
    grid_rows for Ideias, Produções and Config. historical_ids must include
    deleted/promoted IDs when first bootstrapping counters. Never initialize
    counters from only the visible rows of a migrated installation.
    """
    if single_writer is not True or snapshot.get("complete_fresh_read") is not True:
        raise ValueError("Require fresh complete reads and host-enforced single writer")
    if prefix not in {"TF", "VD", "SH"} or not re.fullmatch(r"[A-Za-z0-9_-]{8,80}", operation_id):
        raise ValueError("Invalid prefix or stable operation ID")
    if not isinstance(fields, dict) or not isinstance(historical_ids, list) or any(
        not isinstance(i, str) or not re.fullmatch(r"(?:TF|VD|SH)_\d{4}", i)
        for i in historical_ids
    ):
        raise ValueError("Invalid fields or verified historical IDs")
    sheets = snapshot["sheets"]
    for name in ("Ideias", "Produções", "Config"):
        sheet = sheets[name]
        if type(sheet.get("sheet_id")) is not int or type(sheet.get("grid_rows")) is not int:
            raise ValueError("Native sheet identity and grid size required")
        if sheet["rows"][0][:len(HEADERS[name])] != HEADERS[name]:
            raise ValueError("Header mismatch: " + name)
    config = sheets["Config"]
    entries = {}
    for i, row in enumerate(config["rows"][1:], 1):
        if not row or not any(str(x).strip() for x in row):
            continue
        if not row[0] or row[0] in entries or len(row) < 2:
            raise ValueError("Invalid or duplicate Config key")
        entries[row[0]] = (i, row[1])
    binding = entries.get("CURRENT_SPREADSHEET_ID")
    if not snapshot.get("spreadsheet_id") or not binding or binding[1] != snapshot["spreadsheet_id"]:
        raise ValueError("Config belongs to another spreadsheet; repair cloned bindings first")
    fingerprint = hashlib.sha256(json.dumps(
        [prefix, fields], sort_keys=True, ensure_ascii=False, separators=(",", ":")
    ).encode()).hexdigest()
    key = "OP_" + operation_id
    target_name = "Ideias" if prefix == "TF" else "Produções"
    target = sheets[target_name]
    if key in entries:
        prior = json.loads(entries[key][1])
        if prior.get("fingerprint") != fingerprint:
            raise ValueError("Operation reused with different input")
        matches = [r for r in target["rows"][1:] if r and r[0] == prior.get("id")]
        if len(matches) != 1:
            # Promoted/removed TF must be reconciled by its production origin;
            # never issue another ID on behalf of this same operation.
            return {"status": "REQUIRES_RECONCILIATION", "id": prior.get("id"), "requests": []}
        if prefix != "TF":
            record = dict(zip(HEADERS["Produções"], matches[0]))
            kind = "LONGO" if prefix == "VD" else "SHORT"
            origin = r"(?:^|[\s;])IDEIA_ORIGEM_ID=" + re.escape(fields.get("idea_id", "")) + r"(?=$|[\s;])"
            if record.get("TIPO") != kind or not fields.get("idea_id") or not re.search(origin, record.get("OBSERVAÇÕES", "")):
                return {"status": "REQUIRES_RECONCILIATION", "id": prior.get("id"), "requests": []}
        return {"status": "ALREADY_COMMITTED", "id": prior["id"], "requests": []}
    counter_key = "LAST_ID_" + prefix
    counter = entries.get(counter_key)
    history = [i for i in historical_ids if i.startswith(prefix + "_")]
    if counter:
        if not re.fullmatch(r"\d{1,4}", str(counter[1])):
            raise ValueError("Corrupt high-water counter")
        history.append(f"{prefix}_{int(counter[1]):04d}")
    elif snapshot.get("history_verified_complete") is not True:
        raise ValueError("Counter bootstrap requires verified complete historical IDs")
    if prefix == "TF":
        plan = plan_new_idea(target["rows"], fields, previously_issued_ids=history)
        if plan["status"] != "READY_TO_INSERT":
            return {**plan, "requests": []}
        row = plan["values"]
    else:
        if set(fields) != {"idea_id"}:
            raise ValueError("Promotion accepts only idea_id")
        plan = plan_promotion(sheets["Ideias"]["rows"], target["rows"], fields["idea_id"],
                              "LONGO" if prefix == "VD" else "SHORT",
                              historical_production_ids=history)
        if plan["status"] != "CREATE_PRODUCTION":
            return {**plan, "requests": []}
        row = plan["row"]
    new_id = plan["id"]
    row_index = max((i for i, r in enumerate(target["rows"]) if any(str(v).strip() for v in r)), default=0) + 1
    if row_index >= target["grid_rows"]:
        raise ValueError("Extend target grid with authorization before inserting")
    # Copy safe structure only; never copy another row's data, formula or chips.
    rng = {"sheetId": target["sheet_id"], "startRowIndex": row_index,
           "endRowIndex": row_index + 1, "startColumnIndex": 0, "endColumnIndex": len(row)}
    source = {**rng, "startRowIndex": 1, "endRowIndex": 2}
    requests = [{"copyPaste": {"source": source, "destination": rng, "pasteType": paste}}
                for paste in ("PASTE_FORMAT", "PASTE_DATA_VALIDATION")]
    requests.append(cells(target["sheet_id"], row_index, row))
    config_next = max((i for i, r in enumerate(config["rows"]) if any(str(v).strip() for v in r)), default=0) + 1
    if counter:
        requests.append(cells(config["sheet_id"], counter[0], [str(int(new_id[3:]))], 1))
    else:
        requests.append(cells(config["sheet_id"], config_next,
                              [counter_key, str(int(new_id[3:])), "ID high-water; never decrement"]))
        config_next += 1
    if config_next >= config["grid_rows"]:
        raise ValueError("Config grid full; no partial write permitted")
    value = json.dumps({"id": new_id, "fingerprint": fingerprint}, separators=(",", ":"))
    requests.append(cells(config["sheet_id"], config_next, [key, value, "Idempotency ledger; retain"]))
    return {"status": "READY_FOR_ATOMIC_BATCH", "id": new_id, "row_number": row_index + 1,
            "requests": requests, "readback_required": True,
            "writer_mode": "HOST_SERIALIZED_SINGLE_WRITER", "writes_performed": False}


if __name__ == "__main__":
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("input", type=Path)
    args = p.parse_args()
    print(json.dumps(reserve_insert(**json.loads(args.input.read_text("utf-8"))), ensure_ascii=False))
