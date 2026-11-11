#!/usr/bin/env python3
"""E04: non-destructive validation of existing Diazverso Google Sheets metadata.

Input is a JSON snapshot made by an authorized connector:
{"sheets":[{"properties":{"title":"Produções","hidden":false,
"gridProperties":{"frozenRowCount":1}}}], "headers":{"Produções":[...]}}
The tool does not access accounts, create sheets, or modify cell contents.
"""
from __future__ import annotations
import argparse
import json
from pathlib import Path

HEADERS = {
    "Produções": ["ID","TIPO","TEMA / CONTEXTO","STATUS","PRIORIDADE","TÍTULO A","TÍTULO B","THUMBNAIL A","THUMBNAIL B","ROTEIRO","VÍDEO RELACIONADO","PLANEJADO PARA","PUBLICADO EM","LINK YOUTUBE","REVISÃO","OBSERVAÇÕES","KIT PUBLICAÇÃO"],
    "Ideias": ["ID","TEMA","TESE / CONTEXTO","TÍTULO PROVISÓRIO","IDEIA DE THUMB","POR QUE VALE","PRIORIDADE","TIMING / CONTEXTO","ORIGEM","STATUS","PRODUÇÃO VINCULADA","OBSERVAÇÕES"],
    "Afiliados": ["ID","PRODUTO / SERVIÇO","CATEGORIA","PLATAFORMA","LINK AFILIADO","APLICÁVEL A","STATUS","ÚLTIMA VERIFICAÇÃO","FONTE","OBSERVAÇÕES"],
    "Config": ["CHAVE","VALOR","DESCRIÇÃO"],
}


def validate(snapshot: dict) -> dict:
    if not isinstance(snapshot.get("sheets"), list) or not isinstance(snapshot.get("headers"), dict):
        raise ValueError("São necessários metadados de abas e cabeçalhos lidos da planilha")
    title_to_props = {}
    for sheet in snapshot["sheets"]:
        props = sheet.get("properties", {})
        title = props.get("title")
        if title in title_to_props:
            raise ValueError(f"Aba duplicada nos metadados: {title}")
        if title:
            title_to_props[title] = props
    issues = []
    for name, expected in HEADERS.items():
        props = title_to_props.get(name)
        if props is None:
            issues.append({"sheet": name, "issue": "MISSING_TAB", "action": "Propor criação com autorização; não substituir aba existente"})
            continue
        actual = snapshot["headers"].get(name)
        if not isinstance(actual, list) or not actual:
            issues.append({"sheet": name, "issue": "HEADER_NOT_READ", "action": "Ler a linha 1 antes de qualquer reparo"})
        elif actual[:len(expected)] != expected:
            issues.append({"sheet": name, "issue": "HEADER_MISMATCH", "expected": expected,
                           "actual": actual, "action": "Revisão humana: não sobrescrever cabeçalhos com dados"})
        grid = props.get("gridProperties", {})
        if grid.get("frozenRowCount", 0) < 1:
            issues.append({"sheet": name, "issue": "HEADER_NOT_FROZEN",
                           "action": "Opcional: congelar primeira linha após autorização"})
        if name == "Config" and not props.get("hidden", False):
            issues.append({"sheet": name, "issue": "CONFIG_VISIBLE",
                           "action": "Propor ocultação após autorização, sem apagar valores"})
    return {"status": "VALID" if not issues else "NEEDS_ATTENTION", "issues": issues,
            "writes_performed": False, "checked_tabs": list(HEADERS)}



def plan_new_idea(rows: list[list], fields: dict, *, previously_issued_ids: list[str]) -> dict:
    """E05: prepare exactly one row; caller owns write and live readback.

    Full current Ideias rows AND previously issued historical TF IDs are required. No network/write
    is performed. Concurrent writers need a shared lock or retry after a fresh
    duplicate/ID check; this function alone cannot reserve an ID.
    """
    import re
    import unicodedata

    expected = HEADERS["Ideias"]
    if not rows or rows[0][:len(expected)] != expected:
        raise ValueError("Cabeçalhos de Ideias incompatíveis ou não verificados")
    if not isinstance(fields, dict):
        raise ValueError("Idea fields precisam ser um objeto")
    if any(k not in expected[1:] for k in fields):
        raise ValueError("Campo desconhecido na ideia")
    title = fields.get("TEMA", "")
    if not isinstance(title, str) or not title.strip():
        raise ValueError("TEMA obrigatório")
    if not isinstance(fields.get("TESE / CONTEXTO", ""), str) or not fields.get("TESE / CONTEXTO", "").strip():
        raise ValueError("TESE / CONTEXTO obrigatória")
    for key, value in fields.items():
        if not isinstance(value, str):
            raise ValueError("Campos devem ser textos")
        if value.startswith(("=", "+", "-", "@")):
            raise ValueError(f"Fórmula não permitida no campo {key}; usar RAW na escrita")
    if fields.get("PRODUÇÃO VINCULADA"):
        raise ValueError("Ideia nova não pode nascer vinculada a uma produção")

    def norm(value: str) -> str:
        value = unicodedata.normalize("NFKD", value.strip().casefold())
        return " ".join("".join(ch for ch in value if not unicodedata.combining(ch)).split())

    existing_ids = set()
    titles = set()
    for row in rows[1:]:
        if not row or all(not str(v).strip() for v in row):
            continue
        rid = str(row[0]).strip()
        if rid:
            if rid in existing_ids:
                raise ValueError(f"ID duplicado já existente: {rid}")
            existing_ids.add(rid)
            if not re.fullmatch(r"TF_\d{4,}", rid):
                raise ValueError(f"ID inválido em Ideias: {rid}")
        if len(row) > 1 and str(row[1]).strip():
            titles.add(norm(str(row[1])))
    if norm(title) in titles:
        return {"status": "EXISTS", "reason": "Tema idêntico já existe; revisar antes de inserir",
                "writes_performed": False}

    if not isinstance(previously_issued_ids, list) or any(not isinstance(x, str) or not re.fullmatch(r"TF_\d{4,}", x) for x in previously_issued_ids):
        raise ValueError("Histórico completo de IDs TF emitidos é obrigatório e precisa ser validado")
    # Previously promoted ideas are absent from Ideias; never reuse their IDs.
    all_ids = existing_ids | set(previously_issued_ids)
    next_number = max([int(x[3:]) for x in all_ids] or [0]) + 1
    if next_number > 9999:
        raise ValueError("Limite de IDs TF_#### atingido; definir estratégia antes de prosseguir")
    new_id = f"TF_{next_number:04d}"
    if new_id in existing_ids:
        raise AssertionError("Colisão de ID")

    new_fields = {**fields, "ID": new_id}
    new_fields.setdefault("STATUS", "A AVALIAR")
    values = [new_fields.get(k, "") for k in expected]
    return {"status": "READY_TO_INSERT", "id": new_id, "values": values,
            "header": expected, "writes_performed": False,
            "precondition": "Reconsultar Ideias inteira e garantir exclusividade de escrita; se qualquer linha/ID mudou, recalcular. Inserir somente uma linha sem reordenar ou sobrescrever dados; reler pelo ID."}


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    data = json.loads(args.snapshot.read_text(encoding="utf-8"))
    print(json.dumps(validate(data), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
