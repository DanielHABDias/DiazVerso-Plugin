"""Focused unit tests for the optional M01 context-map prototype."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1] / "scripts" / "context_map.py"
spec = importlib.util.spec_from_file_location("m01_context_map", SOURCE)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class ContextMapTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.source = self.write("skills/roteiro/SKILL.md",
                                 "# Roteiro\nVeja [referência](references/checklist.md).\n")
        self.reference = self.write("skills/roteiro/references/checklist.md",
                                    "# Checklist do roteiro\n")
        self.write("docs/DECISOES.md", "# Decisões de trabalho\n")
        self.write("skills/.env", "PRIVATE_SECRET=never-index")

    def write(self, relative, content):
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def test_scoped_graph_excludes_docs_secrets_and_keeps_line_provenance(self):
        result = module.build(self.root)
        self.assertEqual(result["stats"]["files"], 2)
        self.assertNotIn("docs/DECISOES.md", result["nodes"])
        self.assertNotIn("skills/.env", result["nodes"])
        edge = result["nodes"]["skills/roteiro/SKILL.md"]["references"][0]
        self.assertEqual(edge["target"], "skills/roteiro/references/checklist.md")
        self.assertEqual(edge["line"], 2)
        self.assertEqual(edge["evidence"], "EXTRACTED")
        self.assertNotIn("PRIVATE_SECRET", json.dumps(result))

    def test_opt_in_to_docs_is_explicit(self):
        result = module.build(self.root, include_docs=True)
        self.assertIn("docs/DECISOES.md", result["nodes"])

    def test_incremental_update_and_removal_do_not_lose_edges(self):
        a = module.build(self.root)
        b = module.build(self.root, old=a)
        self.assertEqual(b["stats"]["parsed"], 0)
        self.assertEqual(b["stats"]["reused"], 2)
        self.reference.unlink()
        c = module.build(self.root, old=b)
        self.assertEqual(c["stats"]["removed"], 1)
        self.assertEqual(module.find(c, "roteiro")[0]["references"], [])
        self.write("skills/roteiro/references/checklist.md", "# Checklist atualizado\n")
        d = module.build(self.root, old=c)
        self.assertEqual(d["stats"]["parsed"], 1)
        self.assertEqual(d["stats"]["reused"], 1)
        self.assertEqual(len(module.find(d, "roteiro")[0]["references"]), 1)

    def test_changed_file_reparsed_only_once(self):
        a = module.build(self.root)
        self.write("skills/roteiro/SKILL.md", "# Roteiro\n## Testes\n")
        b = module.build(self.root, old=a)
        self.assertEqual(b["stats"]["parsed"], 1)
        self.assertEqual(b["stats"]["reused"], 1)

    def test_query_returns_bounded_metadata_not_file_body(self):
        self.write("skills/roteiro/SKILL.md",
                   "# Roteiro\n## Estrutura\nCorpo longo não deve ser retornado.\n")
        result = module.build(self.root)
        hits = module.find(result, "estrutura", limit=1)
        self.assertEqual(len(hits), 1)
        self.assertEqual(hits[0]["path"], "skills/roteiro/SKILL.md")
        self.assertNotIn("Corpo longo", json.dumps(hits))

    def test_external_link_and_symlink_are_not_indexed(self):
        self.write("skills/roteiro/SKILL.md", "# Roteiro\n[fora](../../../../docs/DECISOES.md)")
        outside = self.root.parent / (self.root.name + "_external.md")
        outside.write_text("# Externo", encoding="utf-8")
        self.addCleanup(outside.unlink)
        link = self.root / "skills" / "external.md"
        try:
            link.symlink_to(outside)
        except (OSError, NotImplementedError):
            pass
        result = module.build(self.root)
        self.assertNotIn("skills/external.md", result["nodes"])
        self.assertEqual(result["nodes"]["skills/roteiro/SKILL.md"]["references"], [])


if __name__ == "__main__":
    unittest.main()
