---
name: context-optimization
description: "Use for advanced context budgeting, bounded retrieval, observation summarization and prompt-cache design when the runtime exposes the necessary controls."
---

**Protocolo obrigatório Diazverso:** antes de agir, aplicar `../diazverso-contexto-eficiente/SKILL.md`. Ler uma vez por sessão/versão e reutilizar o contexto válido; abrir somente a skill principal e as dependências necessárias.

# Context optimization

Optimize the total work required for a correct result, including retrieval, tool calls, rework and coordination. Preserve decisions, active errors, evidence and source identity.

## Choose the smallest effective technique

1. **Stable prefixes:** when implementing an API application, keep instructions and reusable examples stable; append dynamic metadata afterward. Prompt-cache configuration belongs to that application, not to a skill running in an opaque host.
2. **Bounded retrieval:** select the responsible skill from metadata or the local graph, then read only the next action's sources. Reuse valid observations; refresh a source when its revision changes or before a consequential write.
3. **Observation summaries:** replace repeated narrative with a short result, evidence reference and unresolved error. Keep complete outputs recoverable. Never hide an error during debugging.
4. **Checkpoints:** preserve objective, current source/revision, decisions, verified result, blockers and next action. For the mandatory semantic-compaction procedure, consult [working-context compaction](../diazverso-contexto-eficiente/references/compactacao.md) only when needed. A written checkpoint does not compact the host's internal context.
5. **Partitioning:** use an independent agent only when available, authorized and expected to reduce total work. Account for coordination overhead; do not delegate small tasks merely because delegation exists.

Consult [technique details](references/optimization_techniques.md) only when implementing a specific optimization or measurement system. Its examples and targets are conditional engineering patterns, not promises about the current host.

## Measure honestly

Use real input/output tokens, calls, elapsed time, correctness and rework for equivalent completed tasks. Include indexing and coordination costs. Without telemetry, describe observed reuse or bounded reads rather than a percentage of token savings.

Do not invent cache hit rates, modify hidden reasoning, assume control over compaction, apply arbitrary utilization thresholds or claim a summary has reset the context window. Follow the runtime's actual controls and higher-priority instructions.

License and attribution are preserved in `LICENSE`.
