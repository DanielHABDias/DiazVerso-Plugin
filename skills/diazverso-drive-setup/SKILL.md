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
4. **Comparar com o esquema:** aba `Produções` (IDs, formato, status, títulos A/B, thumbnails, roteiro, publicação), `Ideias`, `Afiliados` e `Config` técnica oculta. Checar cabeçalhos, dropdowns, filtros, congelamento de cabeçalho e IDs. O contrato detalhado está em `docs/CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md`; consultar somente se for reparar ou editar.
5. **Prévia e autorização:** mostrar apenas os itens faltantes e a alteração proposta. Nunca mover/apagar a estrutura de outra conta, criar duplicatas, sobrescrever links, títulos e dados existentes ou realizar migração destrutiva sem consentimento pertinente.
6. **Reparar idempotentemente:** criar **somente** pastas/abas faltantes após autorização. Salvar seus IDs na instância adequada, sem usar IDs fixos do Drive do criador como se fossem globais. Aplicar formatação nativa na planilha.
7. **Ler de volta:** conferir pais, links, abas, formatos e acesso efetivo. Se algum item falhar, registrar precisamente onde ficou incompleto, para permitir reexecução sem duplicatas.

## Fluxo operacional

- Ideias ainda exploratórias ficam em **Ideias**.
- Ao promover, criar registro **Produções** primeiro e conferir a gravação; remover a ideia de **Ideias** somente depois do sucesso (ver regra editorial, implementação/rollback previstos nas tarefas E05–E07).
- Novos Docs de roteiro já devem nascer **formatados** em `Roteiros/Longos` ou `Roteiros/Shorts`; thumbnails ficam nos caminhos equivalentes.
- Textos completos de publicação devem ser mantidos no roteiro como seção não narrada, sem poluir colunas com textos enormes.
- As bibliotecas de mídia do Drive podem alimentar referências; **não assumir direitos de redistribuição** ou copiar automaticamente centenas de arquivos para o plugin.

## Resultado mínimo

Responder com: **estrutura encontrada**, **pendências de permissão/estrutura**, **alterações realizadas e verificadas** (ou não realizadas) e **próxima microtarefa**. Não informar sucesso quando conexão, gravação ou leitura de volta não ocorreram.
