# Diazverso 1.0 — Passagem oficial para o Codex (11/11/2026)

> **DECISÃO MAIS RECENTE DO CRIADOR — PREVALECE SOBRE TODO TEXTO HISTÓRICO:** **NÃO instalar o plugin no ChatGPT nem no Codex durante o desenvolvimento.** Construir e testar tudo no GitHub/ambiente de desenvolvimento; finalizar a V1.0, migrar regras úteis e apagar documentação temporária, gerar e validar o ZIP final; **só então o criador instala manualmente**. **B06 [x]** cobre build e CI de ZIP, não instalação. **F06 [ ]** continua parcial. **Catálogo prioritário de especialistas:** [CATALOGO_SKILLS_PRIORITARIAS_E_IRIS.md](CATALOGO_SKILLS_PRIORITARIAS_E_IRIS.md); pesquisar Iris para visão/QA de vídeo e escolher melhores skills externas ou criar versões Diazverso originais se não houver autorização de redistribuição. GitHub público não é licença de cópia.

> **DOCUMENTO TEMPORÁRIO DE EXECUÇÃO.** Começar por aqui e por `AGENTS.md`. Não é uma skill distribuível nem um documento para manter após a versão 1.0. Não apagar antes da liberação final. **A versão 1.0 ainda NÃO está pronta.**

**ATUALIZAÇÃO DO CRIADOR EM 11/11/2026 (PREVALECE):** vídeos serão **postados manualmente pelo próprio criador**. O plugin termina no kit final revisado. **Não importar skill de postagem do plugin antigo e não criar upload/agendamento/publicação automática nem explicações de como postar.** Após postagem manual comprovada, apenas registrar URL/data/status reais na planilha, se apropriado. K04 removida do escopo.

## 1. Ordem de leitura e regra de continuidade

1. **Ler `AGENTS.md` e este arquivo**, depois `docs/ESPECIFICACAO_CANONICA_DIAZVERSO_V1.md` e o **item atual** de `docs/ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md`. Consultar `docs/CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md` se trabalhar com Drive/Sheets e `docs/TERCEIROS_E_LICENCAS.md` se trabalhar com skills de terceiros. Rascunhos, vídeo de referência, inventários e plugin antigo **somente sob demanda**.
2. Checar branch, último commit, estado do working tree e workflows antes de editar; não sobrescrever trabalhos mais novos.
3. Executar **uma microtarefa pequena** por vez. Criar/editar → testar → reler → revisar **independentemente** → corrigir falhas → **só marcar `[x]` no roadmap após critérios completos comprovados** → seguir à próxima elegível sem exigir que o criador diga “próximo”.
4. Uma tarefa bloqueada por ferramenta/licença/host fica `[ ]` com evidência em `docs/REGISTRO_EXECUCAO_E_PENDENCIAS.md`. Pode seguir outras independentes; **nunca simular instalação, escrita no Drive, render, publicação ou redução de tokens**.
5. Preservar as decisões de 10/11/2026: **plugin antigo e Content Lab antigo são obsoletos**. A refatoração do Content Lab será feita **depois** do plugin novo; usar TSX antigos apenas como referências individuais após análise.
6. **Não executar limpeza documental agora.** As regras temporárias serão removidas **após V1.0 implementada e validada pelos testes de desenvolvimento, antes de entregar o ZIP final para instalação manual pelo criador**, com decisões importantes migradas. Ver seção 8.

## 2. Visão do produto (a ideia central que não pode ser perdida)

O **Diazverso** é um canal brasileiro sobre super-heróis, quadrinhos, filmes, séries, animações e jogos (Marvel, DC, Ben 10 etc.). O plugin deve permitir ao criador pedir **“Chat, vamos criar um vídeo”** e receber **coordenação por pequenas etapas**, até ter material revisado para publicar:

`Ideia/pesquisa/tese → títulos A/B + promessa/thumbnail → roteiro Google Docs formatado → revisão humana/editorial/factual → assets e Nox → decupagem → TSX/Remotion + áudio/captions → render por trecho → revisão visual/sonora → correção e rerender → kit final entregue ao criador para postagem manual → registro posterior opcional de URL/data reais no Sheets (sem postar pelo plugin).`

