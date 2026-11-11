# M01 / Tarefa 88 — comparação técnica e experimento controlado

**Estado em 11/11/2026:** política e utilitário local incorporados à skill de forma **opt-in**, mas **integração automática/efeito em tokens não homologados**; sem instalação de terceiros ou resultado de telemetria Work/API. O pedido atual antecipou a análise originalmente prevista para o final do roadmap. **Não marcar M01 [x].**

## Fontes primárias verificadas

| Opção | Capacidade documentada | Custos e riscos | Juízo para o Diazverso |
| --- | --- | --- | --- |
| [CodeGraph — colbymchenry/codegraph](https://github.com/colbymchenry/codegraph) | CLI + MCP para agentes de código, extração AST/tree-sitter, nós de símbolos e chamadas/imports, índice SQLite local, atualização incremental por mudanças, instalação declarada para Codex CLI. [README](https://github.com/colbymchenry/codegraph/blob/main/README.md) | Binário/runtime e indexação locais, integração MCP que **não está disponível automaticamente no ChatGPT Work**, eventual custo de inicialização, confiança excessiva em índice obsoleto, permissão de uso sobre repo privado; repositório informa licença MIT. | Candidato quando houver **muitas questões de fluxo ou impacto no código**, após teste e autorização; não instalar automaticamente. |
| [Graphify — Graphify-Labs/graphify](https://github.com/Graphify-Labs/graphify) | CLI `graphify` do pacote Python `graphifyy`, grafo JSON/HTML/relatório, parse estrutural local e ligações entre código/documentação/esquemas, marcações `EXTRACTED`/`INFERRED`; extras opcionais para mídia e MCP. [README](https://github.com/Graphify-Labs/graphify#readme) | Dependências Python, índice e tokens consumidos na análise semântica quando backend externo configurado, risco de envio involuntário de docs/ativos, Cloud pago/serviço distinto; repositório indica licenças Apache-2.0 e MIT, **confirmar licença por arquivo antes de redistribuição**. | Candidato mais amplo para **relações código + documentação**, mas complexidade pode superar benefício em repositório pequeno. Não ativar sem necessidade/teste. |
| **Mapa mínimo experimental próprio** (`context_map.py`) | Enumera arquivos textuais permitidos, títulos, cabeçalhos e links explicitamente presentes com arquivo/linha, SHA-256 e reuso incremental por hash; busca lexical limitada. 100% biblioteca padrão Python. | Não resolve chamadas AST, **não compreende semântica** e **não mede tokens**. Para tarefas simples até ele pode custar mais que uma leitura direta. JSON local pode revelar nomes/títulos dos documentos: não compartilhar. | Melhor primeiro piloto **sem dependência externa**, somente quando várias consultas a referências entre skills/docs justificarem. |
| **Nenhum grafo** | Buscar nomes, abrir trechos precisos, usar skill principal e checkpoint curto. | Possível releitura em análises estruturais repetidas, mas sem custo de indexação/servidor. | **Padrão atual** para tarefas isoladas. |

Os números promocionais de economia publicados pelos fornecedores **não comprovam** economia do Diazverso. O [guia de compaction da OpenAI](https://developers.openai.com/api/docs/guides/compaction) documenta interfaces próprias da API Responses; **não autoriza afirmar que uma skill de plugin controla compaction interna do ChatGPT Work**. A [documentação de Agent Skills](https://agentskills.io/specification) e a [pesquisa sobre carregamento progressivo](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills) apoiam o uso seletivo de skills. O [guia de context engineering](https://www.anthropic.com/research/effective-context-engineering-for-ai-agents) ressalta a troca entre recuperação incremental e custo da exploração.

## Protótipo local (opt-in; não integrar ao manifesto)

```bash
python skills/diazverso-contexto-eficiente/scripts/context_map.py --root . --query roteiro
python skills/diazverso-contexto-eficiente/scripts/context_map.py --root . --index /tmp/diazverso-context-map.json --query revisao
python skills/diazverso-contexto-eficiente/scripts/context_map.py --root . --index /tmp/diazverso-context-map.json --include-docs --query contexto
python -m unittest discover -s skills/diazverso-contexto-eficiente/tests -p "test_*.py"
```

**Limites de segurança:** indexa apenas `skills/`, `schemas/`, `templates/`, `plugin.json` e `assets/manifest.json`; `docs/` só com `--include-docs`. Ignora arquivos ocultos, diretórios de build, symlinks e arquivos maiores que 250 KB; não acessa internet nem usa IA. O índice contém **metadados e links** (não corpos completos). Armazenar em área local não versionada; revisar quaisquer metadados antes de compartilhar. A opção `--index` reutiliza nós sem mudança e reprocessa somente SHA-256 modificados. Ela **não prova** economia de tokens e não substitui CodeGraph ou Graphify para análise AST.

## Benchmark obrigatório — **ainda não executado com telemetria real**

Comparar as três tarefas a seguir em pares **idênticos** (baseline sem grafo vs opção escolhida), com **mesmo commit, modelo/nível de esforço, host, permissões, dados e critérios de aceite**. Usar fontes canônicas e conferir caminhos/linhas:

1. **Localizar implementação:** onde se define a seleção da skill de roteiro, e quais testes verificam isso.
2. **Mapear fluxo:** como a orquestradora consulta as regras de contexto, usa referências e chega à próxima microtarefa.
3. **Analisar impacto:** quais links/scripts/documentos efetivamente precisam mudar se a skill de contexto alterar seu nome ou localização.

Para evitar viés, executar as variantes em sessões equivalentes; alternar ordem entre pares; usar um executor capaz de registrar uso real; repetir se a variabilidade for alta. O índice usado no modo otimizado deve ser da **mesma revisão Git** e seu preparo, tempo, leitura de saída e atualização devem contar no custo end-to-end.

### Registro mínimo por execução

- ID e versão da tarefa; commit exato e estado da branch; modelo, esforço e host.
- **Tokens de entrada e saída fornecidos pelo host/API**, incluindo tokens efetivamente consumidos para construir/consultar o índice **quando aplicável**; fonte/ID da telemetria auditável.
- Chamadas por ferramenta, duração de ponta a ponta, tempo de indexação/atualização, bytes do índice e **contexto residual** se o host informar.
- Resultado correto? Referências e linhas corretas? Fatos inferidos apresentados como fatos? Releituras, correções e perda de decisões?
- Custos de memória, segurança e UX: necessidade de rede, permissões, vazamento potencial e complexidade de instalação.

**Uso do comparador já existente**: preencher o objeto JSON com três pares `task_id`, `baseline` e `optimized`, cada execução contendo exatamente `input_tokens`, `output_tokens`, `tool_calls`, `success` e `source`; apontar `source` para o registro de uso real. Executar `python skills/diazverso-contexto-eficiente/scripts/compare_context_cost.py <arquivo.json>`. Não registrar valores ilustrativos como se fossem medições. Anexar tempo/custo de indexação e contexto residual em registro separado, identificando unidade e método, pois o comparador atual não os lê.

### Critério de decisão

Aceitar somente solução que mantenha qualidade e proveniência de **todos** os pares e mostre benefício líquido repetível (tokens/chamadas/tempo, sem aumentar custo total por indexação/retrabalho). Se os sinais forem mistos, restringir a ferramenta ao tipo de tarefa em que ajuda. Se não houver ganho ou acesso autorizado, manter **busca direta + checkpoint** e não criar dependências. A validade da integração com Work/Plugins somente poderá ser afirmada com teste real nesse host, após permissão e disponibilização da ferramenta.

## Pendências específicas para encerrar M01

- [x] Identificar CodeGraph/Graphify e comparar recursos, limites, privacidade e licenças dos repositórios.
- [x] Especificar política de recuperação, checkpoint, compactação e mudança de chat condicionada à capacidade do host.
- [x] Disponibilizar piloto opcional local com testes unitários versionados.
- [x] **Seis testes do protótipo e smoke real de consulta ao repositório passaram** no job isolado `m01-context-map`: [CI #43040170751](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/43040170751). **O job geral de empacotamento ainda falha por teste preexistente do Drive/E02** (`test_publication_success_only_with_verification`: `CONFLICT` em vez de `READY_TO_WRITE`), independente de M01. CI geral não está verde.
- [ ] Obter ≥3 pares de **telemetria real** antes/depois em host compatível, medir custo de índice, qualidade e contexto residual.
- [ ] Decidir integração final, licenças específicas e usabilidade com evidências; atualizar status M01 somente depois do gate.

**O utilitário Python fica distribuído com a skill, mas só é executado sob demanda em host que permita comandos. Não há dependência de CodeGraph/Graphify nem mudança de `plugin.json`; não chamar isso de integração de grafo ao Work.**
