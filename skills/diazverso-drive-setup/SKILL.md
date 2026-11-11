---
name: diazverso-drive-setup
description: "Use para localizar, configurar e operar a estrutura Google Drive/Docs/Sheets do Diazverso com identidade, idempotência e leitura de retorno."
---

**Protocolo obrigatório Diazverso:** antes de agir, aplicar `../diazverso-contexto-eficiente/SKILL.md`. Ler uma vez por sessão/versão e reutilizar o contexto válido; abrir somente a skill principal e as dependências necessárias.

# Organização e registros Google

O contrato da instalação está em [estrutura](references/estrutura.md). Cabeçalhos, IDs de pastas e dados operacionais devem vir da conta conectada, sem IDs pessoais embutidos no plugin.

## Descobrir e configurar

1. Conferir conexão e permissões da sessão.
2. Seguir [descoberta idempotente](references/deteccao-idempotente.md): nome exato, MIME, pais, identidade da instalação e paginação completa. Ambiguidade bloqueia criação.
3. `scripts/discover_structure.py` resolve um snapshot somente em leitura e oferece planos de reparo. Reconsultar o pai antes de criar uma pasta autorizada; conferir ID/MIME/pai depois. A ausência de bibliotecas opcionais não exige reparo.
4. Ler metadados e cabeçalhos das quatro abas. `scripts/validate_sheet_schema.py` confere esquema, congelamento e Config oculta. Os reparos de metadados são planos restritos; não sobrescrevem dados.
5. Preservar abas e células fora do pedido. Não tratar o conteúdo de outra instalação como configuração válida.

## Reservar IDs e criar registros

Usar `scripts/sheets_batch.py` (`reserve_insert`) com:
- snapshot completo e recém-lido, `spreadsheet_id`, `complete_fresh_read=true`;
- `sheets.{Ideias,Produções,Config}` com `sheet_id`, `grid_rows` e `rows`, cabeçalho primeiro;
- prefixo TF/VD/SH, `operation_id` estável e campos da intenção;
- histórico completo de IDs emitidos no bootstrap, inclusive removidos/promovidos.

**Exigir escritor único coordenado pelo host.** Não existe lock distribuído nem compare-and-swap do Sheets neste módulo. Sem coordenação, não executar a escrita.

Conferir CURRENT_SPREADSHEET_ID contra o ID real. Preservar LAST_ID_TF/VD/SH e OP_<operation_id> em Config. O batch reúne a linha, o contador e o ledger; enviá-lo pelo conector autorizado e reler os campos gravados.

Em resposta perdida ou timeout, reler e recalcular com a mesma operação. ALREADY_COMMITTED não exige escrita. REQUIRES_RECONCILIATION exige localizar a produção/origem antes de continuar. Mesmo operation_id com conteúdo diferente é conflito. Não reenviar batch em cache nem decrementar contadores.

`plan_new_idea`, em `validate_sheet_schema.py`, prepara os valores e detecta tema repetido; sozinho não reserva ID. Novas ideias usam status IDEIA e prioridade permitida pelo dropdown atual.

## Promover uma ideia

`scripts/promotion.py` (`plan_promotion`) orienta uma transição por vez:
1. Criar produção com IDEIA_ORIGEM_ID nas observações; conferir o registro.
2. Vincular PRODUÇÃO VINCULADA na ideia; reler.
3. Criar/conferir Doc nativo formatado pela skill de roteiro e vincular sua URL à produção.
4. Só então, com autorização de remoção pertinente, reler as duas abas e remover a ideia pelo ID atual.

Se houver falha, preservar a origem e retomar a fase encontrada. Não criar segundo vídeo nem remover a ideia com Doc ainda não conferido.

## Atualizar produção

`scripts/upsert_production.py` (`plan_upsert`) gera mudanças por célula a partir de cabeçalhos, ID/TIPO, valores atuais e valores esperados. Reconsultar antes da escrita, atualizar somente campos indicados e reler o resultado. Conflito exige reconciliação; nenhuma substituição silenciosa.

Links de roteiro e thumbnail devem identificar os arquivos reais, com MIME/pasta/conteúdo conferidos por ferramenta. Revisão APROVADO depende de decisão real do criador. PUBLICADO exige postagem manual confirmada, data válida e URL verificada; o plugin não publica, agenda ou ensina a postar.

Para afiliados, `scripts/affiliate_selection.py` usa apenas a leitura atual da aba e evidências pertinentes. Não presumir validade de destinos ou condições comerciais.

## Resultado

Informar apenas a alteração verificada ou bloqueio relevante e a próxima ação. Não confundir plano com gravação, campo preenchido com evidência ou arquivo presente com aprovação.
