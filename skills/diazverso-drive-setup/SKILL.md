---
name: diazverso-drive-setup
description: "Use quando for preciso localizar, validar, criar ou reparar a estrutura Diazverso no Google Drive e a planilha Canal do YT com suas abas, evitando pastas duplicadas e respeitando permissões."
---

# Diazverso — Estrutura de Drive e planilha

**Finalidade:** localizar o espaço do canal, verificar seu esquema e corrigir itens faltantes **somente com conexão e autorização**. Uma skill não cria acesso à conta; nunca alegar criação quando não houve ação.

## Estrutura canônica atual

```text
Diazverso/
├── Canal do YT — V1.0 (Diazverso)  [Google Sheets]
├── Roteiros/
│   ├── Longos/
│   └── Shorts/
├── Thumbnails/
│   ├── Longos/
│   └── Shorts/
├── Assets/                         [biblioteca opcional]
├── Backgrounds/                    [biblioteca opcional]
├── Memes/                          [biblioteca opcional]
├── Músicas/                        [biblioteca opcional]
└── Sounds/                         [biblioteca opcional]
```

Pastas de vídeos individuais não devem ser criadas por padrão. O ID `VD_####` ou `SH_####` aparece no nome do arquivo e no vínculo da planilha; `TF_####` identifica ideias ainda não promovidas.

## Descobrir → validar → reparar → conferir

1. **Identificar conexão e escopo.** Verificar quais contas/Drives estão conectados e permissões efetivas de leitura/escrita; não presumir a conta do criador em instalações de terceiros.
2. **Descobrir antes de criar (E02):** seguir `references/deteccao-idempotente.md`: buscar nome exato e tipo, esgotar paginação, confirmar pais, rejeitar ambiguidade e validar IDs da própria instalação. Quando houver executor Python, `scripts/discover_structure.py` resolve o snapshot de metadados **somente em leitura**, sem credenciais nem criação. Repetição deve produzir mesmo resultado. Com homônimos ou compartilhamentos ambíguos, pedir seleção; nunca escolher a primeira ocorrência.
3. **Validar a estrutura:** `Roteiros/Longos`, `Roteiros/Shorts`, `Thumbnails/Longos`, `Thumbnails/Shorts`, planilha e suas abas. As cinco bibliotecas adicionais são **opcionais**; reaproveitar caso já existam.
4. **Comparar com o esquema (E04):** consultar metadados das abas e **linha 1** das quatro abas, sem carregar toda a planilha. `scripts/validate_sheet_schema.py` valida os nomes, cabeçalhos, congelamento básico e `Config` oculta em um snapshot de leitura, sem sobrescrever valores. `plan_safe_metadata_repairs(snapshot)` prepara **apenas** operações nativas `updateSheetProperties` restritas aos campos `gridProperties.frozenRowCount` e `hidden` se o cabeçalho real tiver sido lido e for idêntico ao contrato; nunca emite updates de células. **Não executar** essas propostas em planilha do criador sem autorização específica, releitura atual e readback após aplicação. Conferir dropdowns, filtros e formatação nativa pelo conector se houver suspeita de problema; o script **não valida esses aspectos**. Se houver diferença, apresentar correção específica e obter autorização antes de reparar com ferramentas nativas; reler depois. Preservar integralmente as abas `LEGADO`. Contrato detalhado: `docs/CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md`.
5. **Prévia e autorização:** mostrar apenas os itens faltantes e a alteração proposta. Nunca mover/apagar a estrutura de outra conta, criar duplicatas, sobrescrever links, títulos e dados existentes ou realizar migração destrutiva sem consentimento pertinente.
6. **Reparar idempotentemente (E03):** após E02, usar `scripts/discover_structure.py --plan <snapshot.json>` para obter um plano **sem escrita** apenas de pastas comprovadamente ausentes; bibliotecas opcionais somente se solicitadas (`--include-optional`). **Não criar** se a raiz, o pai, o ID ou a listagem estiverem ambíguos/incompletos. Para uma ação de pasta individual, `scripts/discover_structure.py` oferece `preflight_folder_create(action, fresh_parent=..., authorized=...)`: exige a listagem **recém-reconsultada e paginada até o fim** do pai exato, recusa colisão de nome mesmo quando MIME incorreto e somente retorna `SAFE_TO_ATTEMPT_CREATE_NOW` depois de autorização explícita. **Não executa a criação nem autentica por si o conector**; readback do ID/MIME/pai permanece obrigatório. Mostrar alterações e obter autorização específica; imediatamente antes de cada criação, **reconsultar o pai e seu conteúdo** e confirmar novamente a ausência, o nome, MIME e pai. Criar somente a pasta faltante com ferramenta autorizada, conferir o ID/pai por leitura de retorno e retomar a descoberta antes da próxima ação. Se a planilha estiver ausente, acionar o fluxo de criação nativa/validação E04, não criar arquivo vazio. Não criar pastas automaticamente a partir do plano; os IDs pertencem à instalação atual, nunca ao plugin distribuído.
7. **Ler de volta:** conferir pais, links, abas, formatos e acesso efetivo. Se algum item falhar, registrar precisamente onde ficou incompleto, para permitir reexecução sem duplicatas.

## Fluxo operacional

### Reserva persistente e execução nativa

Para novas ideias e promoções, usar `scripts/sheets_batch.py` (`reserve_insert`),
além dos planejadores abaixo. O host deve serializar **todos** os escritores da
mesma instalação; sem essa garantia, bloquear a escrita. Google Sheets não
oferece compare-and-swap e este módulo não cria um lock distribuído.

