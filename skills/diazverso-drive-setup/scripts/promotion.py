"""promotion/recovery: plan promotion from TF idea to VD/SH production, without Google writes.

Only use a complete, freshly read, header-checked snapshot from the SAME
spreadsheet. The connector executes any authorized operations, re-reads data
between phases, and must serialize writes/IDs. This planner never deletes rows.
"""
from __future__ import annotations

import re
from typing import Any, Sequence

IDEAS = ["ID","TEMA","TESE / CONTEXTO","TÍTULO PROVISÓRIO","IDEIA DE THUMB","POR QUE VALE","PRIORIDADE","TIMING / CONTEXTO","ORIGEM","STATUS","PRODUÇÃO VINCULADA","OBSERVAÇÕES"]
PRODUCTIONS = ["ID","TIPO","TEMA / CONTEXTO","STATUS","PRIORIDADE","TÍTULO A","TÍTULO B","THUMBNAIL A","THUMBNAIL B","ROTEIRO","VÍDEO RELACIONADO","PLANEJADO PARA","PUBLICADO EM","LINK YOUTUBE","REVISÃO","OBSERVAÇÕES","KIT PUBLICAÇÃO"]
ORIGIN = re.compile(r"(?:^|(?:\s|;))IDEIA_ORIGEM_ID=(TF_\d{4,})(?=$|[\s;])")
VALID_IDEA = re.compile(r"TF_\d{4,}")
VALID_PROD = re.compile(r"(?:VD|SH)_\d{4,}")


def _records(rows: Sequence[Sequence[Any]], header: list[str], name: str) -> list[dict[str, str]]:
    if not rows or list(rows[0][:len(header)]) != header:
        raise ValueError(f"Cabeçalho {name} ausente ou alterado")
    output = []
    seen = set()
    for raw in rows[1:]:
        if not raw or not any(str(v).strip() for v in raw):
            continue
        rec = {col: str(raw[i]).strip() if i < len(raw) and raw[i] is not None else ""
               for i, col in enumerate(header)}
        rid = rec["ID"]
        if not rid:
            raise ValueError(f"Linha preenchida sem ID em {name}")
        pattern = VALID_IDEA if name == "Ideias" else VALID_PROD
        if not pattern.fullmatch(rid) or rid in seen:
            raise ValueError(f"ID inválido/duplicado em {name}: {rid}")
        seen.add(rid)
        output.append(rec)
    return output


def _origin(row: dict[str, str]) -> str | None:
    m = ORIGIN.search(row["OBSERVAÇÕES"])
    return m.group(1) if m else None


def plan_promotion(ideas_rows: list[list], production_rows: list[list],
                   idea_id: str, kind: str, *,
                   historical_production_ids: list[str],
                   doc_verified: bool = False) -> dict[str, Any]:
    """One phase at a time; destructive deletion NEVER occurs here.

    Output actions are advisory; only perform after authorization and fresh
    readback. For removal, first confirm production ID+origin+native Doc URL
    and that the production fields match the source idea.
    """
    if not VALID_IDEA.fullmatch(idea_id):
        raise ValueError("ID de ideia inválido")
    if kind not in ("LONGO", "SHORT"):
        raise ValueError("Tipo deve ser LONGO ou SHORT")
    if not isinstance(historical_production_ids, list) or any(
        not isinstance(x, str) or not VALID_PROD.fullmatch(x)
        for x in historical_production_ids
    ):
        raise ValueError("Histórico completo de IDs VD/SH obrigatório")
    ideas = _records(ideas_rows, IDEAS, "Ideias")
    productions = _records(production_rows, PRODUCTIONS, "Produções")
    source = [x for x in ideas if x["ID"] == idea_id]
    related = [x for x in productions if _origin(x) == idea_id]
    if len(related) > 1:
        return {"status": "BLOCKED_DUPLICATE_PRODUCTION", "writes_performed": False}
    if related:
        target = related[0]
        if target["TIPO"] != kind:
            return {"status": "BLOCKED_TYPE_MISMATCH", "id": target["ID"], "writes_performed": False}
        if source and source[0]["PRODUÇÃO VINCULADA"] not in ("", target["ID"]):
            return {"status": "BLOCKED_CONFLICTING_LINK", "writes_performed": False}
        if not source:
            complete = doc_verified and target["ROTEIRO"].startswith("https://docs.google.com/document/d/")
            return {"status": "ALREADY_PROMOTED" if complete else "SOURCE_MISSING_REQUIRES_RECOVERY",
                    "id": target["ID"], "writes_performed": False,
                    "next": "Se falta Doc validado, investigar remoção prematura; não criar outra produção"}
        if not target["TEMA / CONTEXTO"] or not source[0]["TEMA"] or source[0]["TEMA"] not in target["TEMA / CONTEXTO"]:
            return {"status": "BLOCKED_CONTENT_MISMATCH", "writes_performed": False}
        if source[0]["PRODUÇÃO VINCULADA"] != target["ID"]:
            return {"status": "LINK_SOURCE_IDEA", "id": target["ID"],
                    "idea_id": idea_id, "writes_performed": False,
                    "next": "Atualizar APENAS PRODUÇÃO VINCULADA no TF exato; reler"}
        if not doc_verified or not target["ROTEIRO"].startswith("https://docs.google.com/document/d/"):
            return {"status": "WAIT_FOR_VERIFIED_DOC", "id": target["ID"],
                    "writes_performed": False,
                    "next": "Concluir script-document: Doc nativo formatado e link relido na produção"}
        return {"status": "READY_FOR_AUTHORIZED_REMOVAL", "id": target["ID"],
                "idea_id": idea_id, "writes_performed": False,
                "next": "Somente após consentimento específico: reler as DUAS abas, confirmar ID/origem/Doc e excluir a linha TF identificada pelo ID atual, nunca índice em cache"}
    if not source:
        return {"status": "BLOCKED_IDEA_NOT_FOUND", "writes_performed": False}
    idea = source[0]
    if idea["PRODUÇÃO VINCULADA"]:
        return {"status": "BLOCKED_STALE_LINK", "writes_performed": False}
    if not idea["TEMA"] or not idea["TESE / CONTEXTO"]:
        return {"status": "BLOCKED_MISSING_CONTENT", "writes_performed": False}
    prefix = "VD" if kind == "LONGO" else "SH"
    ids = {x["ID"] for x in productions} | set(historical_production_ids)
    current = [int(x.split("_")[1]) for x in ids if x.startswith(prefix + "_")]
    number = max(current, default=0) + 1
    if number > 9999:
        return {"status": "BLOCKED_ID_SPACE", "writes_performed": False}
    new_id = f"{prefix}_{number:04d}"
    record = {
        "ID": new_id, "TIPO": kind,
        "TEMA / CONTEXTO": f"{idea['TEMA']} — {idea['TESE / CONTEXTO']}",
        "STATUS": "PLANEJADO", "PRIORIDADE": idea["PRIORIDADE"] or "MÉDIA",
        "TÍTULO A": idea["TÍTULO PROVISÓRIO"],
        "OBSERVAÇÕES": f"IDEIA_ORIGEM_ID={idea_id}"
    }
    return {"status": "CREATE_PRODUCTION", "id": new_id,
            "idea_id": idea_id, "row": [record.get(k, "") for k in PRODUCTIONS],
            "writes_performed": False,
            "next": "Reconsultar IDs e origem sob exclusividade de escrita; inserir linha formatada sem sobrescrever; reler por ID e IDEIA_ORIGEM_ID; nunca excluir TF antes de confirmar Doc"}
