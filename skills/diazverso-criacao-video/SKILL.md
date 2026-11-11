---
name: diazverso-criacao-video
description: "Use quando o criador disser 'vamos criar um vídeo', 'vamos fazer um Short', 'continue o vídeo' ou pedir para coordenar as etapas de produção Diazverso, da pauta ao kit de publicação para postagem manual pelo criador."
---

# Diazverso — Orquestração de um vídeo por microtarefa

**Objetivo:** coordenar a produção de um vídeo longo ou Short até entregar o **kit final revisado para postagem exclusivamente manual pelo criador**. Não há skill, integração, instruções ou automação de envio/agendamento/publicação de vídeos. Ferramentas especializadas de produção são usadas somente quando disponíveis.

## Início ou retomada

1. Identificar se o pedido é **novo vídeo** ou **continuação**. Se houver Drive/Sheets conectados, localizar o vídeo e status existentes antes de criar outro; se não houver, realizar apenas o que for possível e relatar a limitação.
2. Confirmar apenas a decisão editorial que ainda faltar (tema, formato ou tese) **quando isso impedir a próxima ação**. Não repetir perguntas respondidas na planilha, nos documentos ou nesta conversa.
3. Escolher **uma próxima microtarefa**. Carregar a skill específica e as referências necessárias **sob demanda**; aplicar `diazverso-core` para decisões criativas quando necessário. Não carregar todas as skills de vídeo nem as 44 antigas.
4. Registrar uma saída verificável, revisar e somente após aprovação avançar automaticamente para a próxima tarefa **independente e autorizada**. Em ações críticas (escolha da tese/arte e exclusão), respeitar a aprovação do criador e as permissões reais. **A postagem não é uma ação do plugin.**

## Pipeline e rastreabilidade

