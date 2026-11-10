# A07 — Teste de microtarefa e carregamento progressivo (2026-11-10)

**Estado: PASSOU no fluxo de desenvolvimento via GitHub conectado.** Não é teste de invocação do plugin instalado no ChatGPT/Codex nem medição de tokens.

## Procedimento realmente executado

1. **Selecionar uma microtarefa já revisada** a partir do roadmap: `A06`, criação da matriz de capacidades.
2. **Carregar apenas seus arquivos relevantes** (sem plugin antigo, biblioteca TSX, mídia ou skills de edição): `docs/ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md` (linha A06), `docs/MATRIZ_CAPACIDADES_E_PERMISSOES_V1.md` e `AGENTS.md`.
3. **Conferir a fonte de verdade:** linha `[x] A06` existe no roadmap; documento está realmente no GitHub; contém separação ChatGPT/conectores x Work/Codex, limite do render e autorização.
4. **Conferir o gate:** a linha A06 aponta verificação documental, sem fingir teste de host. A regra do agente prevê leitura sob demanda e revisão antes de avançar.
5. **Resultado:** sete checagens booleanas derivadas dos arquivos **7/7 PASSARAM**. Nenhum arquivo de produção foi movido; nenhuma conta, skill ou ferramenta de host foi declarada instalada.

## Critérios de verificação

| Verificação | Resultado |
| --- | --- |
| Item A06 `[x]` encontrado no roadmap | PASSOU |
| Matriz de capacidades existente, com SHA no GitHub | PASSOU |
| Evidência/gate mencionados no roadmap | PASSOU |
| Distinção ChatGPT e Work/Codex no documento | PASSOU |
| Regra de carregamento sob demanda em AGENTS | PASSOU |
| Limite de render sem executor documentado | PASSOU |
| Arquivo-alvo legível para revisão após commit | PASSOU |

## Limites honestos

- **NÃO testado:** seleção automática da skill pelo host, redução **medida** de tokens, instalação/ativação da V1.0 e retomada persistente entre sessões.
- Esses testes permanecem em **B06, C06/C07 e L04**. Uma simulação documental de fluxo não substitui testes instrumentados dessas tarefas.

Este documento registra evidência reprodutível e pode ser removido após a V1.0 completa, se suas verificações forem consolidadas nos testes definitivos.
