# Diazverso — Contrato operacional de Drive, planilha e produção V1.0

> **APROVADO PELO CRIADOR COMO BASE DE ORGANIZAÇÃO, em 10/11/2026.**
> **Implementação real parcialmente concluída no Google Drive; AUTOMAÇÃO DO PLUGIN AINDA NÃO IMPLEMENTADA.**
> Este contrato registra a estrutura a ser implementada em uma futura versão instalável do plugin. Ele **não autoriza inferir que ChatGPT padrão, Work ou Codex já executam todo o pipeline sem ferramentas ou permissões**. O criador poderá refinar roteiro, organização e fluxo antes de consolidar a V1.0.

## 1. Princípios de operação

- Nome canônico da marca e pasta: **Diazverso** (não "Diasverso" transcrito por voz). Display opcional: **Diazverso**.
- O usuário deve poder solicitar apenas **"Chat, vamos criar um vídeo"** e ser conduzido de **tema, pesquisa e argumento** até **roteiro, thumbnails, edição e pacote de publicação**, sem reexplicar nomes, pastas, formato dos Docs ou colunas da planilha.
- Uma tarefa pequena por vez, com entrada, saída, revisão, evidência e atualização de status. Subagentes paralelos são opcionais **somente se suportados e úteis**; coordenação central e integração sequencial.
- **Google Drive:** armazenar **roteiros, thumbnails, planilha mestre** e, conforme solicitação posterior do criador, **bibliotecas auxiliares Backgrounds, Assets, Memes, Músicas e Sounds** na raiz Diazverso. Não acumular guia de edição, prompts e TSX duplicados por vídeo. O inventário e a reorganização efetiva das bibliotecas estão em [ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md](ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md).
- **GitHub/plugin:** futura fonte versionada de conhecimentos e componentes reutilizáveis — Nox canônico, backgrounds aprovados, recursos TSX Remotion, regras de edição, templates e SFX licenciados.
- **Dados pessoais e permissões:** nunca colocar IDs da conta real, tokens ou emails pessoais como valores universais. Cada instalação deve descobrir e vincular seus próprios Drive IDs.
- **Preservação:** edição deve ser idempotente; pesquisar antes de criar; conservar ID/link de arquivos movidos; não excluir dados ou vídeos de terceiros sem autorização e permissão. **Uma limpeza autorizada dos arquivos antigos foi realizada na instalação atual; ver status no final.**

## 2. Estrutura de pastas CANÔNICA

```text
Diazverso/
├── Canal do YT — V1.0 (Diazverso)           [Google Sheets]
├── Roteiros/
│   ├── Longos/
│   │   ├── VD_0008 — Roteiro aprovado      [Google Doc]
│   │   └── VD_XXXX — ...                   [Google Doc]
│   └── Shorts/
│       ├── SH_0025 — RT_0025 — Roteiro     [Google Doc]
│       └── SH_XXXX — ...                   [Google Doc]
├── Thumbnails/
│   ├── Longos/
│   │   ├── VD_0008_A.png
│   │   └── VD_0008_B.png
│   └── Shorts/
│       └── SH_0025.png
├── Backgrounds/                   [imagens HQ/cores + vídeos animados]
├── Assets/                        [identidade Nox/HQ, motion, apoio, triagem]
├── Memes/                         [imagens e vídeos]
├── Músicas/                       [favoritas, clima, obras, bibliotecas, triagem]
└── Sounds/                        [whoosh, impactos, interface, memes, foley...]
```

**Nota:** o desenho acima ilustra a organização lógica; alguns arquivos históricos têm nomes e extensões legadas (.md, .txt, .docx, .jpg). Não renomear/reescrever automaticamente o conteúdo antigo. Para arquivos **novos**, padronizar nome e tipo.

**Não criar subpasta por vídeo** sob Longos/Shorts. O ID único no nome e os links na planilha bastam. Se surgir uma razão real para guardar dezenas de variantes em um vídeo, reavaliar conscientemente, em vez de recriar a árvore anterior por padrão.

