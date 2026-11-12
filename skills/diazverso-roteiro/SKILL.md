---
name: diazverso-roteiro
description: "Use para criar ou atualizar o Google Doc nativo formatado de roteiro longo ou Short do Diazverso, usando os templates locais e vinculando o documento à produção correta na planilha, quando o Drive estiver conectado."
---

**Protocolo obrigatório Diazverso:** antes de agir, aplicar `../diazverso-contexto-eficiente/SKILL.md`. Ler uma vez por sessão/versão e reutilizar o contexto válido; abrir somente a skill principal e as dependências necessárias.

# Diazverso — Roteiro nativo, formatado e vinculado

**Objetivo:** produzir **um Google Doc nativo por vídeo**, no local certo, e atualizar **somente** a linha correspondente da aba `Produções`, com verificação após cada escrita. Esta skill não concede conexão ao Drive ou Sheets.

## Pré-condições

1. Consultar a linha da produção em `Produções`: ID estável `VD_####` ou `SH_####`, tipo LONGO/SHORT, tese/contexto e links atuais. Se a produção ainda não existir, **não criar silenciosamente** uma linha; ativar a etapa de promoção de ideia apropriada.
2. Verificar conta conectada, permissões, raiz `Diazverso`, `Roteiros/Longos` ou `Roteiros/Shorts`, ID da planilha e aba real. **Nenhum ID de Drive/Sheets é universal**.
3. Descobrir se a linha já tem roteiro ou há Doc com o ID na pasta. Se houver, **reutilizar/editar de forma controlada** após ler sua estrutura. Não duplicar por repetição.
4. Carregar `templates/roteiro-longo-v1.json` ou `templates/roteiro-short-v1.json` a partir do pacote. Não depender da conta Google do autor para obter o template.

## Direção editorial

O texto segue [escrever o roteiro](references/escrita.md): embalagem antes, gancho nos primeiros segundos, blocos ligados por "mas" ou "então", novo gancho a cada 60–90 s, uma frase por beat e direção visual entre colchetes. Pelo Content Lab, o roteiro vai em `creative_write`; o Google Doc é opcional quando o Drive estiver conectado. Sem acesso ao Drive, o roteiro fica no Content Lab (ou num arquivo local) e entra no pacote de registro manual para o criador subir ([modo manual](../diazverso-drive-setup/references/modo-manual.md)).

Antes de preencher o roteiro, escolher o formato e a entrega em [formatos editoriais](../diazverso-core/references/formatos-editoriais.md). Desenvolver a história/trajetória revelando complexidade e aprendizado, ou ensinar uma ideia prática/filosófica através dela. Usar tese, exemplos, comparação, crítica e conceitos para sustentar essa entrega, sem transformá-los em formatos principais isolados. Em ensino através de personagens, conectar situação da obra → escolha/consequência → princípio → aplicação ou reflexão específica, distinguindo fato, interpretação e analogia. Não obrigar uma moral em histórias nem prometer mudança garantida ao espectador. Para o uso das referências de linguagem, consultar [vídeos e princípios](../diazverso-core/references/referencias-audiovisuais.md) apenas quando necessário.

## Criação e preenchimento

- Para um Doc novo, usar ferramenta Google Drive para **criar um arquivo nativo** `application/vnd.google-apps.document`, com nome `VD_#### — [tema] — Roteiro` ou `SH_#### — [tema] — Roteiro`; mover ao destino correspondente.
- Usar `scripts/build_requests.py` desta skill **se houver executor Python**, ou aplicar a mesma lógica de maneira direta: inserir o texto dos parágrafos do template, aplicar `namedStyleType` `TITLE`, `SUBTITLE`, `HEADING_1`, `HEADING_2`, marcar etiquetas de `NARRAÇÃO` / `SOM DA CENA` em negrito. **Google Docs usa índices UTF-16**. Não formatar um texto plano só no chat e chamá-lo de Doc formatado.
- Se o editor permitir **cópia nativa de um modelo compatível**, copiar e preencher sem perder estilos; nunca presumir que ID de modelo de outra conta é válido.
- Substituir placeholders pelas informações **realmente aprovadas**; campos pendentes continuam identificados como tal. Distinguir fala da narração, áudio original autorizado de cena e direção visual **não narrada**. Preservar fontes, gate de revisão e `Kit de publicação — NÃO NARRAR`.
- Ler o Doc de volta e conferir pelo menos: título, hierarquia de parágrafos nativa, seções principais, texto, ID de vídeo, pasta correta e ausência de erros de conteúdo/posição. **Não declarar revisão audiovisual sem render.**

## Sincronizar a planilha com segurança

1. Reconsultar a aba `Produções` imediatamente antes de escrever; localizar a linha **pelo ID único**, não por índice antigo. Confirmar `TIPO`, tema e estado esperado.
2. Se a célula `ROTEIRO` já aponta ao mesmo Doc, operação é idempotente. Se aponta a outro Doc, **não substituir sem análise**.
3. Gravar a URL **do documento nativo**, não de uma pasta, usando a ação Google Sheets autorizada. Não sobrescrever títulos, observações, link YouTube ou estados de aprovação.
4. Ler a célula de volta, conferir ID/URL e verificar que há exatamente um vínculo ativo da produção. Se a escrita na planilha falhar após criar o Doc, **preservá-lo**, registrar `VÍNCULO PENDENTE` e retomar sem gerar cópia.
5. Atualizar status somente quando a etapa correspondente foi realmente executada; `PUBLICADO` exige publicação real e `REVISÃO APROVADA` exige evidência.

## Gate para próxima tarefa

**Roteiro criado na pasta certa + estilos/estrutura verificados + URL de roteiro sincronizada e relida na linha correta da planilha.** Quando algum destes passos não puder ser executado, marcar **PARCIAL/BLOQUEADO**, com evidência do Doc e pendência de sincronização. Não prosseguir como se tivesse concluído.

Para decisões editoriais carregar `diazverso-core` apenas quando necessário; para escolha de ferramentas consultar `diazverso-setup`, evitando carregar toda a documentação do projeto.