- **Voz:** PT-BR natural, conversa e opinião com ironia contextual, sem formalismo robótico; referências de função: **FALL** (personalidade/humor), **Um Nerd** (tese/argumento), **RunnyIA** (fluidez e motion), sem copiar.
- **Visual:** HQ madura/moderna, profundidade, câmera/zoom/pan, parallax, tipografia de impacto **Anton** quando licenciada, CTA pertinente; não balões infantis nem montagens paradas.
- **Nox:** mascote canônico **fisicamente dentro do plugin** em `assets/brand/nox/Nox.png`; não redesenhar. Poses novas requerem comparação visual A05/G01.
- **Shorts:** 9:16, legendas sincronizadas por padrão, CTA contextual, preferência editorial por **pelo menos 60 segundos** (não apresentar como limite de plataforma).
- **Qualidade e segurança:** distinguir fato de interpretação; conferir fontes e direitos de trilhas/imagens/clipes; evitar prometer CTR ou desempenho; não publicar ou excluir sem autorização; **revisão ao fim de cada microtarefa**.

### Drive operacional aprovado

```text
Diazverso/
├── Canal do YT — V1.0 (Diazverso)  [Google Sheets]
├── Roteiros/{Longos,Shorts}/      [Google Docs nativos, diretos]
├── Thumbnails/{Longos,Shorts}/   [imagens diretas]
├── Assets/
├── Backgrounds/
├── Memes/
├── Músicas/
└── Sounds/
```

Abas: **Produções, Ideias, Afiliados, Config** (oculta). IDs **VD_####** (longo), **SH_####** (Short), **TF_####** (ideia). **Ideia aprovada deixa Ideias somente depois de criar/verificar a linha em Produções e preservar sua origem**; testar idempotência e falhas intermediárias antes de apagar a linha. As pastas já existem na instalação atual, mas **as skills para provisionar automaticamente novas contas ainda não estão implementadas**. Não hardcodar os IDs do Drive atual no plugin; a referência da instalação está no contrato de Drive.

## 3. Auditoria do que realmente estava concluído em 10/11/2026

**Roadmap total: 87 microtarefas. [x]: 25. [ ]: 62.** Checados os arquivos e histórico de revisão; os `[x]` representam **escopo próprio concluído**, frequentemente documentação/skill, **não um fluxo de ponta a ponta operacional**.

**IDs `[x]`:**
- **A:** A01, A02, A04, A06, A07
- **B:** B01, B02, B03, B04, B05, B06
- **C:** C01, C02, C03, C04, C05
- **D:** D01, D02, D06
- **E:** E01
- **F:** F01, F02, F03, F04, F05
- **G–L:** nenhuma concluída

