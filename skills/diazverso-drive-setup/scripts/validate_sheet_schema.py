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


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("snapshot", type=Path)
    args = parser.parse_args()
    data = json.loads(args.snapshot.read_text(encoding="utf-8"))
    print(json.dumps(validate(data), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
