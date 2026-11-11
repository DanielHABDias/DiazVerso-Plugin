"""E08: pure, side-effect-free planner for one existing Produções row.

A Sheets-capable caller performs the authorized write, then re-reads the target
by stable ID; this module neither connects to Google nor changes stored data.
"""
from __future__ import annotations
import re

HEADERS = ["ID","TIPO","TEMA / CONTEXTO","STATUS","PRIORIDADE","TÍTULO A","TÍTULO B","THUMBNAIL A","THUMBNAIL B","ROTEIRO","VÍDEO RELACIONADO","PLANEJADO PARA","PUBLICADO EM","LINK YOUTUBE","REVISÃO","OBSERVAÇÕES","KIT PUBLICAÇÃO"]
EDITABLE = {"TÍTULO A", "TÍTULO B", "THUMBNAIL A", "THUMBNAIL B",
            "ROTEIRO", "STATUS", "PUBLICADO EM", "LINK YOUTUBE", "REVISÃO",
            "KIT PUBLICAÇÃO"}
VALID_IDS = re.compile(r"(?:VD|SH)_\d{4,}$")
VALID_STATUSES = {"PLANEJADO","PESQUISA","ROTEIRO","REVISÃO DE ROTEIRO",
                  "ASSETS","EDIÇÃO","REVISÃO FINAL","PRONTO","AGENDADO",
                  "PUBLICADO","PAUSADO","CANCELADO"}
DOC = re.compile(r"https://docs\.google\.com/document/d/[A-Za-z0-9_-]+(?:[/?#].*)?$")
DRIVE_FILE = re.compile(r"https://drive\.google\.com/file/d/[A-Za-z0-9_-]+(?:[/?#].*)?$")
YOUTUBE = re.compile(r"https://(?:www\.)?youtube\.com/(?:watch\?v=|shorts/)[A-Za-z0-9_-]{6,}(?:[&#?].*)?$|https://youtu\.be/[A-Za-z0-9_-]{6,}(?:[?&#].*)?$")


def plan_upsert(rows: list[list], production_id: str, patch: dict[str, str],
                *, expected: dict[str, str] | None = None,
                allow_replace: bool = False,
                publication_verified: bool = False,
                review_approved: bool = False) -> dict:
    """Plan a cell-level update, never an insert or destructive overwrite.

    The caller must check this plan against a fresh spreadsheet read immediately
    before writing, serialize concurrent writes, and read back the exact ID/cells.
    Evidence flags require actual external confirmation, not caller guesses.
    """
    if not VALID_IDS.fullmatch(production_id):
        raise ValueError("ID VD/SH inválido")
    if not rows or list(rows[0][:len(HEADERS)]) != HEADERS:
        raise ValueError("Cabeçalhos de Produções não conferem")
    if not isinstance(patch, dict) or not patch or any(k not in EDITABLE for k in patch):
        raise ValueError("Patch vazio ou coluna não permitida")
    if any(not isinstance(v, str) for v in patch.values()):
        raise ValueError("Todos os valores devem ser strings")
    if any(v.startswith(("=", "+", "-", "@")) for v in patch.values()):
        raise ValueError("Não aceitar fórmula: usar escrita RAW e confirmar conteúdo")
    matches = [(i + 2, raw) for i, raw in enumerate(rows[1:])
               if raw and str(raw[0]).strip() == production_id]
    if len(matches) != 1:
        raise ValueError("Produção inexistente ou ID duplicado")
    row_number, raw = matches[0]
    current = {name: str(raw[i]) if i < len(raw) and raw[i] is not None else ""
               for i, name in enumerate(HEADERS)}
    kind = "LONGO" if production_id.startswith("VD_") else "SHORT"
    if current["TIPO"] != kind:
        raise ValueError("ID e TIPO discordam")
    if expected is not None and any(current.get(k) != v for k, v in expected.items()):
        return {"status": "CONFLICT", "id": production_id, "writes_performed": False}

    for field, value in patch.items():
        if field == "ROTEIRO" and value and not DOC.fullmatch(value):
            raise ValueError("ROTEIRO deve apontar ao Google Doc nativo, não à pasta")
        if field in ("THUMBNAIL A", "THUMBNAIL B") and value and not DRIVE_FILE.fullmatch(value):
            raise ValueError("Thumbnail deve apontar ao arquivo de imagem do Drive, não à pasta")
        if field == "LINK YOUTUBE" and value and not YOUTUBE.fullmatch(value):
            raise ValueError("Link YouTube inválido")
        if field == "STATUS" and value not in VALID_STATUSES:
            raise ValueError("STATUS inválido")
        if field == "REVISÃO" and value.strip().upper() in ("APROVADO", "APROVADA") and not review_approved:
            raise ValueError("Revisão aprovada requer decisão realmente verificada")
    future = {**current, **patch}
    publication_fields = {"STATUS", "PUBLICADO EM", "LINK YOUTUBE"} & patch.keys()
    if patch.get("PUBLICADO EM") and not re.fullmatch(r"\\d{4}-\\d{2}-\\d{2}", patch["PUBLICADO EM"]):
        raise ValueError("PUBLICADO EM deve ser data YYYY-MM-DD")
    if publication_fields and future["STATUS"] == "PUBLICADO":
        if not publication_verified or not future["PUBLICADO EM"] or not YOUTUBE.fullmatch(future["LINK YOUTUBE"]):
            raise ValueError("PUBLICADO requer confirmação real, data e link do vídeo")
    elif ("LINK YOUTUBE" in patch and patch["LINK YOUTUBE"]) or ("PUBLICADO EM" in patch and patch["PUBLICADO EM"]):
        if not publication_verified:
            raise ValueError("Link/data de publicação requer confirmação real")
    updates = []
    for field, value in patch.items():
        old = current[field]
        if old == value:
            continue
        if old and old != value and not allow_replace:
            return {"status": "CONFLICT", "id": production_id, "field": field,
                    "existing": old, "proposed": value, "writes_performed": False}
        col = HEADERS.index(field)
        letters = ""
        n = col + 1
        while n:
            n, rem = divmod(n - 1, 26)
            letters = chr(65 + rem) + letters
        updates.append({"column": field, "a1": f"{letters}{row_number}",
                        "before": old, "after": value})
    return {"status": "NO_CHANGE" if not updates else "READY_TO_WRITE",
            "id": production_id, "row": row_number, "updates": updates,
            "writes_performed": False,
            "precondition": "Reconsultar ID, TIPO e valores ANTES imediatamente antes da escrita; atualizar somente células listadas com RAW; reler ID e valores DEPOIS"}
