# Diazverso Plugin 1.0 — Roadmap de implementação em microtarefas

**Data:** 2026-11-10  
**Estado:** ROADMAP PARA EXECUÇÃO. Nenhum item deste roadmap equivale, sozinho, à funcionalidade implementada.  
**Destino:** [repositório novo](https://github.com/DanielHABDias/DiazVerso-Plugin).  
**AUDITORIA FINAL PARA O CODEX — 10/11/2026:** **25/87 concluídas**, **62 pendentes**. **B06 [x]** (ZIP validado no CI sem instalação) está concluída no escopo correto. **F06 [ ]** (integração real Google Docs/Sheets) continua parcial. Ver [PASSAGEM PARA CODEX](HANDOFF_CODEX_2026-11-11.md) e [riscos](REGISTRO_EXECUCAO_E_PENDENCIAS.md) para continuidade e **limpeza OBRIGATÓRIA dos documentos transitórios somente após release 1.0 completa e validada**. Este próprio roadmap será removido ao final, após migração de conhecimento e testes de referências.  
**Objetivo:** um plugin instalável para ChatGPT e Codex baseado **nas decisões de 2026-11-10**, que coordene em microtarefas pesquisa → tese/packaging → roteiro formatado → thumbnails → narração/assets → instruções e exemplos Remotion/TSX independentes → revisão audiovisual → kit de publicação. **Content Lab antigo é obsoleto e sua refatoração será um projeto separado, após o novo plugin estar concluído.** O fluxo completo depende das ferramentas e autorizações reais do host.

> **CORREÇÃO DE PRIORIDADE 2026-11-10:** o trabalho editorial/operacional definido **hoje** prevalece. Plugin antigo e Content Lab antigo são obsoletos; consultar só ideias e exemplos TSX relevantes. **Refatoração do Content Lab é posterior à conclusão do novo plugin**, não pré-requisito. Criador de plugin selecionado: **OpenAI Plugin Creator oficial**; criação de skills orientada pelo **Skill Creator oficial** e padrão Agent Skills. Microtarefas e gates preservados.

## 0. Regras de execução (obrigatórias)
**DECISÃO CORRETIVA DO CRIADOR (2026-11-10):** **não instalar nada agora** no ChatGPT ou Codex. Construir, verificar, empacotar e documentar o plugin **exclusivamente no GitHub**; ao final da V1.0 o criador gerará/baixará o ZIP e o instalará por conta própria. Assim, B06 é um teste de pacote/CI, **não de instalação**. Alterações nesta decisão prevalecem sobre menções antigas neste roadmap e nos relatórios.

**SKILLS ESPECIALIZADAS — PRIORIDADE:** Codex deverá avaliar **Remotion oficiais (create, markup, best-practices, render, captions, multimedia)**, **HyperFrames, GSAP, Humanizer, Last30Days, Baoyu Cover Image, skills de context engineering/otimização de tokens, Superpowers/Skill Creator, vidIQ quando conectado, EarShot, WATCH e Iris**; avaliar também outras opções superiores justificadas. **Iris foi descrito pelo criador como ferramenta para a IA enxergar/analisar vídeo, possivelmente um aplicativo, não necessariamente uma skill**: identificar o produto/repositório exato e interface antes de prometer integração. As skills externas **selecionadas para uso final devem estar fisicamente no plugin** (não só em links) quando houver permissão de redistribuição. **GitHub público não é licença de redistribuição**. Se não houver licença clara, estudar documentação pública e comportamento geral, entender princípios e **escrever uma skill Diazverso nova, independente e original, sem copiar código/textos protegidos**; testar e revisar a qualidade. Não importar em massa, não inserir credenciais, evitar instruções maliciosas e preservar avisos/licenças. Ver [catálogo prioritário e política de integração](CATALOGO_SKILLS_PRIORITARIAS_E_IRIS.md).

**Atualização de governança (2026-11-10):** criador autorizou seguir automaticamente para microtarefas elegíveis após revisão, sem pedir 'próximo'. **Não instalar o plugin durante o desenvolvimento.** B06 foi redefinida como validação do pacote no CI, já concluída. O criador instalará pessoalmente o ZIP somente depois da V1.0 completa, testada e limpa. Continuar microtarefas revisadas sem esperar instalação. Skills externas selecionadas serão **vendorizadas dentro do plugin quando a licença autorizar**, com referências e licenças; sem licença, adaptar de forma autoral sem copiar arquivos. Documentos temporários serão removidos **somente após release 1.0 completa, validada e com o conhecimento migrado**, não durante as fases de implementação. Registrar impedimentos em [REGISTRO_EXECUCAO_E_PENDENCIAS.md](REGISTRO_EXECUCAO_E_PENDENCIAS.md).


1. **Uma microtarefa por vez:** selecionar o primeiro checkbox pendente cujos pré-requisitos estejam concluídos. Executar, conferir e registrar resultado **antes** de iniciar outra. Não combinar “implementar toda a fase” em uma única solicitação/commit.
2. Cada tarefa deve ter: **entrada, entrega concreta, validação/teste, arquivo(s) impactado(s), estado e próxima tarefa**. Uma tarefa que requer muitas alterações deve ser fracionada antes de começar.
3. **Trabalhar no repositório novo e usar as decisões de hoje como prioridade**; plugin antigo e Content Lab antigo são **obsoletos**, apenas repositórios de ideias/exemplos a consultar seletivamente. **Não incorporar regras velhas nem depender do Content Lab para lançar o plugin V1.0.** Refatorar Content Lab somente depois do plugin novo estar concluído.
4. Tratar cada decisão com origem: **aprovada no novo contexto**, **referência do plugin antigo**, **hipótese a verificar**. Não transferir regras velhas de pastas por vídeo, planilha em duas abas, balões HQ ou espiral obrigatória.
5. **Contexto enxuto:** ler `AGENTS.md`, resumo de decisões e **somente a skill/referência da tarefa atual**; retornar link/resumo do resultado, não despejar árvores/código enormes na conversa. Salvar estado no GitHub.
6. Subagentes são **opcionais** e somente quando runtime suportar, para trabalho independente com escopo estreito (inventário, pesquisa, testes). O agente principal decide, integra e valida sequencialmente; não delegar edições concorrentes no mesmo arquivo.
7. **Não presumir acesso ao Drive, render, GitHub ou YouTube:** verificar conexões/permissões e relatar bloqueios. Plugin de skills ≠ motor de render; render real exige Remotion/Content Lab em ambiente capaz.
8. **Não copiar automaticamente mídia de terceiros** do Drive para repositório distribuível. Nox canônico e materiais próprios/aprovados primeiro; verificar direitos de backgrounds, SFX, memes, músicas, fontes e distribuição.
9. **Não criar arquivos .old/.bak, versões paralelas de regras, campos `schemaVersion` sem necessidade aprovada, nem funcionalidades de composição musical** removidas do Content Lab anterior.
10. Por tarefa concluída: alteração pequena + teste/evidência quando aplicável + atualização desta checklist (e de `docs/DECISOES_E_CONTEXTO.md` quando houver decisão) + próximo ID.

**Gate obrigatório de revisão por microtarefa (decisão reforçada pelo criador em 2026-11-10):** depois de criar/editar um arquivo, fazer uma **segunda passagem de revisão** (estrutura, coerência com decisões, referências, erros e leitura de volta; testes reais quando houver código executável). Corrigir reprovações e repetir. **Somente depois de aprovação atualizar `[x]` e selecionar a próxima microtarefa.** Revisão documental não substitui teste de execução/instalação, que permanece pendente até seu estágio.

### Convenção de conclusão

- `[ ]` pendente; `[x]` concluída com evidência e revisão.
- Para cada tarefa, registrar em commit/PR **ID + entrega + teste**. Falhas: permanecer pendente e guardar o bloqueio. `NÃO_VERIFICADO` não equivale a `APROVADO`.
- Não criar dezenas de issues obrigatórias antes de começar. Esta checklist é o quadro mestre. Um agente pode gerar PR/issue por microtarefa conforme o fluxo do usuário.

## 1. Fontes reais conferidas nesta sessão

| Origem | Localização | Uso adequado |
| --- | --- | --- |
| Nova base | [DiazVerso-Plugin](https://github.com/DanielHABDias/DiazVerso-Plugin), branch principal | Fonte de verdade de decisões 1.0 |
| Drive — plugin anterior | [diazverso-plugin](https://drive.google.com/drive/folders/19_n1sPV0fkLJhD3YZKoyabrWMosvjw_k) | Inventário com **44 pastas de skills**, README, manifestos e exemplos; material de consulta, não instalação automática |
| Drive — TSX antigo | [Custom Cenas Diazverso](https://drive.google.com/drive/folders/1yWogLK6bRWXunvdJxTHBMIqB4ibSN44f) | Biblioteca com cenários TSX, README, JSON, previews 16:9/9:16 |
| Drive — mascote | [Nox/Nox.png](https://drive.google.com/file/d/1X6pabe9ZhBTmOycrtURwg7nDzmJf_M61/view) | Arquivo real PNG (415.179 bytes) a conferir visualmente e **incluir fisicamente** no plugin |
| Drive — mídia atual | [Diazverso](https://drive.google.com/drive/folders/1SbOI-GtWAaWzxFh1ysG5DOjf0DZ8XSYh) | Bibliotecas Assets, Backgrounds, Memes, Músicas, Sounds; organizar por status/licença |
| Content Lab antigo | [DanielHABDias/ContentLab](https://github.com/DanielHABDias/ContentLab), `main`; [layout histórico](https://github.com/DanielHABDias/ContentLab/blob/main/docs/PROJECT_LAYOUT.md) | **Obsoleto para o novo plugin; apenas referência histórica. Refatoração somente depois do novo plugin concluído.** |
| Organização do Drive | [Contrato operacional](CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md) e [Bibliotecas](ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md) | Estrutura aprovada, IDs apenas desta instalação |
| Identidade editorial | [Rascunho em evolução](RASCUNHO_IDENTIDADE_DIAZVERSO_1.0.md) | Briefing a consolidar, **não inteiro em prompt global** |

**TSX confirmados por listagem/leitura inicial:** `TextoHQ.tsx` (Anton/Bangers, texto cinético), `PersonagemEspiralLegenda.tsx` (personagem/legendas), `QuadroHQSobreCena.tsx` (quadro sobre imagem/vídeo), `BackgroundHQ.tsx` (halftone/papel/estrelas/grade), `GaleriaCartasHQ.tsx`, `ComicPageCTA.tsx` e `HQMotion.tsx`, com `HQComicPage.tsx` como dependência compartilhada. Parte dos módulos tem prévias, JSON e variantes 16:9/9:16. **Arquivos da antiga biblioteca não foram importados para o novo GitHub nem compilados nesta fase.** O `HQComicPage.tsx` está repetido nas pastas e exige deduplicação e comparação com o Content Lab atual.

### Skills externas selecionadas para investigar e aplicar seletivamente

- **Eficiência de tokens:** [context-optimization](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering), `context-compression`, `filesystem-context`, `memory-systems`, `multi-agent-patterns`. Aplicar **progressive disclosure** (metadata → SKILL.md → references/assets/scripts) e medir custo em testes comparáveis. Não prometer percentuais sem medição.
- **Execução em tarefas pequenas e qualidade de software:** [obra/superpowers](https://github.com/obra/superpowers) — `writing-plans`, `executing-plans`, testes/revisão; adaptar ao ChatGPT/Codex, sem assumir subagentes disponíveis.
- **Remotion (oficial):** [remotion-dev/skills](https://github.com/remotion-dev/skills) — `remotion-best-practices`, `remotion-markup`, `remotion-create`, `remotion-render`, `remotion-studio`, `remotion-captions`, `remotion-multimedia`, `remotion-docs`. Usar como referência independente para cenas/QA, validando a versão do Remotion no ambiente de testes; **não usar o Content Lab antigo como dependência obrigatória**.
- **Criadores oficiais escolhidos [A01]:** **Plugin Creator** (`skills://plugins/plugin-creator/create-plugin` **presente nesta sessão**) como orientação/validação de pacote; **Skill Creator** oficial para autoria de skills quando disponível no host; especificação aberta [Agent Skills](https://agentskills.io/specification) e [OpenAI Plugin Docs](https://developers.openai.com/plugins/build/plugins). `plugin.json` portátil na raiz + `skills/<nome>/SKILL.md`; `assets/` com Nox essencial; `mcp.json` só se houver endpoint/necessidade real. **Não exigir ferramenta/skill de terceiro de criação.**
- **Outros candidatos não homologados:** HyperFrames, GSAP, Humanizer, Baoyu Cover Image, Last30Days, WATCH, EarShot, Iris, Browser Use, Openverse/Real SFX. Investigar licença, compatibilidade e valor real individualmente; não pré-instalar ou assumir equivalência.
- **Pesquisa de YouTube:** vidIQ quando conectado, fontes oficiais e pesquisa complementar; resultados podem ser usados para perguntas/hipóteses, não promessas do algoritmo.

## 2. Roadmap detalhado — executar na ordem de dependência

### Fase A — Seleção da tecnologia, consolidação das decisões novas e fronteiras

- [x] **A01** — **VALIDADO EM 2026-11-10 (avaliação documental):** selecionar **Plugin Creator oficial OpenAI, disponível neste ambiente**, para pacotes do plugin; usar **Skill Creator oficial** em host que o disponibilizar para skills individuais; padronizar `Agent Skills` com disclosure progressivo. Fontes: `skills://plugins/plugin-creator/create-plugin`, https://developers.openai.com/plugins/build/plugins , https://developers.openai.com/plugins/build/skills e https://agentskills.io/specification . **Ainda não significa teste de instalação do pacote Diazverso.**
- [x] **A02 — CONCLUÍDA E REVISADA (2026-11-10):** criada `docs/ESPECIFICACAO_CANONICA_DIAZVERSO_V1.md` (6,8 mil caracteres) com precedência das decisões atuais, direção editorial refinável, Nox canônico, fluxo Drive/Sheets aprovado, skills externas licenciadas, revisão por tarefa e limpeza pós-release. **Primeira inspeção 8/8, revisão independente 12/12**, referências verificadas; `AGENTS.md` atualizado e relido (7/7) para eliminar instruções obsoletas sobre B06/C01 e Nox. **Não representa validação do host.**
- [ ] **A03** — Montar **catálogo seletivo** de poucos TSX antigos relevantes (texto, fundos, Nox, legenda, CRT, CTA) apenas quando for desenvolver a biblioteca de motion; **não inventariar 44 skills** como pré-requisito do plugin.
- [x] **A04 — CONCLUÍDA E REVISADA (2026-11-10):** explicitado em `docs/ESPECIFICACAO_CANONICA_DIAZVERSO_V1.md` e `AGENTS.md` que o Content Lab legado **não integra nem bloqueia** o plugin V1; sua refatoração será **posterior à conclusão e validação** do plugin. Adaptador futuro, se necessário, será opcional com contrato novo. **5/5 critérios de coerência e leitura de retorno aprovados**; nenhum código ou contrato do Content Lab legado foi importado.
- [ ] **A05** — Validar visualmente `Nox.png` atual e confirmar consistência com a marca V1, sem herdar restrições do Character Lock antigo automaticamente.
- [x] **A06 — CONCLUÍDA E REVISADA (2026-11-10):** criada `docs/MATRIZ_CAPACIDADES_E_PERMISSOES_V1.md` com separação ChatGPT/conectores vs Work/Codex/executor Remotion, requisitos reais de autorização, distinção planejado/estático/executado, Nox e bloqueio B06. **9/9 verificações no documento e 4/4 na integração condicional com `diazverso-setup`**; arquivos relidos no GitHub. Não é teste de host nem habilitação automática de ferramentas.
- [x] **A07 — CONCLUÍDA E REVISADA (2026-11-10, fluxo via conector GitHub):** testada seleção/recuperação da microtarefa A06 a partir do roadmap e leitura somente de `AGENTS.md` + matriz de capacidades relevante, com **7/7 critérios de fonte/gate e 5/5 de conferência de registro aprovados**. Evidência em [TESTE_A07_PROGRESSIVO.md](TESTE_A07_PROGRESSIVO.md). **Não equivale a teste da skill instalada, retomada multi-sessão ou economia medida de tokens** (B06/C06/C07/L04 pendentes).

**Gate A:** a escolha oficial de criadores de plugin/skills está documentada; a validação de funcionamento do **pacote** virá em B04/B06. A02/A05/A06/A07 podem ser executadas em pequenas tarefas próprias, e A03/A04 NÃO bloqueiam o início da consolidação do plugin.

### Fase B — Plugin instalável mínimo

- [x] **B01** — **CONCLUÍDO EM 2026-11-10:** `plugin.json` raiz criado (`diazverso`, `0.1.0`, schema **Agent Plugins 1.0**). JSON parseado, campos essenciais, shortDescription ≤30 caracteres, ausência de MCP inventado e leitura de volta no GitHub validados. **Ainda não instalável/operacional sozinho: precisa de pelo menos uma skill B02.**
- [x] **B02** — **CONCLUÍDA EM 2026-11-10:** `skills/diazverso-setup/SKILL.md` criado e relido via GitHub; frontmatter `name`/`description`, localização portátil e tamanho validados. A skill diagnostica conexões/permissões e indica uma próxima tarefa, sem prometer render ou exigir Content Lab. **Teste real de instalação/invocação permanece em B04/B06.**
- [x] **B03 — CONCLUÍDA E REVISADA (2026-11-10):** `skills/diazverso-core/SKILL.md` criado com núcleo editorial/visual enxuto, Nox canônico ainda não empacotado, direção Shorts 9:16, referências FALL/Um Nerd/RunnyIA e **revisão obrigatória ao fim de cada tarefa**. **Revisão posterior à criação: 14/14 verificações aprovadas** (frontmatter/pasta, links reais de 4 referências, tamanho, limites das capacidades, separação da setup, decisões atuais/hipóteses, independência do Content Lab antigo, revisão antes de avançar). **Não equivale a instalação/invocação no host.**
- [x] **B04 — CONCLUÍDA E REVISADA EM 2026-11-10:** `plugin.json`, `skills/diazverso-setup/SKILL.md` e `skills/diazverso-core/SKILL.md` comparados com as regras atuais do Plugin Creator oficial (Agent Plugins 1.0 + Agent Skills). **Primeira rodada: 18/18 verificações passaram** (JSON/schema/nome/versão, metadados, localização, frontmatter, nomes únicos, funções distintas, referências existentes, limites e QA). **Revisão independente: 17/17 critérios aprovados após corrigir dois falsos positivos do validador** que confundia nomes de arquivos `docs/*.md` com IDs do Drive; scanner refinado confirmou nenhum ID de conta codificado. **Nenhuma alteração necessária nas skills.** Limites: empacotamento de docs, instalação e invocação em ChatGPT/Codex ainda não testados (B05/B06); `Nox.png` ainda não importado (D01). Evidências obtidas por leitura de volta dos três arquivos no GitHub e testes estáticos em duas passagens. **PRÓXIMA B05; não executada.**
- [x] **B05 — CONCLUÍDA E REVISADA EM 2026-11-10:** confirmado nas [regras oficiais de empacotamento](https://developers.openai.com/plugins/build/plugins) que o manifesto raiz portátil Agent Plugins 1.0 e as skills em `skills/<nome>/SKILL.md` são compartilháveis por ChatGPT/Codex; o overlay `.codex-plugin/plugin.json` é **opcional e dispensável** neste momento. Acrescentado `extensions.com.openai.onboardingSkill="./skills/diazverso-setup/SKILL.md"` ao `plugin.json`, preservando os demais campos. **Revisão independente: 12/12 verificações positivas** do manifesto atualizado, caminhos/skills, ausência de conflitos/duplicações e recursos ainda não empacotados. Contrato: [EMPACOTAMENTO_PORTATIL_DIAZVERSO_V1.md](EMPACOTAMENTO_PORTATIL_DIAZVERSO_V1.md). **Nenhum ZIP/instalação/acionamento no host testado nesta etapa. Próxima: B06.**
- [x] **B06 — CONCLUÍDA NO ESCOPO DE DESENVOLVIMENTO (2026-11-10, requisito corrigido pelo criador):** preparar ZIP de teste, verificar manifesto, skills, Nox, licenças e integridade no CI **SEM instalar no ChatGPT/Codex**. Smoke mínimo [CI 42898444365](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42898444365) verde, pacote completo [CI 42903890655](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42903890655) verde; os testes são de empacotamento, não de edição ou funcionamento nos hosts. **Instalar o ZIP NÃO é tarefa de desenvolvimento e será ação exclusiva do criador após a V1 estar completa, limpa e validada.** Se o conteúdo mudar, reexecutar CI de pacote antes da entrega final.

**Gate B (desenvolvimento):** manifesto, duas skills básicas e ZIP mínimo/completo validados estaticamente e no CI. **Nenhuma instalação no ChatGPT ou Codex agora.**

### Fase C — Economia de tokens e orquestração

- [x] **C01 — CONCLUÍDA E REVISADA (2026-11-10):** criada `skills/diazverso-contexto-eficiente/SKILL.md` (9/9 verificações de leitura, frontmatter, links de recursos, economia de contexto e gate). **Skill externa `context-optimization` incorporada integralmente no pacote-fonte**, com `SKILL.md`, referência e licença MIT original preservadas; conteúdos relidos e comparados byte a byte em texto com os arquivos GitHub de origem (3/3). Medição real de tokens continua pendente em C07. Licença/segurança de outras skills ainda em avaliação.
- [x] **C02 — CONCLUÍDA E REVISADA (2026-11-10):** criada `skills/diazverso-contexto-eficiente/references/roteamento.md`, conectada sob demanda ao SKILL.md. Regra de **uma skill principal por microtarefa**, auxiliares condicionalmente, metadados primeiro e referências depois; funções futuras explicitamente não apresentadas como disponíveis. **7/7 critérios documentais e leitura de retorno aprovados**. Testes reais de roteamento em host ficam em C06/B06.
- [x] **C03 — CONCLUÍDA E REVISADA (2026-11-10):** `skills/diazverso-criacao-video/SKILL.md` criado para pedidos 'vamos criar um vídeo', escolha de uma microtarefa, fases Ideias → Produções → roteiro → assets → edição/QA → publicação e revisão antes de seguir. **9/9 verificações aprovadas**, arquivo relido no GitHub. Não declara integração Drive/Remotion/YouTube já existente; testes de runtime pendentes.
- [x] **C04 — CONCLUÍDA E REVISADA (2026-11-10):** `schemas/estado-producao-v1.schema.json` com ID TF/VD/SH, tipo, fase, próxima microtarefa, revisão/evidência, links, bloqueio e data; integração por referência na orquestradora. **8/8 checagens do schema + 4/4 verificações de integração aprovadas**, com arquivos relidos do GitHub. Schema é formato de intercâmbio, **não persistência real**; Google Sheets e Docs seguem fonte de verdade. Integração real/testes multi-sessão pendentes em E/L.
- [x] **C05 — CONCLUÍDA E REVISADA (2026-11-10):** criada `skills/diazverso-criacao-video/references/intencoes.md` com intenções de ideias, títulos, roteiro, revisão, thumbnail, Nox, TSX/motion, música/SFX, Short, publicação, Drive e tokens. Orquestradora aponta para a tabela **somente sob demanda**. **6/6 critérios documentais + 4/4 de integração aprovados**, arquivos relidos do GitHub; funcionalidades especializadas ainda ausentes marcadas explicitamente. Teste de host continua C06/B06.
- [ ] **C06** — Testar 12 pedidos isolados com seleção de skill correta e sem carregamento de módulos irrelevantes.
- [ ] **C07** — Comparar consumo real de tokens/contexto antes/depois com pelo menos 3 tarefas iguais; ajustar os módulos grandes.

**Gate C:** o agente retoma o estado e executa **somente a próxima subtarefa**, com redução de contexto **demonstrada**, sem percentual prometido.

### Fase D — Assets essenciais embutidos no plugin

- [x] **D01 — CONCLUÍDA E REVISADA (2026-11-10):** `assets/brand/nox/Nox.png` copiado **em bytes originais** do Google Drive (ID da instância existente), via blob Git SHA `776d1b26983e6f9095178881c83b44f114a40336` e commit `15438eea2f76a0f72bc56ae13df2aa2a96b5630c`. Origem e destino: **415.179 bytes**. Auditoria estrutural do PNG: assinatura válida, IHDR **1408×768 RGBA (alfa suportado)**, blocos IHDR/pHYs/IDAT/IEND presentes, **0 erros de CRC**, fim consistente. Commit inspecionado: único arquivo novo `assets/brand/nox/Nox.png`. **Visualização do personagem e poses ficará para A05/G01; ainda não foi feito teste gráfico de novas poses.**
- [x] **D02 — CONCLUÍDA E REVISADA (2026-11-10):** `assets/brand/nox/README.md` criado com caminho e Git blob verificáveis, Character Lock **mínimo baseado nas decisões atuais**, variantes de expressão contextuais, proibição de redesenhar/alterar o canônico e gate de comparação visual sem alegar revisão de poses já executada. **7/7 verificações documentais aprovadas**, arquivo relido no GitHub.
- [ ] **D03** — Selecionar 2–5 fundos HQ realmente aprovados no Drive e registrar origem/uso; **não importar todos os backgrounds**.
- [ ] **D04** — Adicionar os backgrounds aprovados em `assets/brand/backgrounds/` com nomenclatura e leitura testadas, se os direitos permitirem empacotamento.
- [ ] **D05** — Escolher SFX essenciais (whoosh curto/longo, ding, boom, riser), ouvir, medir duração, verificar licença e decidir quais podem ser embutidos em `assets/sfx/`.
- [x] **D06 — CONCLUÍDA E REVISADA (2026-11-10):** `assets/manifest.json` com Nox canônico (PNG RGBA, dimensões, tamanho, Git blob SHA, origem, direitos limitados e caminho local). Não inclui mídia externa sem licença confirmada. **8/8 verificações de consistência, limites e readback aprovadas.** Novos assets entrarão apenas após revisão individual; ID do Drive da conta atual não aparece no manifesto do plugin.
- [ ] **D07** — Testar acesso à mídia **sem Google Drive** para garantir que Nox e recursos essenciais funcionem offline no editor capaz.

**Gate D:** `Nox.png` real e pequeno conjunto de recursos aprovados empacotados e recuperáveis, sem redistribuição não autorizada.

### Fase E — Google Drive e planilha sem intervenção repetitiva

- [x] **E01 — CONCLUÍDA E REVISADA (2026-11-10):** `skills/diazverso-drive-setup/SKILL.md` criada, com descoberta de Drive por conta, quatro subpastas essenciais, bibliotecas opcionais, validação de Produções/Ideias/Afiliados/Config, autorização prévia, verificação de IDs, leitura de volta e reporte honesto. **9/9 critérios de revisão documental aprovados** e arquivo relido no GitHub. Operações idempotentes reais E02/E03 ainda não implementadas/testadas.
- [ ] **E02** — Criar detecção idempotente de `Diazverso` e subpastas (não duplicar quando já existem).
- [ ] **E03** — Implementar reparo/criação autorizada de estruturas **faltantes**, mantendo IDs específicos da conta, sem hardcode universal.
- [ ] **E04** — Criar validador das abas e colunas `Produções`, `Ideias`, `Afiliados`, `Config`; reparar formatação/validações sem destruir conteúdo.
- [ ] **E05** — Implementar criação de ideia com ID TF único e linha formatada.
- [ ] **E06** — Implementar promoção de ideia: criar produção VD/SH, verificar gravação, preservar origem; **só então excluir linha TF da aba Ideias**.
- [ ] **E07** — Testar falha no meio da promoção e repetição: nenhum vídeo duplicado, nenhuma ideia perdida.
- [ ] **E08** — Implementar `upsert` de títulos A/B, links diretos de Docs e arquivos de thumbnail, status e URL publicada.

**Gate E:** em conta preparada, ChatGPT atualiza arquivos e planilha corretamente sem o usuário pedir localização/formatação duas vezes.

### Fase F — Pesquisa, títulos, roteiros e revisões editoriais

- [x] **F01 — CONCLUÍDA E REVISADA (2026-11-10):** criada `skills/diazverso-pesquisa/SKILL.md` com pesquisa baseada em fontes, distinção fato/interpretação/pendência, contraponto, briefing, gate editorial e inserção condicional na aba Ideias. **9/9 verificações documentais aprovadas**, leitura de retorno confirmada. Pesquisa em fontes reais será testada ao executar uma pauta.
- [x] **F02 — CONCLUÍDA E REVISADA (2026-11-10):** criada `skills/diazverso-titulos/SKILL.md` com título A/B substancialmente diferente, conceitos de thumbnail correspondentes, promessa de gancho, avaliação factual e vidIQ opcional. **9/9 verificações documentais aprovadas** com leitura de retorno; testes com público/CTR reais não alegados.
- [x] **F03 — CONCLUÍDA E REVISADA (2026-11-10):** `skills/diazverso-revisao-embalagem/SKILL.md` criada, compara título A/B, conceito de thumbnail e gancho contra a tese e evidências, com gate APROVAR/REVISAR/REPROVAR. **9/9 checagens documentais aprovadas**, relida no GitHub. Ainda não é medição real de CTR/retenção.
- [x] **F04 — CONCLUÍDA E REVISADA (2026-11-10):** criado novo Google Doc nativo **MODELO (não publicar) — Roteiro Longo — Diazverso V1** em `Roteiros/Longos`, sem alterar roteiros históricos. Leitura de retorno confirmou **48 parágrafos não vazios**, TITLE, SUBTITLE, 6 HEADING_1 e 4 HEADING_2, distinção NARRAÇÃO/SOM DA CENA, fontes, QA audiovisual `NÃO TESTADO`, aprovação do criador `PENDENTE` e kit de publicação não narrado; **11/11 critérios iniciais + 4/4 ajustes de gate aprovados**. O blueprint portátil `templates/roteiro-longo-v1.json` foi reconciliado com a versão nativa, preservando estilos e sem ID da conta no pacote; **7/7 verificações**. Empacotador inclui e valida templates; [CI completo verde](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42897236656). **Validação por estilos nativos; não foi feita inspeção visual PDF de paginação.**
- [x] **F05 — CONCLUÍDA E REVISADA (2026-11-10):** criado o Google Doc nativo **MODELO (não publicar) — Roteiro Short — Diazverso V1** na pasta `Roteiros/Shorts`, sem alterar Shorts publicados; **44 parágrafos não vazios**, TITLE/SUBTITLE, 6 HEADING_1, 4 HEADING_2, hook, prova, payoff, CTA, NARRAÇÃO e SOM DA CENA separados, 9:16, preferência ≥60 s, legendas e aprovação PENDENTE. **14/14 verificações de leitura/estilos/permissão aprovadas**. Blueprint portátil `templates/roteiro-short-v1.json` criado sem IDs pessoais, **7/7 checagens**; [ZIP completo verde](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42897749304), **68 arquivos** e SHA-256 registrado no CI. Não houve inspeção de paginação via PDF nem instalação no host.
- [ ] **F06 — PARCIAL, NÃO CONCLUIR ANTES DA INTEGRAÇÃO REAL (auditoria 2026-11-10):** `skills/diazverso-roteiro/SKILL.md` criada; `scripts/build_requests.py` gera requisições de formatação Docs com índices UTF-16 e validação de IDs/tema; `tests/test_build_requests.py` tem **7/7 testes aprovados** no [GitHub Actions run 42898526361](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42898526361), além de amostras LONGO/SHORT (`REQUESTS_VALIDATED 21 21`). **FALTA:** executar fluxo real com vídeo de teste, criar/mover/formatar o Doc na pasta correta, conferir estilos e fazer upsert do link na célula ROTEIRO da linha exata em `Produções`, reler a planilha, testar repetição sem duplicidade e falha intermediária. Testes geram requests, **não efetuam gravação no Drive/Sheets**; manter `[ ]`.
- [x] **F07 — CONCLUÍDA E REVISADA (2026-11-11, escopo documental/skill):** criada `skills/diazverso-revisao-fatos/SKILL.md` para extrair alegações por versão/cânone, distinguir FATO/INTERPRETAÇÃO/OPINIÃO/HIPÓTESE, exigir fonte rastreável ou marcar NÃO VERIFICADO, confrontar títulos A/B–thumbnail–gancho–payoff e bloquear promessa não sustentada. Inclui formato de achados, ações, limites de ferramentas e proibição de aprovação fictícia em Sheets. **Leitura de volta no GitHub e 9/9 verificações estáticas aprovadas**; commit `906de8930ba657033311bcff4e943271c045ac5a`. **Não houve teste de invocação no host nem revisão factual de roteiro real**; testes integrados continuam pendentes em L. Próxima independente: F08.
- [x] **F08 — CONCLUÍDA E REVISADA (2026-11-11, escopo documental/skill):** criada `skills/diazverso-revisao-estrutura/SKILL.md` com sete passagens de revisão: promessa/payoff, gancho, progressão, ritmo conversacional, redundância, duração proporcional e fechamento/CTA. Gera diagnóstico por trecho e encaminha afirmações alteradas para F07; trata retenção potencial como hipótese, sem métricas inventadas. **Leitura de volta e 10/10 verificações estáticas aprovadas**; commit `752dc4e1047b44ca09167583f6f6c0b1aafcafe3`. **Não houve teste de invocação no host nem aplicação a roteiro real**. Próxima independente: F09.
- [ ] **F09** — Criar revisor de voz/humanização (sarcasmo natural e conversa autêntica, sem artificializar).
- [ ] **F10** — Exigir gate de aprovação do roteiro e packaging antes de passar à produção técnica.

**Gate F:** Docs bem formatados já na criação, com auditorias registradas e aprovação real.

### Fase G — Nox, thumbnails e biblioteca TSX

- [ ] **G01** — Criar skill `diazverso-nox` usando `assets/brand/nox/Nox.png` e Character Lock; testar uma pose sem redesign.
- [ ] **G02** — Criar skill de thumbnail baseada na tese, em legibilidade/contraste, composição simples e variantes A/B.
- [ ] **G03** — Criar revisor de thumbnail e validar arquivo final, dimensões, texto, identidade e link do Drive.
- [ ] **G04** — Escolher **um** TSX antigo pequeno (p.ex. `TextoHQ.tsx`), copiar **como exemplo de referência**, documentando dependências e diferenças da API atual.
- [ ] **G05** — Compilar e renderizar uma cena baseada no exemplo escolhido em projeto de teste **Remotion independente**, sem depender do Content Lab antigo; revisar quadros 16:9 e 9:16.
- [ ] **G06** — Migrar seletivamente `BackgroundHQ.tsx` e `QuadroHQSobreCena.tsx`, cada um em tarefa/PR separado, após validação.
- [ ] **G07** — Auditar `PersonagemEspiralLegenda.tsx` e `ComicPageCTA.tsx` (legendas/CTA) **sem tornar espiral e balões padrão obrigatório**.
- [ ] **G08** — Consolidar `HQMotion.tsx`/`HQComicPage.tsx` e dependências em biblioteca única quando necessário; **não copiar as inúmeras cópias de 885 KB** indiscriminadamente.

**Gate G:** Nox e components de edição disponíveis/compiláveis; exemplos antigos não substituem critérios editoriais novos.

### Fase H — Produção audiovisual por microcena

- [ ] **H01** — Definir **contrato independente de composição Remotion** para o plugin (props TSX, assets, timeline e outputs) sem exigir integração com o Content Lab antigo; refatoração do Content Lab pertence à etapa pós-plugin.
- [ ] **H02** — Criar skill de decupagem audiovisual: blocos curtos, quadro-alvo, narração, mídia, SFX, música e objetivo de cada cena.
- [ ] **H03** — Criar componentes/testes de câmera em imagens estáticas: zoom/pan/reframe/blur, evitando imagem parada e vazios involuntários.
- [ ] **H04** — Criar componente/teste de parallax em camadas, com fundo e PNG recortado; verificar escala/safe area.
- [ ] **H05** — Criar componente/teste de texto cinético Anton, com contraste real e timing de palavras.
- [ ] **H06** — Criar tratamento de painéis de filme/TV com CRT perceptível, áudio de trecho quando autorizado e moldura contextual; respeitar uso de conteúdo de terceiros.
- [ ] **H07** — Criar seleção contextual de música/SFX a partir da biblioteca aprovada; volume/ducking/sincronização verificados.
- [ ] **H08** — Implementar render **por trecho** e preview automatizado antes do render final.
- [ ] **H09** — Validar saída TSX/Remotion em **runtime independente** (Work/Codex quando disponível), definindo interface de integração futura; **não refatorar nem acoplar ao Content Lab antigo antes de fechar a V1.0**.

**Gate H:** cena/trecho renderizado, com saída verificável; não afirmar que ChatGPT comum renderiza sozinho.

### Fase I — Shorts / vertical e legendas

- [ ] **I01** — Definir preset 9:16, resolução, margens e área segura para texto/legenda.
- [ ] **I02** — Criar skill `diazverso-shorts` com gancho forte, alta dinamicidade, CTA final ao canal e preferência atual por vídeo **de pelo menos 60 segundos**.
- [ ] **I03** — Implementar legendas sincronizadas por padrão, exceto nos trechos **exclusivamente de texto na tela** (não duplicar mensagens).
- [ ] **I04** — Testar um exemplo 9:16 com Nox, texto cinético, parallax, whoosh e legenda, revisando amostras de frames.
- [ ] **I05** — Criar revisor de Short: gancho, retenção provável, ritmo, legenda, áudio, CTA, segurança de enquadramento e links.

**Gate I:** vídeo vertical demonstrável, dinâmico e legível, não mero recorte de um longo.

### Fase J — Revisão obrigatória e QA independente

- [ ] **J01** — Criar revisor de código/JSON/TSX: tipos, contrato Remotion, props, assets, duração e render.
- [ ] **J02** — Criar extrator de quadros em tempos/frames representativos, incluindo entradas, transições, poses e final da cena.
- [ ] **J03** — Criar revisor visual: cortes, parallax, fluidez, legibilidade, erros de fundo, composição, Nox e consistência gráfica.
- [ ] **J04** — Criar revisor de áudio: voz, música, clipping, pausas, SFX e sincronização; considerar EarShot **após instalar e testar**.
- [ ] **J05** — Criar revisor de pacing/engajamento: cenas longas demais, redundâncias, reviravoltas e timing de CTA, com achados verificáveis e sem afirmar previsão do algoritmo.
- [ ] **J06** — Criar revisor de licenças: mídia/áudio, uso de clips, afiliação, direitos e Content ID. Espelhamento, CRT ou moldura **não neutralizam copyright**.
- [ ] **J07** — Criar loop de correção: classificar achados, corrigir **um problema por tarefa**, renderizar novamente e reexecutar a revisão afetada.
- [ ] **J08** — Criar checklist de aprovação humana antes do pacote de publicação; gates só recebem `APROVADO` com evidência.

**Gate J:** revisões visuais e auditivas reais com provas; `NÃO_VERIFICADO` impede falso encerramento.

### Fase K — Publicação e aprendizado

- [ ] **K01** — Gerar kit de publicação após aprovação do vídeo: título, descrição, fontes, tags, comentário, capítulos reais e texto social.
- [ ] **K02** — Selecionar produtos da aba `Afiliados` apenas se adequados e verificados; acrescentar divulgação quando necessária.
- [ ] **K03** — Testar atualização da planilha por status, título/link e data; não marcar `PUBLICADO` sem confirmação da publicação real.
- [ ] **K04** — Integrar envio/publicação **apenas mediante permissão** (Work/browser/Content Lab quando disponível) ou instruir postagem manual.
- [ ] **K05** — Criar rotina de análise de métricas reais pós-publicação e envio de novas hipóteses para Ideias.

**Gate K:** kit pronto e status fiel às ações realmente executadas.

### Fase L — Integração, validação e entrega

- [ ] **L01** — Teste de fluxo com **conectores reais disponíveis e/ou ambiente controlado de desenvolvimento**, da ideia ao Doc e links de thumbnails, sem instalar o plugin no ChatGPT; registrar limites e evidências da escrita/leitura.
- [ ] **L02** — Teste de execução **Work/Codex + Remotion independente, quando disponível**: roteiro → decupagem → TSX → render 16:9 → QA; sem Content Lab antigo.
- [ ] **L03** — Teste completo **Short** 9:16 com legendas/CTA e QA independente.
- [ ] **L04** — Teste de retomada: interromper e reabrir em nova sessão; recuperar a próxima microtarefa sem recomeçar nem duplicar.
- [ ] **L05** — Teste de host sem Drive / sem runtime de render / sem EarShot: degradação transparente e somente funcionalidades possíveis.
- [ ] **L06** — Validar ZIP final offline com ferramentas de build, schemas, testes e revisão de conteúdo: manifesto, skills externas, licenças, templates, Nox e integridade; **não instalar o plugin no ChatGPT/Codex**.
- [ ] **L07** — Consolidar README mínimo para instalação **manual futura pelo criador**, recursos, limites e requisitos; limpar rascunhos e atualizar referências, gerar ZIP final, testar novamente CI e só então declarar V1.0 pronta **para o criador instalar**.

**Gate L:** fluxos comprovados por testes de desenvolvimento/integração e renders reais quando possíveis, pacote ZIP íntegro e independente de rascunhos, exemplos reproduzíveis e limites documentados. **A instalação manual do usuário acontece depois da entrega, não é gate de desenvolvimento.**

## 3. Ordem recomendada de entregas demonstráveis

**Marco 1 — Plugin mínimo:** **A01 validada → B → C**, com A02/A05/A06/A07 executadas conforme surgirem dependências. Resultado: pacote verificável e empacotável, roteador, contexto eficiente e uma tarefa por vez; **sem instalação nesta fase**. Não aguardar auditoria das 44 skills antigas.

**Marco 2 — Produto editorial:** D → E → F → G01–G03. Resultado: Nox embutido, Google Drive/Sheets e roteiro/thumb com revisores, mesmo sem render autônomo.

**Marco 3 — Motion:** G04–G08 → H → J (QA parcial). Resultado: TSX selecionado e testado **contra Remotion independente**, sem requisito de Content Lab.

**Marco 4 — Shorts e finalização:** I → J completo → K → L. Resultado: edição vertical/horizontal, legenda, áudio, QA e publicação assistida quando possível.

**Microtarefas A01 e B01 concluídas:** criador oficial escolhido e manifesto raiz `plugin.json` criado/validado. **B03 criada e aprovada na revisão de arquivo (14/14 verificações). PRÓXIMA: B04 — validação do conjunto e da especificação Agent Skills.** Não executada nesta etapa. **Nox.png** permanece obrigatório em D01, assim que o esqueleto básico estiver validado. **A03 inventário seletivo do TSX antigo** somente quando começar motion; não catalogar as 44 skills como bloqueio.

## 4. Fontes externas — status de uso

O **Plugin Creator oficial** foi encontrado **instalado e lido no ambiente**, e suas regras de pacote portátil foram comparadas com as páginas oficiais OpenAI Plugins e Agent Skills em 2026-11-10. Isso valida a **escolha da metodologia**, não um pacote instalado/testado. **Skill Creator** está documentado como mecanismo oficial em ChatGPT/Codex, mas sua disponibilidade deve ser conferida em cada host. Superpowers/Context Engineering/Remotion serão aplicados seletivamente. Não presumir instalação de Iris/EarShot ou runtime de render.

### Critério de sucesso central

Quando o criador disser **“Chat, vamos criar um vídeo sobre [tema]”**, o plugin deverá: identificar o projeto e as autorizações, localizar/registrar produção, dar **uma próxima subtarefa clara**, executar quando houver ferramenta, atualizar estado e avançar somente após o gate correspondente — até o roteiro, thumbnail, vídeo renderizado/revisado e publicação assistida. **O plugin não pode fingir que realizou qualquer etapa não executada.**
