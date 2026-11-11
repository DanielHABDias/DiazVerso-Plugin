import importlib.util
import unittest
from pathlib import Path

P=Path(__file__).resolve().parents[1]/"scripts"/"route_request.py"
s=importlib.util.spec_from_file_location("diazverso_route_request",P)
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)

CASES={
 "quero configurar o Drive":"diazverso-setup",
 "economizar tokens":"diazverso-contexto-eficiente",
 "revisar fatos e fontes":"diazverso-revisao-fatos",
 "verificar estrutura e gancho":"diazverso-revisao-estrutura",
 "humanizar a voz do roteiro":"diazverso-revisao-voz",
 "aprovar roteiro":"diazverso-aprovacao-roteiro",
 "criar thumbnail":"diazverso-thumbnail",
 "fazer uma pose do Nox":"diazverso-nox",
 "fazer decupagem":"diazverso-decupagem",
 "criar um Short":"diazverso-shorts",
 "escrever roteiro":"diazverso-roteiro",
 "continuar a produção":"diazverso-criacao-video",
}
class RouteTests(unittest.TestCase):
    def test_twelve_isolated_requests_select_exact_primary(self):
        self.assertEqual(len(CASES),12)
        for query,expected in CASES.items():
            with self.subTest(query=query):
                r=m.route(query)
                self.assertEqual(r["primary_skill"],expected)
                self.assertEqual(r["status"],"ROUTED")
                self.assertEqual(r["auxiliary_skills"],[])
                self.assertEqual(r["loaded_files"],[])
                self.assertEqual(r["tools_called"],[])
                self.assertFalse(r["publishing_performed"])
    def test_ambiguous_combined_request_returns_orchestrator(self):
        r=m.route("escrever roteiro e criar thumbnail")
        self.assertEqual(r["status"],"MULTISTEP_PLAN_ONLY")
        self.assertEqual(r["primary_skill"],"diazverso-criacao-video")
        self.assertFalse(r["work_performed"])
    def test_unknown_question_does_not_pretend_to_route(self):
        self.assertEqual(m.route("bom dia")["status"],"NEEDS_INTENT")
    def test_empty_request_invalid(self):
        with self.assertRaises(ValueError):m.route(" ")
    def test_no_upload_tool_or_side_effect(self):
        for query in CASES:
            r=m.route(query)
            self.assertFalse(r["work_performed"])
            self.assertFalse(r["publishing_performed"])
if __name__=="__main__":unittest.main()
