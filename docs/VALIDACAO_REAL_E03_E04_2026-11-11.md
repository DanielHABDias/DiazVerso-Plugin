# Validação real da instalação Diazverso — E03/E04 (11/11/2026)

**Operação:** somente consultas reais ao Drive/Sheets conectados, sem criar, mover, excluir ou alterar dados.

## E03 — Descoberta idempotente e reparos quando necessários

A busca real com filtro de pai no Google Drive confirmou **uma** pasta raiz `Diazverso`, ID `1SbOI-GtWAaWzxFh1ysG5DOjf0DZ8XSYh`. Dentro dela há exatamente os objetos essenciais: `Roteiros` (`1pYzyLLSPpH6HYu-sEaHt5JHs1gMlMNB6`), `Thumbnails` (`1gYR4s8oR6ZSHg-TnqL0EUA7yplU1H18B`) e a planilha nativa `Canal do YT — V1.0 (Diazverso)`. Nas duas pastas foram encontradas exatamente as subpastas `Longos` e `Shorts`, sem homônimos no mesmo pai. Estão presentes também as cinco bibliotecas opcionais `Assets`, `Backgrounds`, `Memes`, `Músicas` e `Sounds`.

O procedimento de E03 `discover_structure.py`/ `plan_repairs()` é somente leitura e, para um ambiente completo, **não precisa criar nenhum item**. Os cenários sintéticos de preflight mostram bloqueio se pai/listagem não forem recentes, se nomes colidirem ou se faltar autorização. Não foi executado reparo destrutivo, porque **não havia estrutura faltante**. Esta evidência valida o comportamento idempotente esperado na instalação atual; o ramo de criação em uma instalação nova continua protegido por autorização, readback e testes isolados no controlador.

## E04 — Esquema de Sheets

Planilha real localizada: [Canal do YT — V1.0 (Diazverso)](https://docs.google.com/spreadsheets/d/12_bYL2N9mwRj4lel_fNVOOPBruth-Ca2FsAjrgU1VQk/edit). Metadados e cabeçalhos da linha 1 das abas `Produções` (17 colunas), `Ideias` (12), `Afiliados` (10) e `Config` (3) correspondem ao contrato local. A primeira linha está congelada nas quatro abas, `Config` está oculta e as cinco abas `LEGADO` foram preservadas/ocultas.

Foi feita leitura real de `userEnteredFormat`, `effectiveFormat` e `dataValidation` das primeiras linhas: **todos os cabeçalhos das quatro abas estão em negrito e têm cor de fundo**. Existem dropdowns nas colunas relevantes: `Produções` B (TIPO), D (STATUS), E (PRIORIDADE), O (REVISÃO); `Ideias` G (PRIORIDADE), J (STATUS); `Afiliados` G (STATUS). Os dropdowns foram conferidos na primeira linha de dados, não em todas as futuras linhas do grid.

**Ponto não validado:** a leitura de metadados não demonstrou `basicFilter` ativo nas abas; o contrato pede preservação dos filtros quando existirem. Não inventar filtro criado, não aplicar alteração na planilha do criador sem autorização. E04 permanece pendente se o critério exigir verificação ou criação de filtros em todas as abas, além do teste de readback das atualizações autorizadas em ambiente isolado.

**Síntese:** E03 atende cenário completo/idempotente real. E04 tem cabeçalhos, congelamento, visibilidade, formatação de header e dropdowns essenciais comprovados, mas filtro/atualização de metadados ainda não foram testados de ponta a ponta. Nenhuma edição feita.
