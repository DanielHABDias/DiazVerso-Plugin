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

## Limites

- Não condensar de modo a ocultar erro, não descartar decisão recente e não inferir que skills independentes já foram instaladas ou testadas no host.
- Não executar limpeza dos documentos temporários antes da **V1.0 completa, revisada e empacotada**; a instalação manual pelo criador ocorre somente depois; seguir o registro de pendências.
