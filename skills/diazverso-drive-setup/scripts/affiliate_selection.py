"""K02: deterministic affiliate candidate filtering for a manually posted video.

No Google writes, no purchase, no link opening and no publishing capability.
Input is an already inspected snapshot of the Afiliados sheet. Verifying a
destination and its current conditions remains a separate real-world step.
"""
from __future__ import annotations

import re
from urllib.parse import urlsplit

HEADERS = ["ID", "PRODUTO / SERVIÇO", "CATEGORIA", "PLATAFORMA",
           "LINK AFILIADO", "APLICÁVEL A", "STATUS", "ÚLTIMA VERIFICAÇÃO",
           "FONTE", "OBSERVAÇÕES"]
ACTIVE = "ATIVO"


def _safe_url(value: str) -> bool:
    try:
        url = urlsplit(value.strip())
        return (url.scheme == "https" and bool(url.hostname) and
                url.username is None and url.password is None and
                url.hostname not in {"localhost", "127.0.0.1", "::1"} and
                not url.hostname.endswith(".local"))
    except ValueError:
        return False


def select_affiliates(rows: list[list], topic_tags: list[str], *,
                      verified_ids: list[str], max_items: int = 3) -> dict:
    """Return relevant, ACTIVE, externally reverified candidates.

    verified_ids must contain only IDs whose destination and current terms
    were independently checked during THIS production, not historical
    spreadsheet verification dates. Never infer current status from a date.
    """
    if not rows or list(rows[0][:len(HEADERS)]) != HEADERS:
        raise ValueError("Cabeçalhos de Afiliados não conferem")
    if not isinstance(topic_tags, list) or not topic_tags or any(
        not isinstance(t, str) or not t.strip() for t in topic_tags
    ):
        raise ValueError("Etiquetas de tema válidas são obrigatórias")
    if not isinstance(verified_ids, list) or any(
        not isinstance(x, str) for x in verified_ids
    ):
        raise ValueError("IDs verificados inválidos")
    if not isinstance(max_items, int) or isinstance(max_items, bool) or not 1 <= max_items <= 10:
        raise ValueError("Limite inválido")
    tags = {t.casefold().strip() for t in topic_tags}
    verified = set(verified_ids)
    selected, skipped, seen = [], [], set()
    for row in rows[1:]:
        if not row or not any(str(v).strip() for v in row):
            continue
        record = {h: str(row[i]).strip() if i < len(row) and row[i] is not None else ""
                  for i, h in enumerate(HEADERS)}
        rid = record["ID"]
        if not rid or rid in seen:
            raise ValueError("ID de afiliado ausente ou duplicado")
        seen.add(rid)
        reasons = []
        if record["STATUS"].upper() != ACTIVE:
            reasons.append("NOT_ACTIVE")
        if rid not in verified:
            reasons.append("NOT_REVERIFIED_FOR_VIDEO")
        if not _safe_url(record["LINK AFILIADO"]):
            reasons.append("INVALID_URL")
        applicable = {tag.casefold().strip() for tag in
                      re.split(r"[,;/|]", record["APLICÁVEL A"]) if tag.strip()}
        if not (tags & applicable):
            reasons.append("NOT_RELEVANT")
        if reasons:
            skipped.append({"id": rid, "reasons": reasons})
        else:
            selected.append({"id": rid, "name": record["PRODUTO / SERVIÇO"],
                             "url": record["LINK AFILIADO"],
                             "platform": record["PLATAFORMA"]})
    return {
        "selected": selected[:max_items],
        "skipped": skipped,
        "requires_disclosure": bool(selected[:max_items]),
        "disclosure_suggestion": "Este conteúdo contém links de afiliados. Posso receber uma comissão se você comprar por eles." if selected[:max_items] else "",
        "review_overflow": len(selected) > max_items,
        "writes_performed": False,
        "publishing_performed": False,
    }
