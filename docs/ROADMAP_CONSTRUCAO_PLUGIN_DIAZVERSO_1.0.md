# Diazverso Plugin 1.0 — Roadmap de implementação em microtarefas

**Data:** 2026-11-10  
**Estado:** ROADMAP PARA EXECUÇÃO. Nenhum item deste roadmap equivale, sozinho, à funcionalidade implementada.  
**Destino:** [repositório novo](https://github.com/DanielHABDias/DiazVerso-Plugin).  
**Objetivo:** um plugin instalável para ChatGPT e Codex baseado **nas decisões de 2026-11-10**, que coordene em microtarefas pesquisa → tese/packaging → roteiro formatado → thumbnails → narração/assets → instruções e exemplos Remotion/TSX independentes → revisão audiovisual → kit de publicação. **Content Lab antigo é obsoleto e sua refatoração será um projeto separado, após o novo plugin estar concluído.** O fluxo completo depende das ferramentas e autorizações reais do host.

> **CORREÇÃO DE PRIORIDADE 2026-11-10:** o trabalho editorial/operacional definido **hoje** prevalece. Plugin antigo e Content Lab antigo são obsoletos; consultar só ideias e exemplos TSX relevantes. **Refatoração do Content Lab é posterior à conclusão do novo plugin**, não pré-requisito. Criador de plugin selecionado: **OpenAI Plugin Creator oficial**; criação de skills orientada pelo **Skill Creator oficial** e padrão Agent Skills. Microtarefas e gates preservados.

## 0. Regras de execução (obrigatórias)
**Atualização de governança (2026-11-10):** criador autorizou seguir automaticamente para microtarefas elegíveis após revisão, sem pedir 'próximo'. **B06 permanece `[ ]` enquanto não houver instalação/invocação real**; por instrução nova, é permitido trabalhar em tarefas **independentes**, marcando-as individualmente somente após revisão. Skills externas selecionadas serão **vendorizadas dentro do plugin quando a licença autorizar**, com referências e licenças; sem licença, adaptar de forma autoral sem copiar arquivos. Documentos temporários serão removidos **somente após release 1.0 completa, validada e com o conhecimento migrado**, não durante as fases de implementação. Registrar impedimentos em [REGISTRO_EXECUCAO_E_PENDENCIAS.md](REGISTRO_EXECUCAO_E_PENDENCIAS.md).


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
- [ ] **A02** — Escrever a **fonte canônica resumida da V1.0** a partir das decisões de **hoje** (identidade editorial e audiovisual ainda ajustável, Drive/planilha aprovados, Nox, Shorts, QA, economia de contexto). Não usar plugin anterior como baseline.
- [ ] **A03** — Montar **catálogo seletivo** de poucos TSX antigos relevantes (texto, fundos, Nox, legenda, CRT, CTA) apenas quando for desenvolver a biblioteca de motion; **não inventariar 44 skills** como pré-requisito do plugin.
- [ ] **A04** — Registrar o Content Lab como **projeto de refatoração posterior à conclusão do plugin novo**, sem auditar/copiar seu contrato técnico agora; a V1 pode prever uma interface/adaptador **opcional**, sem implementação.
- [ ] **A05** — Validar visualmente `Nox.png` atual e confirmar consistência com a marca V1, sem herdar restrições do Character Lock antigo automaticamente.
- [ ] **A06** — Definir funcionalidades disponíveis no ChatGPT normal por conexão com Drive/Sheets e as que exigem runtime de execução (Codex/Work/Remotion); não assumir que o antigo Content Lab está ativo.
- [ ] **A07** — Testar um fluxo mínimo de uma microtarefa com carregamento progressivo e fonte de verdade no GitHub.

**Gate A:** a escolha oficial de criadores de plugin/skills está documentada; a validação de funcionamento do **pacote** virá em B04/B06. A02/A05/A06/A07 podem ser executadas em pequenas tarefas próprias, e A03/A04 NÃO bloqueiam o início da consolidação do plugin.

### Fase B — Plugin instalável mínimo

- [x] **B01** — **CONCLUÍDO EM 2026-11-10:** `plugin.json` raiz criado (`diazverso`, `0.1.0`, schema **Agent Plugins 1.0**). JSON parseado, campos essenciais, shortDescription ≤30 caracteres, ausência de MCP inventado e leitura de volta no GitHub validados. **Ainda não instalável/operacional sozinho: precisa de pelo menos uma skill B02.**
- [x] **B02** — **CONCLUÍDA EM 2026-11-10:** `skills/diazverso-setup/SKILL.md` criado e relido via GitHub; frontmatter `name`/`description`, localização portátil e tamanho validados. A skill diagnostica conexões/permissões e indica uma próxima tarefa, sem prometer render ou exigir Content Lab. **Teste real de instalação/invocação permanece em B04/B06.**
- [x] **B03 — CONCLUÍDA E REVISADA (2026-11-10):** `skills/diazverso-core/SKILL.md` criado com núcleo editorial/visual enxuto, Nox canônico ainda não empacotado, direção Shorts 9:16, referências FALL/Um Nerd/RunnyIA e **revisão obrigatória ao fim de cada tarefa**. **Revisão posterior à criação: 14/14 verificações aprovadas** (frontmatter/pasta, links reais de 4 referências, tamanho, limites das capacidades, separação da setup, decisões atuais/hipóteses, independência do Content Lab antigo, revisão antes de avançar). **Não equivale a instalação/invocação no host.**
- [x] **B04 — CONCLUÍDA E REVISADA EM 2026-11-10:** `plugin.json`, `skills/diazverso-setup/SKILL.md` e `skills/diazverso-core/SKILL.md` comparados com as regras atuais do Plugin Creator oficial (Agent Plugins 1.0 + Agent Skills). **Primeira rodada: 18/18 verificações passaram** (JSON/schema/nome/versão, metadados, localização, frontmatter, nomes únicos, funções distintas, referências existentes, limites e QA). **Revisão independente: 17/17 critérios aprovados após corrigir dois falsos positivos do validador** que confundia nomes de arquivos `docs/*.md` com IDs do Drive; scanner refinado confirmou nenhum ID de conta codificado. **Nenhuma alteração necessária nas skills.** Limites: empacotamento de docs, instalação e invocação em ChatGPT/Codex ainda não testados (B05/B06); `Nox.png` ainda não importado (D01). Evidências obtidas por leitura de volta dos três arquivos no GitHub e testes estáticos em duas passagens. **PRÓXIMA B05; não executada.**
- [x] **B05 — CONCLUÍDA E REVISADA EM 2026-11-10:** confirmado nas [regras oficiais de empacotamento](https://developers.openai.com/plugins/build/plugins) que o manifesto raiz portátil Agent Plugins 1.0 e as skills em `skills/<nome>/SKILL.md` são compartilháveis por ChatGPT/Codex; o overlay `.codex-plugin/plugin.json` é **opcional e dispensável** neste momento. Acrescentado `extensions.com.openai.onboardingSkill="./skills/diazverso-setup/SKILL.md"` ao `plugin.json`, preservando os demais campos. **Revisão independente: 12/12 verificações positivas** do manifesto atualizado, caminhos/skills, ausência de conflitos/duplicações e recursos ainda não empacotados. Contrato: [EMPACOTAMENTO_PORTATIL_DIAZVERSO_V1.md](EMPACOTAMENTO_PORTATIL_DIAZVERSO_V1.md). **Nenhum ZIP/instalação/acionamento no host testado nesta etapa. Próxima: B06.**
- [ ] **B06 — EM ANDAMENTO, BLOQUEADA NO GATE DE RUNTIME (2026-11-10):** criados [script Python de empacotamento](../scripts/b06_package_smoke.py), [workflow GitHub Actions](../.github/workflows/b06-plugin-smoke.yml) e [relatório de teste](TESTE_B06_PLUGIN.md). **Revisão estática 21/21 PASSOU**; arquivos gravados e relidos. **FALTAM execução comprovada do script/workflow, ZIP inspecionado e teste real de instalação/invocação no ChatGPT e Codex.** Ferramentas de runtime/instalação não estavam disponíveis nesta sessão. **Não marcar [x] nem iniciar outra tarefa enquanto o gate não for satisfeito.**

**Gate B:** plugin mínimo instalado **e testado**, ainda sem afirmar que edita vídeos.

### Fase C — Economia de tokens e orquestração

- [x] **C01 — CONCLUÍDA E REVISADA (2026-11-10):** criada `skills/diazverso-contexto-eficiente/SKILL.md` (9/9 verificações de leitura, frontmatter, links de recursos, economia de contexto e gate). **Skill externa `context-optimization` incorporada integralmente no pacote-fonte**, com `SKILL.md`, referência e licença MIT original preservadas; conteúdos relidos e comparados byte a byte em texto com os arquivos GitHub de origem (3/3). Medição real de tokens continua pendente em C07. Licença/segurança de outras skills ainda em avaliação.
- [x] **C02 — CONCLUÍDA E REVISADA (2026-11-10):** criada `skills/diazverso-contexto-eficiente/references/roteamento.md`, conectada sob demanda ao SKILL.md. Regra de **uma skill principal por microtarefa**, auxiliares condicionalmente, metadados primeiro e referências depois; funções futuras explicitamente não apresentadas como disponíveis. **7/7 critérios documentais e leitura de retorno aprovados**. Testes reais de roteamento em host ficam em C06/B06.
- [x] **C03 — CONCLUÍDA E REVISADA (2026-11-10):** `skills/diazverso-criacao-video/SKILL.md` criado para pedidos 'vamos criar um vídeo', escolha de uma microtarefa, fases Ideias → Produções → roteiro → assets → edição/QA → publicação e revisão antes de seguir. **9/9 verificações aprovadas**, arquivo relido no GitHub. Não declara integração Drive/Remotion/YouTube já existente; testes de runtime pendentes.
- [ ] **C04** — Definir estrutura mínima de estado da produção e retomada entre sessões (ID, fase, links e pendência); fonte de verdade em Sheets/Docs/GitHub conforme etapa.
- [ ] **C05** — Criar roteamento por intenção: ideias, títulos, roteiro, revisão, thumb, Nox, motion, áudio, Short, publicação.
- [ ] **C06** — Testar 12 pedidos isolados com seleção de skill correta e sem carregamento de módulos irrelevantes.
- [ ] **C07** — Comparar consumo real de tokens/contexto antes/depois com pelo menos 3 tarefas iguais; ajustar os módulos grandes.

**Gate C:** o agente retoma o estado e executa **somente a próxima subtarefa**, com redução de contexto **demonstrada**, sem percentual prometido.

### Fase D — Assets essenciais embutidos no plugin

- [ ] **D01** — Copiar o `Nox.png` canônico **fisicamente** do Drive para `assets/brand/nox/Nox.png` no repositório do plugin; verificar tamanho/hash, transparência e abertura.
- [ ] **D02** — Criar `assets/brand/nox/README.md` curto com Character Lock, variantes permitidas e uso da referência visual; não reestilizar automaticamente.
- [ ] **D03** — Selecionar 2–5 fundos HQ realmente aprovados no Drive e registrar origem/uso; **não importar todos os backgrounds**.
- [ ] **D04** — Adicionar os backgrounds aprovados em `assets/brand/backgrounds/` com nomenclatura e leitura testadas, se os direitos permitirem empacotamento.
- [ ] **D05** — Escolher SFX essenciais (whoosh curto/longo, ding, boom, riser), ouvir, medir duração, verificar licença e decidir quais podem ser embutidos em `assets/sfx/`.
- [ ] **D06** — Criar manifesto mínimo de mídia própria/aprovada: nome, função, origem, status de licença, formato, caminho local e Drive quando aplicável.
- [ ] **D07** — Testar acesso à mídia **sem Google Drive** para garantir que Nox e recursos essenciais funcionem offline no editor capaz.

**Gate D:** `Nox.png` real e pequeno conjunto de recursos aprovados empacotados e recuperáveis, sem redistribuição não autorizada.

### Fase E — Google Drive e planilha sem intervenção repetitiva

- [ ] **E01** — Criar skill `diazverso-drive-setup` para localizar conta, raiz, quatro pastas de roteiros/thumbs, cinco bibliotecas opcionais e planilha.
- [ ] **E02** — Criar detecção idempotente de `Diazverso` e subpastas (não duplicar quando já existem).
- [ ] **E03** — Implementar reparo/criação autorizada de estruturas **faltantes**, mantendo IDs específicos da conta, sem hardcode universal.
- [ ] **E04** — Criar validador das abas e colunas `Produções`, `Ideias`, `Afiliados`, `Config`; reparar formatação/validações sem destruir conteúdo.
- [ ] **E05** — Implementar criação de ideia com ID TF único e linha formatada.
- [ ] **E06** — Implementar promoção de ideia: criar produção VD/SH, verificar gravação, preservar origem; **só então excluir linha TF da aba Ideias**.
- [ ] **E07** — Testar falha no meio da promoção e repetição: nenhum vídeo duplicado, nenhuma ideia perdida.
- [ ] **E08** — Implementar `upsert` de títulos A/B, links diretos de Docs e arquivos de thumbnail, status e URL publicada.

**Gate E:** em conta preparada, ChatGPT atualiza arquivos e planilha corretamente sem o usuário pedir localização/formatação duas vezes.

### Fase F — Pesquisa, títulos, roteiros e revisões editoriais

- [ ] **F01** — Criar skill de pesquisa/ideação com evidências, tese e diferenciação (Marvel/DC/Ben 10/cultura pop etc.).
- [ ] **F02** — Criar skill de títulos e packaging A/B, com hipóteses e critérios explícitos de escolha.
- [ ] **F03** — Criar skill de revisão de título + expectativa da thumbnail e promessa dos primeiros segundos.
- [ ] **F04** — Criar template **Google Docs nativo formatado** de roteiro longo e validar hierarquia visual/estilos.
- [ ] **F05** — Criar template **Google Docs nativo formatado** de Short, com blocos específicos e legendas.
- [ ] **F06** — Criar skill `diazverso-roteiro` que gera um Doc pelo template **na pasta certa** e sincroniza o link na planilha.
- [ ] **F07** — Criar revisor de fatos/fontes/promessas sem confundir hipótese com evidência.
- [ ] **F08** — Criar revisor de estrutura/gancho/ritmo e retenção potencial.
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

- [ ] **L01** — Teste completo **ChatGPT comum**: conectores/skills → ideia → produção → Doc formatado → links de thumbnail, com relatório de limites.
- [ ] **L02** — Teste de execução **Work/Codex + Remotion independente, quando disponível**: roteiro → decupagem → TSX → render 16:9 → QA; sem Content Lab antigo.
- [ ] **L03** — Teste completo **Short** 9:16 com legendas/CTA e QA independente.
- [ ] **L04** — Teste de retomada: interromper e reabrir em nova sessão; recuperar a próxima microtarefa sem recomeçar nem duplicar.
- [ ] **L05** — Teste de host sem Drive / sem runtime de render / sem EarShot: degradação transparente e somente funcionalidades possíveis.
- [ ] **L06** — Testar versão final do pacote com Plugin Creator/Codex, incluindo manifesto, skills e Nox; verificar que assets não faltam.
- [ ] **L07** — Consolidar README de instalação, recursos, limites e requisitos/autorizações; só então marcar V1.0 apta a uso.

**Gate L:** fluxo testado por host, pacote instalável, exemplos reproduzíveis e limites documentados.

## 3. Ordem recomendada de entregas demonstráveis

**Marco 1 — Plugin mínimo:** **A01 validada → B → C**, com A02/A05/A06/A07 executadas conforme surgirem dependências. Resultado: pacote instalável, roteador, contexto eficiente e uma tarefa por vez. Não aguardar auditoria das 44 skills antigas.

**Marco 2 — Produto editorial:** D → E → F → G01–G03. Resultado: Nox embutido, Google Drive/Sheets e roteiro/thumb com revisores, mesmo sem render autônomo.

**Marco 3 — Motion:** G04–G08 → H → J (QA parcial). Resultado: TSX selecionado e testado **contra Remotion independente**, sem requisito de Content Lab.

**Marco 4 — Shorts e finalização:** I → J completo → K → L. Resultado: edição vertical/horizontal, legenda, áudio, QA e publicação assistida quando possível.

**Microtarefas A01 e B01 concluídas:** criador oficial escolhido e manifesto raiz `plugin.json` criado/validado. **B03 criada e aprovada na revisão de arquivo (14/14 verificações). PRÓXIMA: B04 — validação do conjunto e da especificação Agent Skills.** Não executada nesta etapa. **Nox.png** permanece obrigatório em D01, assim que o esqueleto básico estiver validado. **A03 inventário seletivo do TSX antigo** somente quando começar motion; não catalogar as 44 skills como bloqueio.

## 4. Fontes externas — status de uso

O **Plugin Creator oficial** foi encontrado **instalado e lido no ambiente**, e suas regras de pacote portátil foram comparadas com as páginas oficiais OpenAI Plugins e Agent Skills em 2026-11-10. Isso valida a **escolha da metodologia**, não um pacote instalado/testado. **Skill Creator** está documentado como mecanismo oficial em ChatGPT/Codex, mas sua disponibilidade deve ser conferida em cada host. Superpowers/Context Engineering/Remotion serão aplicados seletivamente. Não presumir instalação de Iris/EarShot ou runtime de render.

### Critério de sucesso central

Quando o criador disser **“Chat, vamos criar um vídeo sobre [tema]”**, o plugin deverá: identificar o projeto e as autorizações, localizar/registrar produção, dar **uma próxima subtarefa clara**, executar quando houver ferramenta, atualizar estado e avançar somente após o gate correspondente — até o roteiro, thumbnail, vídeo renderizado/revisado e publicação assistida. **O plugin não pode fingir que realizou qualquer etapa não executada.**
