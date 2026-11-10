# Diazverso Plugin 1.0 — Roadmap de implementação em microtarefas

**Data:** 2026-11-10  
**Estado:** ROADMAP PARA EXECUÇÃO. Nenhum item deste roadmap equivale, sozinho, à funcionalidade implementada.  
**Destino:** [repositório novo](https://github.com/DanielHABDias/DiazVerso-Plugin).  
**Objetivo:** um plugin instalável para ChatGPT e Codex que coordene, em etapas pequenas, conteúdo de vídeo longo/Short: pesquisa → tese/packaging → roteiro formatado → thumbnails → narração/assets → Remotion/Content Lab → revisão audiovisual → kit de publicação. O fluxo completo depende das ferramentas e autorizações reais do host.

## 0. Regras de execução (obrigatórias)

1. **Uma microtarefa por vez:** selecionar o primeiro checkbox pendente cujos pré-requisitos estejam concluídos. Executar, conferir e registrar resultado **antes** de iniciar outra. Não combinar “implementar toda a fase” em uma única solicitação/commit.
2. Cada tarefa deve ter: **entrada, entrega concreta, validação/teste, arquivo(s) impactado(s), estado e próxima tarefa**. Uma tarefa que requer muitas alterações deve ser fracionada antes de começar.
3. **Trabalhar no repositório novo**; o plugin antigo no Drive é referência histórica, **não fonte que sobrescreve decisões 1.0**. Usar o código atual do Content Lab como contrato técnico quando acessível.
4. Tratar cada decisão com origem: **aprovada no novo contexto**, **referência do plugin antigo**, **hipótese a verificar**. Não transferir regras velhas de pastas por vídeo, planilha em duas abas, balões HQ ou espiral obrigatória.
5. **Contexto enxuto:** ler `AGENTS.md`, resumo de decisões e **somente a skill/referência da tarefa atual**; retornar link/resumo do resultado, não despejar árvores/código enormes na conversa. Salvar estado no GitHub.
6. Subagentes são **opcionais** e somente quando runtime suportar, para trabalho independente com escopo estreito (inventário, pesquisa, testes). O agente principal decide, integra e valida sequencialmente; não delegar edições concorrentes no mesmo arquivo.
7. **Não presumir acesso ao Drive, render, GitHub ou YouTube:** verificar conexões/permissões e relatar bloqueios. Plugin de skills ≠ motor de render; render real exige Remotion/Content Lab em ambiente capaz.
8. **Não copiar automaticamente mídia de terceiros** do Drive para repositório distribuível. Nox canônico e materiais próprios/aprovados primeiro; verificar direitos de backgrounds, SFX, memes, músicas, fontes e distribuição.
9. **Não criar arquivos .old/.bak, versões paralelas de regras, campos `schemaVersion` sem necessidade aprovada, nem funcionalidades de composição musical** removidas do Content Lab anterior.
10. Por tarefa concluída: alteração pequena + teste/evidência quando aplicável + atualização desta checklist (e de `docs/DECISOES_E_CONTEXTO.md` quando houver decisão) + próximo ID.

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
| Código atual de edição | [DanielHABDias/ContentLab](https://github.com/DanielHABDias/ContentLab), `main`; [layout do projeto](https://github.com/DanielHABDias/ContentLab/blob/main/docs/PROJECT_LAYOUT.md) | Contrato técnico vigente de TSX, edição, saída e render — auditar antes de integração |
| Organização do Drive | [Contrato operacional](CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md) e [Bibliotecas](ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md) | Estrutura aprovada, IDs apenas desta instalação |
| Identidade editorial | [Rascunho em evolução](RASCUNHO_IDENTIDADE_DIAZVERSO_1.0.md) | Briefing a consolidar, **não inteiro em prompt global** |

**TSX confirmados por listagem/leitura inicial:** `TextoHQ.tsx` (Anton/Bangers, texto cinético), `PersonagemEspiralLegenda.tsx` (personagem/legendas), `QuadroHQSobreCena.tsx` (quadro sobre imagem/vídeo), `BackgroundHQ.tsx` (halftone/papel/estrelas/grade), `GaleriaCartasHQ.tsx`, `ComicPageCTA.tsx` e `HQMotion.tsx`, com `HQComicPage.tsx` como dependência compartilhada. Parte dos módulos tem prévias, JSON e variantes 16:9/9:16. **Arquivos da antiga biblioteca não foram importados para o novo GitHub nem compilados nesta fase.** O `HQComicPage.tsx` está repetido nas pastas e exige deduplicação e comparação com o Content Lab atual.

### Skills externas selecionadas para investigar e aplicar seletivamente

- **Eficiência de tokens:** [context-optimization](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering), `context-compression`, `filesystem-context`, `memory-systems`, `multi-agent-patterns`. Aplicar **progressive disclosure** (metadata → SKILL.md → references/assets/scripts) e medir custo em testes comparáveis. Não prometer percentuais sem medição.
- **Execução em tarefas pequenas e qualidade de software:** [obra/superpowers](https://github.com/obra/superpowers) — `writing-plans`, `executing-plans`, testes/revisão; adaptar ao ChatGPT/Codex, sem assumir subagentes disponíveis.
- **Remotion (oficial):** [remotion-dev/skills](https://github.com/remotion-dev/skills) — `remotion-best-practices`, `remotion-markup`, `remotion-create`, `remotion-render`, `remotion-studio`, `remotion-captions`, `remotion-multimedia`, `remotion-docs`. Versões e API verificadas contra o Content Lab atual; não instalar o conjunto todo sem necessidade.
- **Formato de skills/plugins:** [Agent Skills](https://agentskills.io), [OpenAI Plugin Docs](https://developers.openai.com/plugins/build/plugins). `plugin.json` raiz + `skills/<nome>/SKILL.md`; `assets/` opcional; `mcp.json` **apenas quando necessário**. Validar com Plugin Creator e host.
- **Outros candidatos não homologados:** HyperFrames, GSAP, Humanizer, Baoyu Cover Image, Last30Days, WATCH, EarShot, Iris, Browser Use, Openverse/Real SFX. Investigar licença, compatibilidade e valor real individualmente; não pré-instalar ou assumir equivalência.
- **Pesquisa de YouTube:** vidIQ quando conectado, fontes oficiais e pesquisa complementar; resultados podem ser usados para perguntas/hipóteses, não promessas do algoritmo.

## 2. Roadmap detalhado — executar na ordem de dependência

### Fase A — Auditoria e fronteiras

- [ ] **A01** — Listar as 44 skills do plugin antigo em uma tabela de nome/função/arquivos, sem copiar nenhum arquivo.
- [ ] **A02** — Classificar cada skill antiga: `REUTILIZAR CONCEITO`, `REESCREVER`, `NÃO HERDAR`; justificar conflitos com a V1.
- [ ] **A03** — Inventariar as pastas de TSX antigos, os arquivos TSX, JSON de exemplo, previews e dependências. Um registro por componente; apontar redundâncias.
- [ ] **A04** — Comparar contratos de TSX antigos com o código atual de `ContentLab/main` (manifests, versões, props, hooks, local de cenas e formato de projeto).
- [ ] **A05** — Verificar visualmente `Nox.png` e confrontar com o Character Lock histórico; definir **uma** referência canônica do Nox para V1.
- [ ] **A06** — Definir o mínimo viável do plugin em ChatGPT normal versus recursos que exigem Work/Codex/Content Lab, identificando conectores e limites.
- [ ] **A07** — Consolidar **somente as decisões editoriais já aprovadas** do rascunho em um resumo curto, mantendo dúvidas fora do núcleo.

**Gate A:** inventários verificáveis, decisões antigas conflitantes identificadas, sem importação indiscriminada.

### Fase B — Plugin instalável mínimo

- [ ] **B01** — Criar e validar `plugin.json` raiz com identidade `diazverso`, descrição, versão e schema portátil correto.
- [ ] **B02** — Criar skill mínima `skills/diazverso-setup/SKILL.md` de onboarding (descobrir permissões, dependências e pastas, sem prometer render).
- [ ] **B03** — Criar `skills/diazverso-core/SKILL.md` com posicionamento, vocabulário, Nox e links para referências — sem duplicar briefing.
- [ ] **B04** — Validar `SKILL.md`/frontmatter/path de todas as skills criadas até aqui com spec Agent Skills.
- [ ] **B05** — Criar compatibilidade Codex/Plugin Creator **apenas no formato exigido pelo host verificado**; evitar manifests divergentes.
- [ ] **B06** — Instalar localmente o plugin mínimo e confirmar que ChatGPT/Codex conseguem invocar a skill de setup (testes separados por host).

**Gate B:** plugin mínimo instalado **e testado**, ainda sem afirmar que edita vídeos.

### Fase C — Economia de tokens e orquestração

- [ ] **C01** — Criar `skills/diazverso-contexto-eficiente/SKILL.md` com roteamento e disclosure progressivo inspirados em `context-optimization`.
- [ ] **C02** — Implementar a regra **uma skill principal por microtarefa**, carregando referências somente quando indispensáveis.
- [ ] **C03** — Criar skill orquestradora `diazverso-criacao-video`: entrada `vamos criar um vídeo`, status e próximo passo, sem colar conteúdo das demais skills.
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
- [ ] **G05** — Compilar e renderizar uma cena baseada no exemplo escolhido no Content Lab/Remotion atual; revisar quadros 16:9 e 9:16.
- [ ] **G06** — Migrar seletivamente `BackgroundHQ.tsx` e `QuadroHQSobreCena.tsx`, cada um em tarefa/PR separado, após validação.
- [ ] **G07** — Auditar `PersonagemEspiralLegenda.tsx` e `ComicPageCTA.tsx` (legendas/CTA) **sem tornar espiral e balões padrão obrigatório**.
- [ ] **G08** — Consolidar `HQMotion.tsx`/`HQComicPage.tsx` e dependências em biblioteca única quando necessário; **não copiar as inúmeras cópias de 885 KB** indiscriminadamente.

**Gate G:** Nox e components de edição disponíveis/compiláveis; exemplos antigos não substituem critérios editoriais novos.

### Fase H — Produção audiovisual por microcena

- [ ] **H01** — Auditar `ContentLab/main`, suas dependências e formatos reais `edit_plan.json`/`scene-library`/`custom-scenes`.
- [ ] **H02** — Criar skill de decupagem audiovisual: blocos curtos, quadro-alvo, narração, mídia, SFX, música e objetivo de cada cena.
- [ ] **H03** — Criar componentes/testes de câmera em imagens estáticas: zoom/pan/reframe/blur, evitando imagem parada e vazios involuntários.
- [ ] **H04** — Criar componente/teste de parallax em camadas, com fundo e PNG recortado; verificar escala/safe area.
- [ ] **H05** — Criar componente/teste de texto cinético Anton, com contraste real e timing de palavras.
- [ ] **H06** — Criar tratamento de painéis de filme/TV com CRT perceptível, áudio de trecho quando autorizado e moldura contextual; respeitar uso de conteúdo de terceiros.
- [ ] **H07** — Criar seleção contextual de música/SFX a partir da biblioteca aprovada; volume/ducking/sincronização verificados.
- [ ] **H08** — Implementar render **por trecho** e preview automatizado antes do render final.
- [ ] **H09** — Integrar geração/edição técnica ao Content Lab local/Work/Codex; avaliar MCP **se for necessário**, com autenticação, escopo e teste de ponta a ponta.

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
- [ ] **L02** — Teste completo **Work/Codex + Content Lab**: roteiro → decupagem → TSX → render 16:9 → QA.
- [ ] **L03** — Teste completo **Short** 9:16 com legendas/CTA e QA independente.
- [ ] **L04** — Teste de retomada: interromper e reabrir em nova sessão; recuperar a próxima microtarefa sem recomeçar nem duplicar.
- [ ] **L05** — Teste de host sem Drive / sem Content Lab / sem EarShot: degradação transparente e somente funcionalidades possíveis.
- [ ] **L06** — Testar versão final do pacote com Plugin Creator/Codex, incluindo manifesto, skills e Nox; verificar que assets não faltam.
- [ ] **L07** — Consolidar README de instalação, recursos, limites e requisitos/autorizações; só então marcar V1.0 apta a uso.

**Gate L:** fluxo testado por host, pacote instalável, exemplos reproduzíveis e limites documentados.

## 3. Ordem recomendada de entregas demonstráveis

**Marco 1 — Plugin mínimo:** A → B → C. Resultado: instalável, roteador, contexto eficiente e uma tarefa por vez.

**Marco 2 — Produto editorial:** D → E → F → G01–G03. Resultado: Nox embutido, Google Drive/Sheets e roteiro/thumb com revisores, mesmo sem render autônomo.

**Marco 3 — Motion:** G04–G08 → H → J (QA parcial). Resultado: TSX selecionado e testado contra Remotion/Content Lab.

**Marco 4 — Shorts e finalização:** I → J completo → K → L. Resultado: edição vertical/horizontal, legenda, áudio, QA e publicação assistida quando possível.

**Primeira microtarefa a executar depois de aprovar este plano:** **A01 — catalogar as 44 skills do plugin antigo**; saída em tabela de inventário, sem importar código. **Segunda:** A02 (triagem). **Importação real de Nox.png:** D01, logo após ter o esqueleto validado, sem esperar pela implementação do editor.

## 4. Fontes externas — status de uso

As fontes técnicas de Remotion, Agent Skills, Context Engineering, Superpowers e OpenAI Plugins foram verificadas publicamente em 2026-11-10, mas **suas skills não foram instaladas ou testadas no novo plugin nesta etapa**. Verificação de compatibilidade e licença acontece por tarefa. Não presumir que dependências de modelos/Work/Codex/Plugin Creator/Iris/EarShot estejam presentes.

### Critério de sucesso central

Quando o criador disser **“Chat, vamos criar um vídeo sobre [tema]”**, o plugin deverá: identificar o projeto e as autorizações, localizar/registrar produção, dar **uma próxima subtarefa clara**, executar quando houver ferramenta, atualizar estado e avançar somente após o gate correspondente — até o roteiro, thumbnail, vídeo renderizado/revisado e publicação assistida. **O plugin não pode fingir que realizou qualquer etapa não executada.**
