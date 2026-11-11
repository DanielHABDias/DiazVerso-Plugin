#!/usr/bin/env python3
"""C06 — deterministic, narrow selection for 12 isolated Diazverso requests.

This selects a skill; it NEVER calls or loads skills, invokes connectors,
renders, approves, or posts videos. Unknown requests fail closed.
"""
from __future__ import annotations
import argparse
import json
import re
from pathlib import Path

RULES = (
 ("retomada","diazverso-criacao-video",r"\b(?:retomar|continuar|continue|retomada)\b"),
 ("configuração","diazverso-setup",r"\b(?:configurar|instalar|conectar|setup)\b"),
 ("economia de contexto","diazverso-contexto-eficiente",r"\b(?:tokens?|contexto|economizar)\b"),
 ("análise factual","diazverso-revisao-fatos",r"\b(?:fontes|checagem factual|revisar fatos|verificar fatos)\b"),
 ("revisão estrutural","diazverso-revisao-estrutura",r"\b(?:estrutura|gancho|payoff|redundância)\b"),
 ("voz narrativa","diazverso-revisao-voz",r"\b(?:humanizar|naturalizar|voz do roteiro)\b"),
 ("aprovação de roteiro","diazverso-aprovacao-roteiro",r"\b(?:aprovar roteiro|liberar roteiro)\b"),
 ("thumbnail","diazverso-thumbnail",r"\b(?:thumbnail|capa do vídeo)\b"),
 ("nox","diazverso-nox",r"\b(?:nox|pose do mascote)\b"),
 ("decupagem","diazverso-decupagem",r"\b(?:decupagem|dividir.*cenas|planejar cenas)\b"),
 ("shorts","diazverso-shorts",r"\b(?:shorts?|vídeo vertical)\b"),
 ("roteiro","diazverso-roteiro",r"\b(?:escrever roteiro|criar roteiro|roteirizar)\b"),
)
META = {"diazverso-core", "diazverso-criacao-video", "diazverso-contexto-eficiente"}


def route(query: str) -> dict:
    if not isinstance(query,str) or not query.strip():
        raise ValueError("Nonempty request required")
    q=query.casefold()
    found=[(label,skill) for label,skill,regex in RULES if re.search(regex,q)]
    if not found:
        return {"status":"NEEDS_INTENT","primary_skill":None,"matched_intents":[],
                "auxiliary_skills":[],"loaded_files":[],"tools_called":[],
                "work_performed":False,"publishing_performed":False}
    # A mixed request must go through the orchestrator rather than secretly
    # loading many skill bodies or silently executing multiple phases.
    skills={skill for _,skill in found}
    mixed=len(skills)>1
    return {"status":"MULTISTEP_PLAN_ONLY" if mixed else "ROUTED",
            "primary_skill":"diazverso-criacao-video" if mixed else found[0][1],
            "matched_intents":[label for label,skill in found],
            "auxiliary_skills":[],
            "loaded_files":[],"tools_called":[],
            "work_performed":False,"publishing_performed":False}


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument("request")
    a=p.parse_args()
    print(json.dumps(route(a.request),ensure_ascii=False,indent=2))


if __name__=="__main__":
    main()