| Estado/fase | Microentrega | Persistência quando disponível | Gate |
| --- | --- | --- | --- |
| IDEIA | Pauta, tese inicial, fontes e timing | Aba `Ideias` (TF_####) | Ideia distinta e investigável |
| PLANEJADO/PESQUISA | Tese aprovada, referências, título A/B e conceito de thumb | Aba `Produções` (VD_#### ou SH_####) | Pesquisa/fatos verificados |
| ROTEIRO | Documento audiovisual completo, já formatado | `Roteiros/Longos` ou `Roteiros/Shorts` | Aplicar F07 (`diazverso-revisao-fatos`), F08 (`diazverso-revisao-estrutura`), F09 (`diazverso-revisao-voz`) e F10 (`diazverso-aprovacao-roteiro`) sobre a mesma versão; **aprovação explícita do criador** antes da produção técnica |
| ASSETS | Plano de cenas, Nox, fundos, mídia e direitos | Referência no roteiro; biblioteca aprovada | Direitos e assets verificados |
| EDIÇÃO | Composição TSX/Remotion em executor independente | Runtime de edição real | Preview e amostras de quadros |
| REVISÃO FINAL | QA narrativo, audiovisual, legendas/áudio e correções | Evidências do editor/roteiro | Aprovado após novo render |
| PRONTO/AGENDADO | Kit com título, descrição, tags, comentários, fontes e afiliados verificados | Seção não narrada do Google Doc/planilha | Pacote conferido |
| PUBLICADO (registro posterior opcional) | URL e data informadas e verificadas após a postagem manual pelo criador | Aba `Produções`, se conectada | Nunca publicar pelo plugin nem inferir postagem pelo kit pronto |

**Regra da aba Ideias:** ao aprovar transformação em vídeo, criar registro de Produção e confirmar que gravou; **somente depois remover a ideia original**. Se falhar, preservar a ideia para recuperação. Essa operação exige integração real ainda prevista nas tarefas E05–E07; não alegar que está implementada agora.

**Arquivos:** usar a raiz `Diazverso`, planilha do canal, `Roteiros/{Longos,Shorts}`, `Thumbnails/{Longos,Shorts}` e bibliotecas Assets/Backgrounds/Memes/Músicas/Sounds quando a conexão permitir. Nomes e IDs da conta do criador não são universais.

**Shorts:** 9:16, legendas sincronizadas com exceções de tipografia integral, gancho rápido e CTA contextual. A duração de pelo menos 60 s é preferência editorial atual, não limite de plataforma.

## Kit final de publicação manual — K01

A produção termina com um **pacote pronto para o criador publicar pessoalmente**, não com upload/postagem feita ou orientada pelo ChatGPT.

**Entradas:** roteiro aprovado (mesma versão do vídeo final), título escolhido, arquivos finais de vídeo e thumbnail efetivamente verificados, fontes, decisões de QA, links afiliados pertinentes já conferidos e informações editoriais. Sem vídeo renderizado/QA, entregar **rascunho de kit** marcado como pendente, não kit final aprovado.

**Saída utilizável:** título final, descrição PT-BR pronta para copiar, fontes/atribuições, links pertinentes e divulgação de afiliação quando aplicável, tags relevantes sem exageros, comentário fixado opcional e capítulos **somente com timestamps conferidos no render final**. Para K02, usar `../diazverso-drive-setup/scripts/affiliate_selection.py` apenas sobre uma leitura atual da aba `Afiliados`: selecionar somente itens `ATIVO`, pertinentes e cujo link/destino/condições foram **verificados nesta produção**; não deduzir validade da data antiga de verificação. Se nenhum passar, não inserir afiliados por obrigação. Quando houver links de afiliados, incluir divulgação transparente da relação comercial. O script não verifica destinos por conta própria nem publica vídeos. Para Shorts, adaptar linguagem e CTA ao formato sem fingir dados. Informar quais arquivos aprovados compõem o kit, com referência verificável e pendências. Não inventar links, datas, estatísticas, capítulos ou patrocínios.

**Geração executável:** com os dados aprovados, usar `scripts/build_publication_kit.py <entrada.json>` (JSON local) para obter título, descrição, fontes, tags, capítulos confirmados e afiliados verificados. O gerador aceita apenas dados fornecidos e flags de revisão; **não verifica por si mesmo a existência dos arquivos nem a veracidade das aprovações**. Validar esses insumos na execução do fluxo; nenhum upload é realizado.

**Finalização:** registrar `KIT PRONTO PARA POSTAGEM MANUAL` apenas quando roteiro, arte, render, QA e conteúdo textual realmente aprovados. Caso contrário, `KIT PARCIAL — PENDÊNCIAS`, listando somente o que falta. **Não executar nem ensinar upload, agendamento ou postagem**, nem importar a skill de postagem antiga. `PUBLICADO` é apenas registro posterior, após o criador postar manualmente e fornecer evidência de URL/data reais.

## Análise depois da postagem manual — K05

Somente **após o criador ter postado o vídeo**, e se ele fornecer métricas reais (com data de coleta, fonte e ID da produção), usar `scripts/analyze_metrics.py` com os dados recebidos para registrar observações, CTR calculável e duração média proporcional quando as medidas necessárias existirem. Sem acesso ou dados reais, responder `MÉTRICAS NÃO DISPONÍVEIS`, sem inferir visualizações, receita ou retenção. Comparações com outros vídeos exigem dados comparáveis, período e contexto.

Transformar achados em **hipóteses de pauta a pesquisar**, não conclusões sobre o algoritmo. Registrar novas ideias em `Ideias` somente após seleção editorial e gravação autorizada pelo fluxo E05; não criar linhas automaticamente. **Não acessar, agendar, enviar ou postar vídeos** por causa desta análise.

## Retomada entre sessões

Quando a ferramenta permitir persistência, usar `schemas/estado-producao-v1.schema.json` como **formato mínimo de intercâmbio**, não como banco paralelo: `id`, `tipo`, `fase`, `proxima_tarefa`, `revisao`, `links` e bloqueio opcional. **Fonte de verdade**: linha do vídeo no Google Sheets, roteiro Google Docs e evidências dos artefatos; atualizar/relêr após cada ação importante. Sem conector, não alegar estado salvo ou continuidade automática. Evitar credenciais no registro.

## Revisão antes de cada próximo passo

- Revisar **integridade da saída** (arquivo, coluna, link, prévia, testes e dados reais).
- Revisar **identidade** (tese, voz, Nox, HQ madura, humor contextual).
- Revisar **fontes e direitos**, especialmente imagens, música, vídeos e links afiliados.
- Em produção técnica, revisar **render e áudio reais** quando houver executor; sem isso, registrar `NÃO TESTADO`.
- Se a revisão falhar, corrigir a microtarefa em curso antes de avançar. Se o passo exigir autorização ou ferramenta ausente, guardar o estado como **BLOQUEADO** e não inventar sucesso.

Em caso de ambiguidade entre tarefas de ideias, títulos, roteiro, revisão, thumbnail, Nox, motion, música, Shorts e kit de publicação manual, consultar `references/intencoes.md` **sob demanda**; não carregar a tabela em toda conversa.

## Informações adicionais sob demanda

- `docs/CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md` — contrato de planilha e pastas.
- `docs/ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md` — mídias, triagem e licenças.
- `docs/REGISTRO_EXECUCAO_E_PENDENCIAS.md` — problemas e gates ainda não aprovados.
- `skills/diazverso-contexto-eficiente/references/roteamento.md` — quando houver disputa entre skills.

**Fronteira final:** após o kit revisado, a produção é entregue ao criador para **postagem manual**. Não descrever etapas de upload, envio, agendamento ou postagem. A atualização posterior de status/link é somente registro factual após confirmação externa do criador.

**Estado atual do projeto:** a orquestradora descreve procedimentos; **não** significa que Drive/editor estejam integrados ou testados.