**Instância real de 10/11/2026** (URLs ilustram a conta existente; NÃO hardcodar no plugin distribuído):
- [Raiz Diazverso](https://drive.google.com/drive/folders/1SbOI-GtWAaWzxFh1ysG5DOjf0DZ8XSYh)
- [Planilha V1.0](https://docs.google.com/spreadsheets/d/12_bYL2N9mwRj4lel_fNVOOPBruth-Ca2FsAjrgU1VQk/edit)
- [Roteiros/Longos](https://drive.google.com/drive/folders/1Q0C9buTyO7QLS1P7L3ZwAApLj8Iz0HDs)
- [Roteiros/Shorts](https://drive.google.com/drive/folders/1s1MHzcO32rC3G577-QmiI08PLAg-at5C)
- [Thumbnails/Longos](https://drive.google.com/drive/folders/1sRrsRT_qERy92p1VkTtCh1DwQ9ZLZBZi)
- [Thumbnails/Shorts](https://drive.google.com/drive/folders/10ur3-daj2mWqUsgWTpblmb_XnYOFKOco)

## 3. Planilha mestre — abas oficiais

**Google Sheets** `Canal do YT — V1.0 (Diazverso)`:

### 3.1 `Produções` — única tabela de vídeos LONGO e SHORT

Uma linha para cada vídeo real (sem IDs pré-criados vazios). Os campos **reais** da planilha criada são:

| Coluna | Nome | Finalidade |
| --- | --- | --- |
| A | ID | `VD_0001` ou `SH_0001`; permanente |
| B | TIPO | `LONGO` ou `SHORT` — dropdown |
| C | TEMA / CONTEXTO | Tese e contexto resumidos; evitar dados sem validação |
| D | STATUS | Fase do pipeline, inclusive `PUBLICADO` |
| E | PRIORIDADE | `ALTA`, `MÉDIA`, `BAIXA` |
| F | TÍTULO A | Primeira proposta de título |
| G | TÍTULO B | Alternativa para comparação/teste |
| H | THUMBNAIL A | Link do **arquivo de imagem**, nunca de pasta temporária |
| I | THUMBNAIL B | Link de alternativa, se houver |
| J | ROTEIRO | Link do documento real na pasta correspondente |
| K | VÍDEO RELACIONADO | ID do vídeo longo para Short derivado, se aplicável |
| L | PLANEJADO PARA | Data prevista, opcional |
| M | PUBLICADO EM | Data real, não inferir |
| N | LINK YOUTUBE | URL real após publicação |
| O | REVISÃO | Estado do gate de qualidade quando realmente verificado |
| P | OBSERVAÇÕES | Anotações úteis e excepcionais; **não inserir recados artificiais sobre "textos preservados no LEGADO"** |
| Q | KIT PUBLICAÇÃO | Link opcional para texto/artefato do kit de postagem (pode ficar no roteiro) |

Status permitidos no modelo: `PLANEJADO`, `PESQUISA`, `ROTEIRO`, `REVISÃO DE ROTEIRO`, `ASSETS`, `EDIÇÃO`, `REVISÃO FINAL`, `PRONTO`, `AGENDADO`, `PUBLICADO`, `PAUSADO`, `CANCELADO`.

**Situação real migrada:** 8 longos e 25 Shorts existentes, todos em `PUBLICADO` conforme `FINALIZADO=true` e link YouTube real na planilha de origem; **não afirmar que passaram por revisão V1.0**, pois o campo REVISÃO foi deixado em branco. A antiga mensagem de observação foi apagada das 33 linhas. Todos os 33 links de roteiro foram validados após movimentação de arquivos. Quatro Shorts `SH_0001`–`SH_0004` tiveram links corrigidos para **imagens reais** em vez de pastas posteriormente excluídas.

### 3.2 `Ideias` — apenas pauta **ainda não promovida**

Campos reais: `ID` (TF_####), `TEMA`, `TESE / CONTEXTO`, `TÍTULO PROVISÓRIO`, `IDEIA DE THUMB`, `POR QUE VALE`, `PRIORIDADE`, `TIMING / CONTEXTO`, `ORIGEM`, `STATUS`, `PRODUÇÃO VINCULADA`, `OBSERVAÇÕES`.

**Decisão explícita do criador — MOVER, NÃO DUPLICAR:**
1. Pesquisar e amadurecer uma pauta na aba **Ideias** até aprovação.
2. Ao começar a produção concreta, alocar um **novo ID de vídeo** `VD_####` ou `SH_####` (não reutilizar `TF_####` como ID de produção).
3. Copiar para **Produções** os dados relevantes da ideia: tese, contexto, títulos provisórios e prioridade; gravar `IDEIA_ORIGEM_ID` no contexto/metadados do roteiro ou em um campo adequado da produção, para rastrear a origem.
4. **Verificar** que a linha nova está registrada, completa e que o roteiro foi criado/associado conforme estágio.
5. **Só após sucesso, REMOVER a linha original da aba Ideias**, usando o ID `TF_####` exato e não o número de linha em cache. Reconsultar as linhas imediatamente antes da exclusão, pois índices mudam quando usuários editam a planilha.
6. Se alguma ação falhar, **não apagar a ideia**. Em caso de execução repetida, localizar o ID de produção já gerado e retomar sem criar duplicata. Se necessário, informar qual etapa ficou incompleta.
7. É aceitável manter `PRODUÇÃO VINCULADA` na aba durante testes/migração; após eliminação consistente da linha, a coluna se torna dispensável e poderá ser removida em revisão posterior. **A aba Ideias deve conter só ideias em aberto.**

**Importante:** essa é uma regra operacional futura, **não executada retroativamente sobre as 15 ideias** em 10/11. A análise prévia mostrou textos em ideias que já mencionam vídeos reais; conferir duplicidade ao selecionar uma delas, não excluí-las em massa.

### 3.3 `Afiliados`

Campos reais: `ID`, `PRODUTO / SERVIÇO`, `CATEGORIA`, `PLATAFORMA`, `LINK AFILIADO`, `APLICÁVEL A`, `STATUS`, `ÚLTIMA VERIFICAÇÃO`, `FONTE`, `OBSERVAÇÕES`.

- Foram recuperados **8 links** de descrições antigas, com nomes normalizados. Todos estão marcados `A CONFERIR` porque **não houve validação dos destinos/preços/validade**.
- O agente deve selecionar links **pertinentes à pauta** e com status `ATIVO`, verificando necessidade de aviso de afiliação nas descrições. Nunca inserir todos os links automaticamente por obrigação, nem presumir que links aumentam RPM/distribuição.
- Separar `ATIVO`, `A CONFERIR`, `PAUSADO`, `EXPIRADO`. Não guardar credenciais ou IDs privados de programa de afiliados desnecessários.

### 3.4 `Config` — aba técnica oculta

- Esquema/schema versionado, IDs **da instalação** (raiz, pastas, planilha), versão de migração e parâmetros necessários; sem tokens ou segredos.
- **Não tornar a aba visível ao usuário por padrão**, mas permitir inspeção/alteração quando necessário.
- As cinco abas históricas `LEGADO — ...` permanecem **ocultas só na cópia V1.0** para conservar descrições, tags e comentários que ainda não foram migrados para Docs. Não lê-las em fluxos normais; não excluí-las antes de um plano de preservação do material textual.

### 3.5 Regras de escrita

- Usar **IDs e cabeçalhos validados**, não números de coluna improvisados. Operações repetidas devem fazer `upsert` e conferir a mesma linha, em vez de criar outra.
- Congelamento do cabeçalho, filtros, formatação legível, validações/dropdowns e links reais devem sobreviver a cada atualização.
- Antes de mudar status, confirmar que a entrega exigida para aquele estágio existe e passou pelo gate correspondente.
- Não criar linhas-placeholder de produção. Gerar próximo ID ao aprovar um vídeo concreto.
- Se houver ambiguidades (duas planilhas compatíveis, duas pastas de raiz, links conflitantes), solicitar seleção em vez de assumir.

## 4. Padrão futuro de roteiro formatado automaticamente

**Fonte editorial para templates:** docs existentes `VD_0008` e `SH_0025` (estrutura observada). **Templates oficiais ainda precisam ser criados e aprovados.**

Criação por cópia de um template **Google Docs nativo** com estilos de parágrafo reais; não criar um Doc de texto cru e pedir depois para o usuário solicitar formatação.

**Estrutura proposta:**
1. `TITLE`: `[VD_####|SH_####] — [Título de trabalho]`, tipo, versão e status.
2. `HEADING_1: Premissa e embalagem` — tese, promessa, título A/B, conceitos de thumbnails e pesquisas.
3. `HEADING_1: Roteiro audiovisual` — capítulos/trechos com `HEADING_2`, blocos claros `NARRAÇÃO`, `SOM DA CENA`, `MOTION / TSX`, `NOX`, `SFX`, `LEGENDA` quando cabível. Duração estimada, intenção e links para cenas/assets quando úteis.
4. Abertura: gancho e valor imediatos, sobretudo nos primeiros 30 s de longos; adaptação ao 9:16 e atenção imediata em Shorts.
5. CTAs no corpo de longos e no encerramento de Shorts, integrados à narração.
6. `HEADING_1: Fontes e checagem factual` — evidências e interpretação separadas.
7. `HEADING_1: Revisões` — comentários concretos e critérios de aprovação.
8. `HEADING_1: Kit de publicação — NÃO NARRAR` — descrição, tags, comentário, capítulos **com timestamps verificados**, links de afiliados pertinentes e divulgação, versão para redes quando necessário.
9. Roteiro Short: legendas por padrão, ocultas em cenas exclusivamente tipográficas, duração-alvo **≥60 s** como preferência editorial atual, CTA para o canal no final.
10. Aplicar tipografia/hierarquia/espaçamento e bullets nativos; revisar com leitura de volta do Google Docs. Estilos e seções são parte da criação, **não uma segunda tarefa pedida pelo usuário**.

Não reformatar Docs históricos indiscriminadamente; alguns são Markdown/Word/TXT e precisam de migração dirigida se desejado.

## 5. Comportamento de instalação e reparo no Google Drive

Em ChatGPT comum, Work, Codex ou outro ambiente, obedecer às ferramentas realmente disponíveis.

**Bootstrap idempotente:**
1. Detectar conexão, permissões, conta/Drive e instância já configurada.
2. Buscar raiz **Diazverso**, identificar estrutura e conferir `Config` + IDs reais, sem assumir que nomes iguais são a mesma conta.
3. Validar quatro subpastas canônicas, planilha, abas, cabeçalhos e validações. Se tudo existe, **não criar nada**.
4. Se faltar estrutura, mostrar alterações previstas e **solicitar a autorização pertinente**; então criar **apenas os itens ausentes**, aplicando formatação e vínculos automaticamente.
5. Para uma planilha existente incompatível, propor migração/cópia com backup e sem sobrescrever valores silenciosamente.
6. Após cada criação, verificar pasta, ID, link, styles, dropdowns e leitura de retorno; armazenar configurações da conta em local autorizado. Não expor configurações de outras pessoas.
7. Em conexão ausente ou operação negada, **relatar exatamente o bloqueio** e não inventar sucesso.

**Nota:** uma skill define procedimentos, mas não cria permissões nem renderiza vídeo sozinha. O ChatGPT comum pode coordenar, pesquisar, criar/editar Docs/Sheets quando conectado; compilação/render Remotion precisa de ambiente adequado, Work/Codex, máquina ou Content Lab/MCP habilitado.

## 6. Pipeline passo a passo: "Vamos criar um vídeo"

| Etapa | Trabalho (subtarefa verificável) | Resultado salvo e local | Gate |
| --- | --- | --- | --- |
| 0. Preparação | Validar conexão Drive, planilha, instalação e projeto; escolher LONGO ou SHORT conforme intenção. | `Config` / contexto de execução | Pastas, planilha e permissões verificadas |
| 1. Ideação | Encontrar ou criar pauta; investigar assunto e interesse, preservar fontes/hipóteses. | Linha em `Ideias` (TF_####) se pauta não aprovada | Ideia investigável |
| 2. Tese e packaging inicial | Definir tese, promessa, contraponto, propostas de títulos A/B e thumbnails A/B com evidências. | Atualizar Ideias enquanto exploratória | Aprovação de direção editorial |
| 3. Promoção da ideia | Criar `VD_####`/`SH_####` com dados, atualizar `Produções`; verificar; **apagar ideia da aba Ideias** só depois. | Linha única em `Produções` + origem no novo registro | Sem duplicação nem perda |
| 4. Roteiro | Criar Doc **já formatado** em `Roteiros/Longos` ou `Roteiros/Shorts`, elaborar narração, humor, Nox, áudio de cenas e indicações de motion. | Link na coluna `ROTEIRO` | Revisão editorial, factual e de voz |
| 5. Pré-edição / assets | Decupar cenas/quadros, direitos e arquivos; usar biblioteca plugin e pesquisar assets adicionais. | Plano de cenas por roteiro, não pastas extras no Drive | Assets/uso/licenças conferidos |
| 6. Thumbnails | Elaborar A/B (ou uma Short), revisar tema/contraste/legibilidade, salvar versões aprovadas. | `Thumbnails/Longos` ou `Thumbnails/Shorts`; links H/I da `Produções` | Conferência de arquivo + embalagem |
| 7. Motion / edição | Gerar TSX Remotion por microcenas, sincronizar voz/câmera/parallax/Nox/Anton/SFX, criar versão horizontal ou 9:16. | Arquivos do editor local/Content Lab ou repositório de projeto apropriado; Drive só documentos finais definidos | Preview/render parcial |
| 8. Revisão AV | Auditar quadros/cortes/legendas/áudio, SFX, movimento, preto acidental, safe areas, copyright e retenção; corrigir e re-renderizar. | Estado em `REVISÃO`; evidências conforme ferramenta | Aprovação humana final |
| 9. Pacote publicação | Gerar título, descrição e tags coerentes, afiliados relevantes ativos, CTA, capítulos com tempos reais, comentário e outras redes. | Seção no Google Doc e/ou link `KIT PUBLICAÇÃO` | Revisão publicável |
| 10. Publicação | Somente com autorização, publicar/agendar onde houver ferramenta e permissão; se manual, instruir sem fingir que publicou. | `STATUS=PUBLICADO`, URL e data real no Sheets | URL verificável |
| 11. Aprendizado | Revisar métricas quando disponíveis e criar hipóteses de melhoria para próximos vídeos. | Próximos registros de ideias ou observações realmente úteis | Não reescrever vídeo histórico sem motivo |

**Política de orquestração:** executar uma subtarefa por vez, trabalhar a partir do último status e artefatos existentes, preservar progresso; não repetidamente perguntar o que já está no Sheets/Docs. Ativar skills especializadas sob demanda para manter tokens baixos. Escolha editorial humana em decisões que mudam tese, arte, voz e publicação. As fases são modulares: uma conversa só de ideias não deve forçar criação de roteiro, thumbnail ou edição sem sinalização do criador.

## 7. Conferência da estrutura realmente implantada

**No Drive atual, 2026-11-10:**
- Nova raiz, quatro subpastas e planilha nativa V1.0 criadas.
- **33 vídeos com `PUBLICADO`**, 15 ideias e 8 afiliados (`A CONFERIR`). Observações artificiais de legado removidas das 33 linhas; campo `OBSERVAÇÕES` permanece disponível.
- **35 arquivos de roteiro realocados**, incluindo 10 arquivos de longos e 25 de Shorts. **30 imagens de thumbnail realocadas**, incluindo 16 longos e 14 Shorts. IDs e URLs dos 33 roteiros preservados; links de thumbnail de quatro Shorts corrigidos.
- **Pastas antigas de Roteiros e Thumbnail foram excluídas, inclusive subpastas por vídeo já esvaziadas.** Conteúdo auxiliar não migrado foi movido para [Diazverso — Acervo legado (temporário)](https://drive.google.com/drive/folders/1SZIKGdq7wrZs4eo859WA6M-fJxiijmO_), fora da estrutura ativa, para revisão antes da incorporação ao plugin.
- **Planilha original antiga não pôde ser excluída:** [Canal do YT histórico](https://docs.google.com/spreadsheets/d/1s_7ybuYet0La5_cem01p_UwTNzN2uIq5vfLAgWEF_s8/edit) é compartilhada e a tentativa de exclusão retornou **FORBIDDEN**. A cópia V1.0 funciona de modo independente e tem as abas `LEGADO` ocultas como backup.
- **Ainda não implementados:** provisionamento automático de contas novas, templates Google Docs definitivos, conversão dos Docs históricos, renderização/QA integral pelo plugin, importação dos assets canônicos ao GitHub, checagem comercial de links de afiliados e transações de promoção de Ideias no Google Sheets.

## 7A. Bibliotecas auxiliares reorganizadas em 10/11/2026

O usuário ampliou explicitamente o escopo do Drive: além do acervo de roteiros/thumbnails, as cinco bibliotecas `Assets`, `Backgrounds`, `Memes`, `Músicas` e `Sounds` foram realocadas para dentro da raiz `Diazverso`, com categorias internas reorganizadas.

**Fonte de verdade para este conjunto:** [ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md](ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md), contendo links reais, árvore detalhada, contagens verificadas e pendências de licença e triagem. Referência sob demanda, não carregar em toda solicitação de roteiro.

Essa mudança **não** significa copiar todos os assets ao pacote instalável. O plugin deve futuramente oferecer descoberta idempotente das bibliotecas e seleção contextual por função de edição, com direitos verificados. Mídias antigas ou genéricas preservadas em `99 - Para avaliar` não são assets aprovados para uso automático. O sistema de busca/catalogação ainda não foi implementado. A estrutura mínima de produção continua válida mesmo sem bibliotecas, para instalações que não as tenham.

## 8. Critérios de aceitação para o plugin futuro

- Drive vazio → criação assistida de raiz, 4 subpastas e planilha **formatada**; segunda execução → não duplica nada.
- Drive parcialmente configurado → repara só o ausente.
- Planilha com esquema válido → reconhece e trabalha sem perguntar onde fica cada coluna; sem permissão → falha explícita.
- Criar ideia → 1 linha válida em Ideias.
- Promover ideia → 1 nova produção completa e 0 linhas ativas com aquele TF na aba Ideias; em falha → ideia original intacta.
- Criar roteiro → Doc nativo com headings, seções e formatação verificada, no local exato, link sincronizado.
- Criar thumbnails → arquivos com ID/versionamento e links de **arquivo**; não links de subpasta.
- Editar/renderizar → evidências QA; não anunciar que passou sem rodar revisões reais.
- Publicar → só marcar PUBLICADO após URL/data/ação real e confirmação de que está público ou conforme estado de publicação verificado.
- Testar longos e Shorts separadamente (incluindo legendas e CTA dos Shorts); preservar nomes, estados, links e direitos de terceiros.

**Este documento é o roteiro de implementação, não a implementação automática. Ele poderá ser refinado após o criador validar todo o fluxo.**
