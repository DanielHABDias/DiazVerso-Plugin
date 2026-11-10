---
name: diazverso-contexto-eficiente
description: "Use quando uma tarefa Diazverso exigir várias fontes, skills ou etapas e for necessário reduzir tokens sem perder decisões, progresso, qualidade ou verificações."
---

# Diazverso — Contexto enxuto sem perder qualidade

**Objetivo:** realizar uma microtarefa por vez, usando contexto mínimo suficiente e acesso sob demanda. Esta skill não substitui competências editoriais nem concede ferramentas.

## Ciclo de uma microtarefa

1. **Localizar o estado atual:** ler apenas o item correspondente do roadmap e o resultado da última revisão; recuperar arquivos e decisões pertinentes. Não reler toda a história do projeto a cada etapa.
2. **Definir escopo:** declarar entrada, arquivo/resultado esperado e gate de aceite; executar **uma microtarefa** por vez. Se a tarefa estiver bloqueada, registrar o motivo e escolher a próxima **independente**.
3. **Carregamento progressivo:** usar metadados das skills para selecionar no máximo a habilidade principal e as realmente necessárias; ler `SKILL.md` somente quando ativada; abrir referências, scripts e assets apenas se a ação exigir. Não carregar as 44 skills antigas.
4. **Observações compactas:** relatar caminhos, IDs e resultados de testes em vez de transcrever arquivos grandes. Manter saída completa **salva e recuperável** no GitHub ou documento aprovado; nunca compactar credenciais para dentro de logs.
5. **Preservar fatos críticos:** decisões recentes, restrições, origem de fonte, status real, IDs, revisão, falhas e a próxima tarefa não podem desaparecer na compactação. Dados antigos e não confirmados são referência, não requisito.
6. **Executar e revisar:** reler arquivos modificados, executar testes disponíveis, separar estático de runtime e conferir links/formatos; **não marcar `[x]` antes da revisão final**. Registrar a evidência e seguir para próxima microtarefa elegível.
7. **Medir antes de afirmar economia:** comparar tarefas equivalentes quanto a contexto carregado, qualidade e falhas. Não prometer uma porcentagem de redução sem métricas.

Para decidir entre skills semelhantes sem carregar todas, consultar `references/roteamento.md` **sob demanda**; o resultado deve ter uma única skill responsável e auxiliares somente se exigidas.

## Skill externa incorporada e atribuição

Para técnicas avançadas, **carregar somente quando necessário** a skill incluída em `skills/context-optimization/SKILL.md` e, se a tarefa justificar, `skills/context-optimization/references/optimization_techniques.md`. É um recurso externo distribuído **dentro deste plugin** sob licença MIT, preservada em `skills/context-optimization/LICENSE`.

Não presumir acesso a contadores exatos de tokens, hooks de cache, edição da janela de contexto, subagentes ou armazenamento local. Estratégias que dependem desses recursos são opcionais e exigem ambiente capaz.

## Limites

- Não condensar de modo a ocultar erro, não descartar decisão recente e não inferir que skills independentes já foram instaladas ou testadas no host.
- Não executar limpeza dos documentos temporários antes do **release 1.0 completo, revisado e comprovadamente instalado**; seguir o registro de pendências.
