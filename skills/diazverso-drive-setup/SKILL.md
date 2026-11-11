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
4. **Comparar com o esquema (E04):** consultar metadados das abas e **linha 1** das quatro abas, sem carregar toda a planilha. `scripts/validate_sheet_schema.py` valida os nomes, cabeçalhos, congelamento básico e `Config` oculta em um snapshot de leitura, sem sobrescrever valores. Conferir dropdowns, filtros e formatação nativa pelo conector se houver suspeita de problema; o script **não valida esses aspectos**. Se houver diferença, apresentar correção específica e obter autorização antes de reparar com ferramentas nativas; reler depois. Preservar integralmente as abas `LEGADO`. Contrato detalhado: `docs/CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md`.
5. **Prévia e autorização:** mostrar apenas os itens faltantes e a alteração proposta. Nunca mover/apagar a estrutura de outra conta, criar duplicatas, sobrescrever links, títulos e dados existentes ou realizar migração destrutiva sem consentimento pertinente.
6. **Reparar idempotentemente (E03):** após E02, usar `scripts/discover_structure.py --plan <snapshot.json>` para obter um plano **sem escrita** apenas de pastas comprovadamente ausentes; bibliotecas opcionais somente se solicitadas (`--include-optional`). **Não criar** se a raiz, o pai, o ID ou a listagem estiverem ambíguos/incompletos. Mostrar alterações e obter autorização específica; imediatamente antes de cada criação, **reconsultar o pai e seu conteúdo** e confirmar novamente a ausência, o nome, MIME e pai. Criar somente a pasta faltante com ferramenta autorizada, conferir o ID/pai por leitura de retorno e retomar a descoberta antes da próxima ação. Se a planilha estiver ausente, acionar o fluxo de criação nativa/validação E04, não criar arquivo vazio. Não criar pastas automaticamente a partir do plano; os IDs pertencem à instalação atual, nunca ao plugin distribuído.
7. **Ler de volta:** conferir pais, links, abas, formatos e acesso efetivo. Se algum item falhar, registrar precisamente onde ficou incompleto, para permitir reexecução sem duplicatas.

## Fluxo operacional

- **Criação de ideia (E05):** validar cabeçalhos de `Ideias` e ler IDs/temas atuais antes de escrever; `scripts/validate_sheet_schema.py` expõe `plan_new_idea(rows, fields)` para preparar a linha e detectar colisões **no conjunto recebido**, mas **não reserva IDs**. Antes de criar, consultar também o histórico de IDs TF já promovidos e/ou contador persistente da instalação (ainda não implementado), para evitar reutilização de TF antigos; garantir exclusividade de escrita, reler dados imediatamente antes da inserção, usar escrita nativa de texto com formatação preservada, localizar a nova linha pelo ID e confirmar os campos. Na ausência dessas garantias, ficar em **PARCIAL**, sem inserir. Nunca criar ideias de teste na planilha real sem autorização.
- Ideias ainda exploratórias ficam em **Ideias**.
- Ao promover, criar registro **Produções** primeiro e conferir a gravação; remover a ideia de **Ideias** somente depois do sucesso (ver regra editorial, implementação/rollback previstos nas tarefas E05–E07).
- Novos Docs de roteiro já devem nascer **formatados** em `Roteiros/Longos` ou `Roteiros/Shorts`; thumbnails ficam nos caminhos equivalentes.
- Textos completos de publicação devem ser mantidos no roteiro como seção não narrada, sem poluir colunas com textos enormes.
- As bibliotecas de mídia do Drive podem alimentar referências; **não assumir direitos de redistribuição** ou copiar automaticamente centenas de arquivos para o plugin.

## Resultado mínimo

Responder com: **estrutura encontrada**, **pendências de permissão/estrutura**, **alterações realizadas e verificadas** (ou não realizadas) e **próxima microtarefa**. Não informar sucesso quando conexão, gravação ou leitura de volta não ocorreram.
