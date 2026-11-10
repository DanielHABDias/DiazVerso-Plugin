---
name: diazverso-criacao-video
description: "Use quando o criador disser 'vamos criar um vídeo', 'vamos fazer um Short', 'continue o vídeo' ou pedir para coordenar as etapas de produção Diazverso, da pauta ao pacote de publicação."
---

# Diazverso — Orquestração de um vídeo por microtarefa

**Objetivo:** coordenar a produção de um vídeo longo ou Short, mantendo registro, revisão e estado. Esta skill **não implementa** Google APIs, geração de imagem, síntese de áudio, TSX, render nem publicação; utilizar ferramentas e skills especializadas somente quando estiverem disponíveis.

## Início ou retomada

1. Identificar se o pedido é **novo vídeo** ou **continuação**. Se houver Drive/Sheets conectados, localizar o vídeo e status existentes antes de criar outro; se não houver, realizar apenas o que for possível e relatar a limitação.
2. Confirmar apenas a decisão editorial que ainda faltar (tema, formato ou tese) **quando isso impedir a próxima ação**. Não repetir perguntas respondidas na planilha, nos documentos ou nesta conversa.
3. Escolher **uma próxima microtarefa**. Carregar a skill específica e as referências necessárias **sob demanda**; aplicar `diazverso-core` para decisões criativas quando necessário. Não carregar todas as skills de vídeo nem as 44 antigas.
4. Registrar uma saída verificável, revisar e somente após aprovação avançar automaticamente para a próxima tarefa **independente e autorizada**. Em ações críticas (escolha da tese/arte, exclusão, publicação), respeitar a aprovação do criador e as permissões reais.

## Pipeline e rastreabilidade

| Estado/fase | Microentrega | Persistência quando disponível | Gate |
| --- | --- | --- | --- |
| IDEIA | Pauta, tese inicial, fontes e timing | Aba `Ideias` (TF_####) | Ideia distinta e investigável |
| PLANEJADO/PESQUISA | Tese aprovada, referências, título A/B e conceito de thumb | Aba `Produções` (VD_#### ou SH_####) | Pesquisa/fatos verificados |
| ROTEIRO | Documento audiovisual completo, já formatado | `Roteiros/Longos` ou `Roteiros/Shorts` | Roteiro aprovado |
| ASSETS | Plano de cenas, Nox, fundos, mídia e direitos | Referência no roteiro; biblioteca aprovada | Direitos e assets verificados |
| EDIÇÃO | Composição TSX/Remotion em executor independente | Runtime de edição real | Preview e amostras de quadros |
| REVISÃO FINAL | QA narrativo, audiovisual, legendas/áudio e correções | Evidências do editor/roteiro | Aprovado após novo render |
| PRONTO/AGENDADO | Kit com título, descrição, tags, comentários, fontes e afiliados verificados | Seção não narrada do Google Doc/planilha | Pacote conferido |
| PUBLICADO | URL e data reais, resultado publicado | Aba `Produções` | Publicação confirmada no serviço |

**Regra da aba Ideias:** ao aprovar transformação em vídeo, criar registro de Produção e confirmar que gravou; **somente depois remover a ideia original**. Se falhar, preservar a ideia para recuperação. Essa operação exige integração real ainda prevista nas tarefas E05–E07; não alegar que está implementada agora.

**Arquivos:** usar a raiz `Diazverso`, planilha do canal, `Roteiros/{Longos,Shorts}`, `Thumbnails/{Longos,Shorts}` e bibliotecas Assets/Backgrounds/Memes/Músicas/Sounds quando a conexão permitir. Nomes e IDs da conta do criador não são universais.

**Shorts:** 9:16, legendas sincronizadas com exceções de tipografia integral, gancho rápido e CTA contextual. A duração de pelo menos 60 s é preferência editorial atual, não limite de plataforma.

## Revisão antes de cada próximo passo

- Revisar **integridade da saída** (arquivo, coluna, link, prévia, testes e dados reais).
- Revisar **identidade** (tese, voz, Nox, HQ madura, humor contextual).
- Revisar **fontes e direitos**, especialmente imagens, música, vídeos e links afiliados.
- Em produção técnica, revisar **render e áudio reais** quando houver executor; sem isso, registrar `NÃO TESTADO`.
- Se a revisão falhar, corrigir a microtarefa em curso antes de avançar. Se o passo exigir autorização ou ferramenta ausente, guardar o estado como **BLOQUEADO** e não inventar sucesso.

## Informações adicionais sob demanda

- `docs/CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md` — contrato de planilha e pastas.
- `docs/ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md` — mídias, triagem e licenças.
- `docs/REGISTRO_EXECUCAO_E_PENDENCIAS.md` — problemas e gates ainda não aprovados.
- `skills/diazverso-contexto-eficiente/references/roteamento.md` — quando houver disputa entre skills.

**Estado atual do projeto:** a orquestradora descreve procedimentos; **não** significa que a cadeia Drive → editor → YouTube esteja conectada ou testada.
