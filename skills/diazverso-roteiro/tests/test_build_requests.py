"""Testes unitários offline do gerador de requests Google Docs Diazverso."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_requests import requests_for, utf16_length  # noqa: E402


class TestRoteiroRequests(unittest.TestCase):
    def test_longo_nativo(self):
        result = requests_for("LONGO", "VD_0031", "Heróis e legado")
        self.assertEqual(result["id"], "VD_0031")
        self.assertTrue(result["title"].startswith("VD_0031 — "))
        body = result["requests"][0]["insertText"]["text"]
        self.assertIn("VD_0031", body)
        self.assertNotIn("[VD_####]", body)
        self.assertIn("SOM DA CENA — SEM NARRADOR", body)
        self.assertIn("Aprovação do criador: PENDENTE", body)
        self.assertEqual(result["expected"]["last_utf16_index"], 1 + utf16_length(body))
        self.assertEqual(result["expected"]["host_writing"], "NOT_EXECUTED")

    def test_short_vertical(self):
        result = requests_for("SHORT", "SH_0049", "Um gancho surpreendente")
        self.assertEqual(result["type"], "SHORT")
        body = result["requests"][0]["insertText"]["text"]
        self.assertIn("9:16", body)
        self.assertIn("60 s", body)
        self.assertIn("Legenda sincronizada", body)
        self.assertIn("KIT DE PUBLICAÇÃO — NÃO NARRAR", body)

    def test_ranges_match_utf16_including_emoji(self):
        result = requests_for("SHORT", "SH_0100", "Batman 😁 e legado")
        body = result["requests"][0]["insertText"]["text"]
        self.assertEqual(result["expected"]["last_utf16_index"], 1 + utf16_length(body))
        self.assertGreater(utf16_length("😁"), len("😁"))
        for request in result["requests"][1:]:
            spec = request.get("updateParagraphStyle") or request.get("updateTextStyle")
            a = spec["range"]["startIndex"]
            b = spec["range"]["endIndex"]
            self.assertGreaterEqual(a, 1)
            self.assertGreater(b, a)
            self.assertLessEqual(b, result["expected"]["last_utf16_index"])

    def test_invalid_cross_type_id(self):
        with self.assertRaises(ValueError):
            requests_for("LONGO", "SH_0123", "Tema")
        with self.assertRaises(ValueError):
            requests_for("SHORT", "VD_0123", "Tema")
        with self.assertRaises(ValueError):
            requests_for("SHORT", "SH_12", "Tema")

    def test_invalid_theme_and_type(self):
        with self.assertRaises(ValueError):
            requests_for("CURTO", "SH_1234", "Tema")
        with self.assertRaises(ValueError):
            requests_for("LONGO", "VD_1234", " ")
        with self.assertRaises(ValueError):
            requests_for("LONGO", "VD_1234", "x" * 121)

    def test_title_one_line_no_newlines(self):
        result = requests_for("LONGO", "VD_1234", "Título\n com \t quebras")
        self.assertEqual(result["title"], "VD_1234 — Título com quebras — Roteiro")
        self.assertEqual(result["expected"]["sheet_sync"], "NOT_EXECUTED")

    def test_named_styles_generated(self):
        for tipo, ident in (("LONGO", "VD_0001"), ("SHORT", "SH_0001")):
            with self.subTest(tipo=tipo):
                r = requests_for(tipo, ident, "Assunto")
                headings = [q["updateParagraphStyle"]["paragraphStyle"]["namedStyleType"]
                            for q in r["requests"] if "updateParagraphStyle" in q]
                self.assertIn("TITLE", headings)
                self.assertIn("HEADING_1", headings)
                self.assertIn("HEADING_2", headings)
                self.assertTrue(any("updateTextStyle" in q for q in r["requests"]))


if __name__ == "__main__":
    unittest.main()
