---
name: diazverso-criacao-video
description: "Use quando o criador disser 'vamos criar um vídeo', 'vamos fazer um Short', 'continue o vídeo' ou pedir para coordenar as etapas de produção Diazverso, da pauta ao kit de publicação para postagem manual pelo criador."
---

# Diazverso — Orquestração de um vídeo por microtarefa

**Objetivo:** coordenar a produção de um vídeo longo ou Short até entregar o **kit final revisado para postagem exclusivamente manual pelo criador**. Não há skill, integração, instruções ou automação de envio/agendamento/publicação de vídeos. Ferramentas especializadas de produção são usadas somente quando disponíveis.

## Degradação transparente de capacidades — L05

Antes de usar Drive/Docs/Sheets, render independente, FFmpeg ou EarShot, verificar as **permissões e ferramentas desta sessão**. Se um recurso estiver ausente, consultar `scripts/capability_fallback.py` com snapshot explícito `session_id`, `verified_at` e `capabilities` (booleanos `drive_read`, `drive_write`, `docs_write`, `sheets_read`, `sheets_write`, `render_runtime`, `ffmpeg`, `earshot`). Exemplo: `python skills/diazverso-criacao-video/scripts/capability_fallback.py <capacidades.json> --action draft_script_local --action create_native_doc --action render_preview`.

**Sem Drive:** produzir somente material editorial local (pauta, pesquisa preliminar, rascunho, briefing de thumbnail e decupagem), sem alegar Google Doc, links ou linha de planilha criados. **Sem Remotion:** entregar plano/contrato e comandos de render, nunca MP4/QA aprovado. **Sem FFmpeg:** não alegar extração de quadros; outros planos independentes seguem disponíveis. **Sem EarShot:** o revisor local PCM16 pode ser usado quando houver WAV real, mas não afirmar escuta, transcrição/sincronia ou qualquer uso de serviço externo. A disponibilidade não é prova de execução: o retorno `AVAILABLE_FOR_ATTEMPT` exige ainda a ação real, readback/arquivo e evidência para concluir.

O avaliador não chama ferramentas, não altera arquivos conectados nem publica vídeo. Se a ação for bloqueada, registrar qual recurso faltou e escolher a próxima microtarefa **independente** disponível, respeitando a autorização do criador. Não instalar recursos nem conectar serviços apenas por causa da ausência.

## Retomada entre processos e sessões — L04

O módulo `scripts/resume.py` implementa um **checkpoint local de referência**, sem ser um novo banco de verdade. Antes da pausa, obter da fonte de verdade atual (`Produções` no Sheets + evidências do Doc, quando conectados) `production_id`, `revision` monotônica, `next_task`, `completed` (ordem de tarefas confirmadas) e `source_ref`; `checkpoint(source)` adiciona hash SHA-256 canônico do registro. Guardar esse snapshot de forma segura no sistema disponível, sem credenciais.

Na sessão seguinte, **reler de fato** a fonte de verdade e montar `latest` com os mesmos campos e `fresh_read=True` somente após readback confirmado. `recover(checkpoint, latest)` verifica integridade, produção, referência, revisão, histórico de tarefas e impede retomar uma tarefa que já conste como concluída. Se os registros divergirem ou a leitura for antiga, retornar bloqueio e reconciliar antes de criar/editar algo. **A fonte mais recente prevalece quando avança de revisão**, evitando reexecutar tarefas concluídas após o último checkpoint.

CLI para diagnóstico sem escritas: `python skills/diazverso-criacao-video/scripts/resume.py <checkpoint.json> <latest.json>`. O arquivo `latest.json` deve corresponder a **leitura real verificada** — não marcar `fresh_read=True` só para fazer o teste passar. Foram executados localmente 13 testes Python, incluindo um **segundo processo** que lê arquivos persistidos, mas isso **não substitui um teste com duas sessões reais e Sheets conectado**. Não criar IDs, documentos, renders nem publicação automaticamente com esse script. L04 só será concluída integralmente quando houver readback de retomada em host real e confirmação de que nenhum item duplicou.

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
| ASSETS | Decupagem com `diazverso-decupagem`: objetivo por cena, narração, quadro, música/SFX, Nox, assets e direitos | Referência no roteiro; biblioteca aprovada | Plano audiovisual consistente; direitos e assets verificáveis |
| EDIÇÃO | Composição TSX/Remotion em executor independente | Runtime de edição real | Preview e amostras de quadros |
| REVISÃO FINAL | QA narrativo, audiovisual, legendas/áudio e correções | Evidências do editor/roteiro | Aprovado após novo render |
| PRONTO/AGENDADO | Kit com título, descrição, tags, comentários, fontes e afiliados verificados | Seção não narrada do Google Doc/planilha | Pacote conferido |
| PUBLICADO (registro posterior opcional) | URL e data informadas e verificadas após a postagem manual pelo criador | Aba `Produções`, se conectada | Nunca publicar pelo plugin nem inferir postagem pelo kit pronto |

