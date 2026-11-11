---
name: diazverso-contexto-eficiente
description: "Use quando uma tarefa Diazverso exigir várias fontes, skills ou etapas e for necessário reduzir tokens sem perder decisões, progresso, qualidade ou verificações."
---

# Diazverso — Contexto enxuto sem perder qualidade

**Objetivo:** obter o resultado correto com o menor trabalho total viável (leituras, chamadas, arquivos, retrabalho e tokens). Uma entrega funcional pode satisfazer diversos itens históricos do roadmap. Esta skill não concede ferramentas nem controla cache/tokens internos do host.

## Estratégia de execução enxuta (decisão 11/11/2026)

1. **Decidir antes de abrir arquivos:** qual resultado observável resolve a necessidade? Verificar se já existe algo funcional; não criar uma skill, script ou documento se uma alteração simples ou reutilização for suficiente.
2. **Agrupar trabalho pelo resultado, não pelo número de checkboxes:** reunir itens que pertencem à mesma funcionalidade (implementação + teste + documentação). Os 87 IDs são rastreabilidade histórica, não obrigação de 87 rodadas, commits ou conversas. Manter critérios críticos de segurança, aprovação e integrações, mesmo agrupados.
3. **Escolher o menor caminho suficiente:** inspecionar apenas trechos/arquivos afetados; usar uma skill principal, auxiliares só quando necessárias; reutilizar funções/testes; evitar comparações, agentes e planejamento extenso para tarefas simples. Scripts e arquivos novos precisam ter uso concreto.
4. **Fazer uma entrega vertical:** implementar uma parte utilizável de ponta a ponta, com interface/entrada/saída reais. Não criar apenas scaffolding ou documentação se a integração executável puder ser feita agora. Identificar ferramentas disponíveis antes de planejar um teste que o ambiente não consegue executar.
5. **Fazer bem, sem revisão cerimonial:** conferir o resultado durante a implementação e executar só as verificações proporcionais ao risco: código → teste focado; Drive/Sheets → leitura de retorno e proteção contra duplicidade; render/áudio → execução real; exclusão/publicação → autorização explícita. **Não abrir uma etapa independente de revisão em toda tarefa**, nem inventar métricas 7/7 ou 12/12. Corrigir erros identificados antes de declarar sucesso.
6. **Atualizar estado somente ao encerrar uma entrega funcional:** marcar somente IDs realmente atendidos, referenciar commit/testes e registrar bloqueios que mudam o próximo passo. Evitar atualizar simultaneamente README, AGENTS, roadmap, handoff e registros com o mesmo parágrafo; atualizar a fonte canônica e um ponteiro curto quando indispensável.
7. **Medir eficiência pelo trabalho total:** quando o host disponibilizar métricas, comparar tokens de entrada/saída, chamadas, tempo, taxa de falhas e retrabalho para a **mesma entrega correta**. Menos tokens em uma chamada não é ganho se duplicar tarefas ou reduzir qualidade. Sem telemetria, tratar eficiência como hipótese e não alegar percentuais.

### Regra de parada

Se a saída já satisfaz os critérios, **parar**. Não acrescentar abstrações, novas skills, pastas, testes redundantes ou futuras funcionalidades sem necessidade demonstrada. Se um item depende de conexão/execução ausente, registrar a pendência e avançar ao próximo trabalho independente; não criar documentação repetitiva como substituto da integração.

### Carregamento de contexto

Metadados → skill relevante → referências somente sob demanda. Nunca ler o roadmap inteiro ou todos os logs em cada rodada; usar a seção consolidada do roadmap e os IDs afetados. Resumir saídas volumosas preservando erros úteis, provas, decisões e caminho de retomada. Não assumir controle sobre KV-cache, masking interno, contagem de tokens ou subagentes se o host não oferecer esses recursos.

## Skill externa incorporada e atribuição

Para técnicas avançadas, **carregar somente quando necessário** a skill incluída em `skills/context-optimization/SKILL.md` e, se a tarefa justificar, `skills/context-optimization/references/optimization_techniques.md`. É um recurso externo distribuído **dentro deste plugin** sob licença MIT, preservada em `skills/context-optimization/LICENSE`.

Não presumir acesso a contadores exatos de tokens, hooks de cache, edição da janela de contexto, subagentes ou armazenamento local. Estratégias que dependem desses recursos são opcionais e exigem ambiente capaz.

## Roteamento focado e medição comparativa — C06/C07

Para diagnósticos de **um único pedido isolado**, `scripts/route_request.py "<pedido>"` seleciona a skill principal por intenção de resultado. São doze intenções cobertas em `tests/test_route_request.py` (setup, contexto, fatos, estrutura, voz, aprovação, thumbnail, Nox, decupagem, Short, roteiro e retomada). O script **não carrega** arquivos ou skills, não executa ferramentas e não usa IA para classificar: quando um pedido combina etapas, devolve `MULTISTEP_PLAN_ONLY` com orquestradora principal. Regras lexicais podem não interpretar sinônimos e não substituem o julgamento do agente; pedido ambíguo devolve `NEEDS_INTENT`.

Para **C07**, o comparador `scripts/compare_context_cost.py <telemetria.json>` recebe pelo menos três pares de **tarefas idênticas** com tokens de entrada/saída, chamadas de ferramentas, sucesso verificado e referência à telemetria. Calcula diferença de consumo antes/depois; não aceita números de tokens estimados, nem conta caracteres como tokens. A implementação e testes aritméticos não provam nenhuma redução. Recolher métricas reais do host ou API, incluindo custo de indexação se houver, e qualidade do resultado. Se os registros não forem verificáveis, manter C07 `[ ]`.

**M01 / Tarefa 88 — contexto no Work/Codex:** quando houver sessão longa, nova frente de trabalho, recuperação repetitiva ou análise de várias skills, consultar **sob demanda** `references/m01-operacao.md`. Priorizar busca focada e checkpoints; a compactação nativa, memória persistente, novo chat e cache interno dependem de controles do host, não desta skill. Não definir limiares percentuais arbitrários. **O utilitário autoral `scripts/context_map.py` já faz parte da skill e pode ser executado sob demanda com Python em repositório local acessível**, para identificar títulos, arquivos, referências com linha e mudanças incrementais: `python skills/diazverso-contexto-eficiente/scripts/context_map.py --root . --query roteiro`. Por padrão não grava índice; `--index <caminho-local-não-versionado>` é opcional e envolve metadados internos. Para tarefas pequenas, continuar com leitura direta. Testes: `python -m unittest discover -s skills/diazverso-contexto-eficiente/tests -p "test_*.py"`. **Não confundir instalação física no pacote com chamada automática pelo Work:** a capacidade real de executar comandos/ler repositório precisa existir. M01 segue `[ ]` até três pares de telemetria real, ganho líquido e correção verificados; comparação técnica em `docs/M01_AVALIACAO_CONTEXTO_TAREFA_88.md` durante o desenvolvimento.

## Limites

- Não condensar de modo a ocultar erro, não descartar decisão recente e não inferir que skills independentes já foram instaladas ou testadas no host.
- Não executar limpeza dos documentos temporários antes da **V1.0 completa, revisada e empacotada**; a instalação manual pelo criador ocorre somente depois; seguir o registro de pendências.