**Principais evidências reais:**
- `plugin.json` na raiz; `skills/diazverso-setup`, `diazverso-core`, `diazverso-contexto-eficiente`, `diazverso-criacao-video`, `diazverso-drive-setup`, `diazverso-pesquisa`, `diazverso-titulos`, `diazverso-revisao-embalagem` existem. `schemas/estado-producao-v1.schema.json` existe.
- Quatro skills **externas realmente incorporadas com licença MIT preservada**: `context-optimization`, `video-editing`, `analyze-video-editing`, `find-broll`. A análise externa de áudio recebeu um bloqueio de upload até haver **consentimento específico** (`--allow-external-upload`); não supor que o uso de áudio externo foi autorizado genericamente.
- **Nox real** em `assets/brand/nox/Nox.png`: blob Git `776d1b26983e6f9095178881c83b44f114a40336`, PNG RGBA 1408×768, 415.179 bytes; `assets/manifest.json` o descreve. O GitHub Actions validou bytes, hash e CRC no ZIP. Ferramenta textual pode falhar ao tentar decodificar PNG como UTF-8; isso **não significa arquivo ausente**.
- **Templates LONGO e SHORT:** Google Docs nativos já criados/relidos no Drive real; blueprints independentes em `templates/roteiro-longo-v1.json` e `templates/roteiro-short-v1.json`. Docs de referência na conta existente:
  - [Modelo de longo](https://docs.google.com/document/d/1yiakQ9VXci6yODX_xqXIqUJxiYpruU8AqZrQZpMsdlw/edit)
  - [Modelo de Short](https://docs.google.com/document/d/1FvJsjq-IyX4Q_JPlxAoBkPLA7oRp11sFTsx9IBCKo4Y/edit)
  Esses links são **evidência da instalação atual**, não configuração universal a embutir em plugin.
- **CI de ZIP mínimo:** [run 42898444365](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42898444365) verde. **CI ZIP completo:** [run 42898444272](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42898444272) verde, `PACKAGE_VALIDATED`, **71 arquivos**, ZIP **592.367 bytes**, SHA-256 `7c8af2fd919f2dd67902b6c215165b8c7bdd7dd265b67c66948071036fdd08fb`, `host_installation=NOT_TESTED`. Futuras alterações exigem novo CI.
- **Testes do gerador de requests Docs:** [run 42898526361](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42898526361), **7/7 testes unitários**, mais amostras LONGO e SHORT `REQUESTS_VALIDATED 21 21`. Não foi testada sincronização com Sheets.

**Escopo parcial importantíssimo — `[ ] F06`:** a skill `skills/diazverso-roteiro/SKILL.md`, o gerador `skills/diazverso-roteiro/scripts/build_requests.py` e testes **já existem e passaram no CI**, mas **NÃO foi verificado** o ciclo: localizar um vídeo de teste → criar/mover Doc nativo na pasta correta → aplicar/reler estilos → atualizar somente a célula `ROTEIRO` da produção exata na planilha → reler → repetir sem duplicar. **Não marcar F06 `[x]` antes disso.**

**B06 concluída — `[x] B06`:** o escopo correto é **construir e validar ZIP no GitHub Actions sem instalar**. O ZIP passou no CI; **a instalação manual será feita pelo criador somente depois da V1.0 pronta**. Não criar tarefa bloqueante de instalação nesta fase.

## 4. Como o Codex deve continuar, em ordem prática

**Não repetir as 24 tarefas marcadas `[x]`; checar somente se mudanças novas quebraram algo.** Sugerimos esta sequência, respeitando pré-requisitos reais:

1. **Checagem inicial:** executar `git status`, conferir `main`, rodar os três workflows/testes ou seus equivalentes. Ler últimas falhas em `docs/REGISTRO_EXECUCAO_E_PENDENCIAS.md`. Se os testes falharem, corrigir primeiro. O pacote de 71 arquivos é uma **referência histórica**, não a contagem final após novas skills.
2. **B06 já concluída:** verificar se os testes de ZIP/CI continuam verdes após alterações; **NÃO instalar o plugin em nenhum host**. Codex constrói e testa offline; o criador instalará manualmente após a V1 entregue.
3. **F06:** completar integração real com Drive/Sheets usando uma **produção de teste isolada**, com permissões e proteção contra duplicidade. Não alterar vídeos publicados como cobaias.
4. **E02–E08:** provisionamento idempotente, validação de planilha, criação de ideia, promoção segura TF→VD/SH e upserts. **E06 precisa de teste de falha/repetição E07**; não excluir ideias antes de confirmar o novo vídeo.
5. **F07–F10:** revisores de fatos, estrutura/ritmo, humanização e gate de aprovação antes da edição.
6. **A03/A05 e D03–D05/D07:** catálogo seletivo de TSX antigos, **revisão visual do Nox** e importação de backgrounds/SFX somente com direitos comprovados; teste de acesso sem Drive.
7. **G01–G08, H01–H09, I01–I05:** skills de Nox, thumbnail, biblioteca TSX/Remotion independente, composições reais, Shorts 9:16 e revisão de render. Testes de TSX/FFmpeg devem rodar em executor real; **Content Lab não é dependência**.
8. **C06/C07, J01–J08, K01–K05, L01–L07:** testes de roteamento e economia medidos; QA de código, imagem/áudio/licenças; kit/publicação quando autorizada; ensaios integrados e liberação final. Nenhum campo `PUBLICADO` sem URL realmente confirmada.

Se uma tarefa de integração ficar bloqueada por conexão/permissão, deixar `[ ]` e avançar a outra independente sem alegar sucesso.

## 5. O que existe dentro do pacote e licenças

```text
plugin.json
skills/                              # skills autorais e externas vendorizadas
assets/brand/nox/Nox.png             # mascote canônico
assets/manifest.json
templates/                           # blueprints de Doc longo/Short
schemas/                             # contrato de estado
docs/                                # TEMPORARIAMENTE embutidos por builder atual
```

- `scripts/build_diazverso_plugin.py` monta o ZIP completo e verifica hash/CRC/skills/licenças/templates; atualmente inclui vários `docs/*.md` de trabalho porque ainda existem referências neles.
- As skills externas **não são apenas links**: arquivos e licenças fazem parte da árvore `skills/`; consultar `docs/TERCEIROS_E_LICENCAS.md`. **Não copiar** as skills oficiais Remotion sem licença de redistribuição inequívoca; é possível criar integração autoral a partir de documentação oficial.
- Nenhuma música/meme/clipe de terceiros é liberado para distribuição apenas por constar no Google Drive; conferir origem/uso.
- O plugin ainda está na versão de manifesto **0.1.0**, em desenvolvimento. Não anunciar release 1.0 antes dos gates L.

## 6. Problemas e riscos que não podem ser esquecidos

| Referência | Problema real | Estado |
| --- | --- | --- |
| B06 | ZIP mínimo/completo validado no CI; instalação reservada ao criador pós-V1 | **CONCLUÍDO NO ESCOPO DE BUILD [x]** |
| F06 | Escrita idempotente no Docs e sincronização de link na linha Sheets | **PARCIAL** |
| E02–E08 | Conectores/permissões, duplicação, promoção de ideias e rollback | **NÃO IMPLEMENTADO/TESTADO** |
| A05/G01 | Poses Nox ainda sem revisão visual comparada | **PENDENTE** |
| H/G/I/J | Remotion/TSX, render, movimento, SFX, captions e QA reais | **PENDENTE** |
| Externas/Remotion | Licenças/redistribuição e envio opcional de áudio a serviços externos | **RESTRIÇÕES ATIVAS** |
| Histórico | Bug `.gitkeep` no build completo foi **corrigido** e CI verde | **RESOLVIDO** |
| Limpeza | Arquivos temporários necessários durante o desenvolvimento; limpar **antes de entregar o ZIP final**, depois dos testes de desenvolvimento | **ADIADA PARA O FECHAMENTO DA V1** |

Relatório operacional contínuo em `docs/REGISTRO_EXECUCAO_E_PENDENCIAS.md`. Diferenciar **falha**, **falta de ferramenta** e **não testado**.

## 7. Critério real de conclusão da V1.0

Não basta `SKILL.md` existir ou CI estar verde. Precisamos de:

- [ ] Manifesto, skills e assets validados no pacote e **testados em ambiente de desenvolvimento com casos reproduzíveis**, sem instalar no ChatGPT/Codex.
- [ ] Drive provisionado/reparado idempotentemente; Google Docs nativos e Sheets integrados, sem duplicatas/perdas.
- [ ] Fontes, revisão de roteiro, thumbnails e Nox testados; mídia só com direitos verificados.
- [ ] Remotion independente com render **longo e Short**, voz/áudio/legendas e QA de quadros/áudio reais.
- [ ] Kit de publicação pronto para postagem **manual pelo criador**; atualização factual de status/link apenas depois que o criador confirmar sua publicação, sem envio pelo plugin.
- [ ] Testes de falha/repetição, retomada de sessão, segurança, licenças e degradação sem conectores.
- [ ] ZIP de release e CI validados, documentação curta de **instalação manual futura pelo criador** e limitações reais, versão/tag no GitHub.
- [ ] **Somente depois:** limpeza da documentação temporária sem quebrar o pacote.

## 8. LIMPEZA OBRIGATÓRIA APÓS V1.0 VALIDADA — não executar antes

**Decisão explícita do criador:** “rascunho, roadmap, todos eles vão ser apagados” e ficarão apenas os materiais úteis ao plugin. Esta limpeza faz parte do **último gate de release**, após todo conhecimento funcional e direitos serem migrados para skills, `references/`, assets, schemas, templates e README mínimo.

### Candidatos temporários a REMOVER do repositório ao finalizar

- `AGENTS.md` — instrução do Codex durante construção; **migrar regras operacionais úteis para skills/references antes**.
- Este `docs/HANDOFF_CODEX_2026-11-11.md`.
- `docs/ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md`.
- `docs/RASCUNHO_IDENTIDADE_DIAZVERSO_1.0.md`.
- `docs/PROPOSTA_ORGANIZACAO_DRIVE_PLANILHA_V1.0.md`.
- `docs/DECISOES_E_CONTEXTO.md`.
- `docs/REGISTRO_EXECUCAO_E_PENDENCIAS.md`.
- `docs/TESTE_A07_PROGRESSIVO.md` e `docs/TESTE_B06_PLUGIN.md`.
- `docs/EMPACOTAMENTO_PORTATIL_DIAZVERSO_V1.md`.
- `docs/MATRIZ_CAPACIDADES_E_PERMISSOES_V1.md`.
- `docs/ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md`.
- `docs/CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md`.
- `docs/ESPECIFICACAO_CANONICA_DIAZVERSO_V1.md`.
- `docs/CATALOGO_SKILLS_PRIORITARIAS_E_IRIS.md` — migrar seleção final, integração Iris e alternativas autorais para skills/references.
- `docs/TERCEIROS_E_LICENCAS.md` **só quando** os avisos de copyright/licença e vínculos necessários estiverem preservados no pacote final, p.ex. um `THIRD_PARTY_NOTICES.md` pequeno, além dos `LICENSE` em cada skill.

**Também fazer triagem da infraestrutura de desenvolvimento**: `scripts/b06_package_smoke.py`, `scripts/build_diazverso_plugin.py`, `.github/workflows/`, testes de unidade dos scripts, exemplos de teste, códigos e documentos não consumidos pelo plugin. Só manter o que é necessário à **operação, instalação, manutenção autorizada ou obrigação de licença**; evitar deixar dentro do ZIP artefatos de QA/development sem necessidade. O script funcional `skills/diazverso-roteiro/scripts/build_requests.py` é parte potencial do plugin e **não deve ser apagado por estar em pasta `scripts`**.

### Sequência de limpeza — executar quando TODAS as condições acima estiverem satisfeitas

1. Auditar **todas as referências** `docs/` em `skills/`, `plugin.json`, `templates/`, `schemas/`, `README.md` e scripts. **Migrar conteúdo essencial** para `skills/<nome>/references/` e documentação curta mantida. Não deixar referências quebradas.
2. Ajustar `scripts/build_diazverso_plugin.py` para **não embutir rascunhos/roadmap/docs de projeto** em `DOCS`; validar distribuição mínima e licenças. Reavaliar se manter build/CI no repositório é útil ao plugin (no ZIP final, normalmente não).
3. Garantir que **qualquer documentação temporária no Google Drive** não pertença à pasta de produção; tratar exclusão de Docs do Drive somente com autorização específica. **Não excluir roteiros, thumbnails, planilha operacional, Nox ou bibliotecas do canal.**
4. Tirar snapshot/tag do release, registrar resultados e SHA do ZIP, então **excluir do branch de produção** os arquivos transitórios listados, preservando o histórico Git. Remover somente após confirmar que o plugin final já consegue operar **sem depender desses arquivos**.
5. Rodar testes e CI **depois da limpeza**, verificar que o ZIP é autossuficiente **sem instalar em ChatGPT/Codex**. Revisar `README.md`, `plugin.json`, licenças e atribuições. O criador instalará depois que receber o pacote validado.
6. Se qualquer referência/teste falhar, **não apagar a origem pendente** até migrar/corrigir e rever. Não remover histórico do Git.

**Não executar nenhum dos passos destrutivos desta seção agora.** A limpeza será feita **antes** de o criador instalar o plugin: após finalizar os recursos/testes, migrar as regras úteis e garantir que o ZIP final não contém rascunhos.

## 9. Registro final da passagem

- Auditoria: 10/11/2026, antes de a implementação ser retomada no Codex.
- **25 concluídas e 62 pendentes**; **F06 continua parcial** e **B06 está concluída como validação de ZIP (não instalação)**.
- Código de geração de requests validado com 7 testes; **integração Google Docs/Sheets ainda não comprovada; instalação não é tarefa de desenvolvimento**.
- Ao continuar, **não pedir ao criador para dizer “próximo” entre tarefas; revisar cada uma e registrar resultados no roadmap**.