**Regra da aba Ideias:** ao aprovar transformação em vídeo, criar registro de Produção e confirmar que gravou; **somente depois remover a ideia original**. Se falhar, preservar a ideia para recuperação. Essa operação exige integração real ainda prevista nas tarefas E05–E07; não alegar que está implementada agora.

**Arquivos:** usar a raiz `Diazverso`, planilha do canal, `Roteiros/{Longos,Shorts}`, `Thumbnails/{Longos,Shorts}` e bibliotecas Assets/Backgrounds/Memes/Músicas/Sounds quando a conexão permitir. Nomes e IDs da conta do criador não são universais.

**Shorts:** ativar `../diazverso-shorts/SKILL.md` para roteiro/plano vertical, com preset testável `../diazverso-shorts/references/preset-vertical-v1.json` (1080×1920, 30 fps e zonas seguras conservadoras). Legendas sincronizadas são o padrão, com exceção para cenas **exclusivamente de texto na tela**. Gancho rápido, payoff e CTA ao canal contextual. Preferência por pelo menos 60 s, sem tratar como limite da plataforma. **O criador posta manualmente**.

## Kit final de publicação manual — K01

A produção termina com um **pacote pronto para o criador publicar pessoalmente**, não com upload/postagem feita ou orientada pelo ChatGPT.

**Entradas:** roteiro aprovado (mesma versão do vídeo final), título escolhido, arquivos finais de vídeo e thumbnail efetivamente verificados, fontes, decisões de QA, links afiliados pertinentes já conferidos e informações editoriais. Sem vídeo renderizado/QA, entregar **rascunho de kit** marcado como pendente, não kit final aprovado.

**Saída utilizável:** título final, descrição PT-BR pronta para copiar, fontes/atribuições, links pertinentes e divulgação de afiliação quando aplicável, tags relevantes sem exageros, comentário fixado opcional e capítulos **somente com timestamps conferidos no render final**. Para K02, usar `../diazverso-drive-setup/scripts/affiliate_selection.py` apenas sobre uma leitura atual da aba `Afiliados`: selecionar somente itens `ATIVO`, pertinentes e cujo link/destino/condições foram **verificados nesta produção**; não deduzir validade da data antiga de verificação. Se nenhum passar, não inserir afiliados por obrigação. Quando houver links de afiliados, incluir divulgação transparente da relação comercial. O script não verifica destinos por conta própria nem publica vídeos. Para Shorts, adaptar linguagem e CTA ao formato sem fingir dados. Informar quais arquivos aprovados compõem o kit, com referência verificável e pendências. Não inventar links, datas, estatísticas, capítulos ou patrocínios.

**Geração executável:** com os dados aprovados, usar `scripts/build_publication_kit.py <entrada.json>` (JSON local) para obter título, descrição, fontes, tags, capítulos confirmados e afiliados verificados. O gerador aceita apenas dados fornecidos e flags de revisão; **não verifica por si mesmo a existência dos arquivos nem a veracidade das aprovações**. Validar esses insumos na execução do fluxo; nenhum upload é realizado.

**Finalização:** registrar `KIT PRONTO PARA POSTAGEM MANUAL` apenas quando roteiro, arte, render, QA e conteúdo textual realmente aprovados. Caso contrário, `KIT PARCIAL — PENDÊNCIAS`, listando somente o que falta. **Não executar nem ensinar upload, agendamento ou postagem**, nem importar a skill de postagem antiga. `PUBLICADO` é apenas registro posterior, após o criador postar manualmente e fornecer evidência de URL/data reais.

## Correção técnica antes da aprovação — J07

Quando os revisores J01–J06/I05 retornarem problemas, usar `../diazverso-decupagem/scripts/correction_loop.py` e a regra **um achado por vez**: registrar alteração concreta → rerender do trecho afetado com arquivo comprovável → executar novamente o revisor afetado sobre o novo render → fechar apenas se passar. Uma falha mantém a produção **EM REVISÃO**, não permite criar aprovação fictícia no gate J08. Sem runtime de render, registrar estado `BLOQUEADO`, sem fingir que a tarefa foi corrigida. Não atualizar a linha da produção nem postar vídeos por efeito do checklist; qualquer persistência conectada depende de autorização e validação real.

## Aprovação humana antes de entregar o kit — J08

Executar `scripts/approval_gate.py <revisao.json>` antes de declarar `KIT APROVADO PARA ENTREGA MANUAL`. O objeto da revisão contém `production_id`, os nove gates `roteiro`, `fatos_fontes`, `titulo_thumbnail`, `direitos_midias`, `video_render`, `qa_visual`, `qa_audio`, `legendas` e `kit_textual`, cada um com `status` (`APROVADO`, `PENDENTE`, `REPROVADO`) e `evidence`. Acrescentar `creator_decision: {approved: true/false, evidence: "..."}` com a decisão **real** do criador. Não marcar um gate aprovado por inferência, arquivo presente ou resposta automática; cada aprovação exige evidência. Qualquer pendência/reprovação bloqueia entrega como final. O validador não confere a autenticidade externa da evidência e não publica nem ensina a postar.

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