Fornecer snapshot completo e recém-lido com `spreadsheet_id`,
`complete_fresh_read=true` e `sheets.{Ideias,Produções,Config}` contendo
`sheet_id`, `grid_rows` e `rows` (cabeçalho na primeira linha). Conferir
`Config.CURRENT_SPREADSHEET_ID` contra o ID real; uma cópia de planilha pode
conter referências à instalação original. Reparar os vínculos da cópia antes
de usá-la; nunca seguir automaticamente os IDs herdados para escrever.

Na primeira reserva de cada prefixo, fornecer histórico completo verificado
de IDs emitidos (`historical_ids` e `history_verified_complete=true`), incluindo
itens removidos/promovidos. Depois, conservar `LAST_ID_TF/VD/SH` e as chaves
`OP_<operation_id>` em Config. Não decrementar contadores nem limpar o ledger.
Usar um `operation_id` estável por intenção, preservado no checkpoint.

O resultado agrupa linha formatada, contador e ledger em **um**
`spreadsheets.batchUpdate` atômico. Enviar `requests` pelo conector autorizado,
conferir ID/campos/Config por leitura de retorno e só então avançar. Em timeout
ou resposta perdida, reler e recalcular com o mesmo operation_id; não reenviar
um batch antigo. `ALREADY_COMMITTED` não requer escrita. Se o TF já saiu de
Ideias, `REQUIRES_RECONCILIATION` exige localizar sua produção pela origem e
conferir o Doc com `plan_promotion`, sem emitir novo ID. Um ID de operação com
conteúdo diferente é conflito. Escritores em outros hosts exigem coordenação
externa; não alegar exclusividade global por ter passado `single_writer=true`.

Os testes nativos de desenvolvimento cobriram inserção, promoção, readback,
repetição, erro HTTP 400 com rollback integral do batch, recuperação e remoção
somente do TF de teste após vínculo/Doc conferidos. O canal real não foi editado.

- **Criação de ideia (E05):** validar cabeçalhos de `Ideias` e ler IDs/temas atuais antes de escrever; `scripts/validate_sheet_schema.py` expõe `plan_new_idea(rows, fields)` para preparar a linha e detectar colisões **no conjunto recebido**, mas **não reserva IDs**. Antes de criar, consultar também o histórico de IDs TF já promovidos e/ou contador persistente da instalação (implementado em `sheets_batch.py`), para evitar reutilização de TF antigos; garantir exclusividade de escrita, reler dados imediatamente antes da inserção, usar escrita nativa de texto com formatação preservada, localizar a nova linha pelo ID e confirmar os campos. Na ausência dessas garantias, ficar em **PARCIAL**, sem inserir. Nunca criar ideias de teste na planilha real sem autorização.
- Ideias ainda exploratórias ficam em **Ideias**.
- **Promoção E06/E07:** usar `scripts/promotion.py` (função `plan_promotion`) com snapshot completo e atual de `Ideias` e `Produções` e histórico de IDs `VD/SH` já emitidos. **Uma transição por chamada:** planejar a produção com `IDEIA_ORIGEM_ID=TF_####` em `OBSERVAÇÕES` → confirmar criação e reler ID/origem → vincular `PRODUÇÃO VINCULADA` na ideia e reler → concluir/vincular Doc nativo formatado (F06) e conferir URL → somente com consentimento explícito para remoção, reler as duas abas imediatamente e excluir a ideia pelo ID atual, nunca por índice antigo. Em erro, repetir a detecção e retomar a fase encontrada, sem gerar outro vídeo ou apagar a ideia. `READY_FOR_AUTHORIZED_REMOVAL` é **proposta**, não permissão nem exclusão executada. Sem serialização de escritores, histórico confiável, readback ou ferramenta real, bloquear a escrita; não usar produções publicadas como teste.
- **Upsert E08:** usar `scripts/upsert_production.py` (`plan_upsert`) com cabeçalhos e linhas atuais de `Produções`; atualizar **somente** as células indicadas pelo planejador. Aceitar alteração de título A/B e links diretos de Doc/thumbnail apenas com origem verificada, detectar valor anterior incompatível antes de substituir, preservar ID/TIPO/observações, e nunca assumir índices de linha após edições concorrentes. Antes da escrita, reconsultar ID/linha e comparar valores antigos; escrever via conector Sheets com formato RAW, reler a linha exata e confirmar as mudanças. `STATUS=PUBLICADO` é somente **registro posterior da postagem manual feita pelo criador**, mediante confirmação real, data e link YouTube; a skill **não publica, agenda, envia nem ensina a postar**. `REVISÃO=APROVADO` requer decisão editorial registrada. Sem ferramenta ou confirmação, registrar pendência e **não inventar gravação**.
- Novos Docs de roteiro já devem nascer **formatados** em `Roteiros/Longos` ou `Roteiros/Shorts`; thumbnails ficam nos caminhos equivalentes.
- Textos completos de publicação devem ser mantidos no roteiro como seção não narrada, sem poluir colunas com textos enormes.
- As bibliotecas de mídia do Drive podem alimentar referências; **não assumir direitos de redistribuição** ou copiar automaticamente centenas de arquivos para o plugin.

## Resultado mínimo

Responder com: **estrutura encontrada**, **pendências de permissão/estrutura**, **alterações realizadas e verificadas** (ou não realizadas) e **próxima microtarefa**. Não informar sucesso quando conexão, gravação ou leitura de volta não ocorreram.
