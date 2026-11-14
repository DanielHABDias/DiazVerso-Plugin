---
name: diazverso-criacao-video
description: "Use para iniciar, coordenar ou retomar uma produção Diazverso entre ideia, roteiro, artes, edição, QA e kit de publicação manual."
---

# Coordenação de produção

Com o Content Lab conectado, a produção corre por `../diazverso-contentlab/SKILL.md`, que combina o fluxo com o criador e opera o app. Esta skill vale sem ele e para retomada, kit e métricas.

## Iniciar ou retomar

1. Aplicar o protocolo de contexto e selecionar a próxima entrega observável. Não carregar todo o pipeline.
2. Localizar produção e fontes atuais antes de criar algo: linha em Produções, Doc e artefatos vinculados. IDs TF_#### identificam ideias; VD_#### longos; SH_#### Shorts.
3. Pedir apenas a decisão editorial ausente que impeça avançar. Reutilizar respostas, revisões e links ainda válidos.
4. Conferir ferramentas e permissões necessárias. `scripts/capability_fallback.py` classifica limitações sem inventar integração, render ou persistência.
5. Executar a skill da etapa. Corrigir falhas antes de considerar a entrega concluída e avançar nas ações autorizadas.

## Escolher a etapa

| Resultado | Skill responsável |
| --- | --- |
| Pesquisa e tese | diazverso-pesquisa |
| Títulos e promessa visual | diazverso-titulos |
| Doc nativo formatado | diazverso-roteiro |
| Revisões (embalagem, fatos, estrutura, voz) e aprovação do roteiro | diazverso-revisao |
| Arte e mascote | diazverso-thumbnail e diazverso-nox |
| Montagem do vídeo em motion (beats, kit, Nox, som) | diazverso-motion |
| Decupagem em beats e QA do render | diazverso-decupagem |
| Vertical e legendas | diazverso-shorts |
| Arquivos e registros Google | diazverso-drive-setup |

Acionar apenas a responsável pela próxima ação. `../diazverso-core/SKILL.md` fornece identidade quando houver decisão criativa.

## Retomada verificável

`scripts/resume.py` oferece `checkpoint(source)` e `recover(saved, latest)`. O estado contém `production_id`, revisão inteira monotônica, `next_task`, `completed` em ordem e `source_ref`. Etapas são nomes semânticos como `facts`, `script-approval` e `visual`.

Persistir o checkpoint com hash em armazenamento autorizado. Ao retomar, reler as fontes reais e acrescentar `fresh_read=true` somente depois dessa conferência. Divergência de produção, fonte, revisão ou histórico bloqueia continuidade até reconciliação. A revisão atual prevalece; não recriar itens nem repetir etapas concluídas.

O esquema `../../schemas/estado-producao-v1.schema.json` descreve o intercâmbio de informações da produção. Sheets/Docs e arquivos vinculados são a fonte de verdade; o checkpoint ajuda a retomada, sem criar banco paralelo ou guardar credenciais.

## Kit para publicação manual

Entradas: roteiro aprovado, título escolhido, thumbnail e vídeo finais conferidos, fontes, QA, decisão real do criador e afiliados pertinentes.

A descrição segue sempre a [estrutura do canal](references/descricao.md): completa no vídeo longo e curta no Short. Usar `scripts/build_publication_kit.py <entrada.json>` para montá-la a partir dos campos (vídeo longo: abertura, resumo, capítulos, vídeos relacionados, afiliados, obras, fontes oficiais, trilha e hashtags; Short, com ID `SH_`: título A, explicação, chamada para o canal e hashtags) e compor título, tags e comentário. Capítulos só com os tempos conferidos no render. O gerador valida os dados recebidos; não autentica arquivos ou aprovações.

Para afiliados, `../diazverso-drive-setup/scripts/affiliate_selection.py` seleciona apenas registros ATIVO pertinentes, com destino e condições verificados nesta produção. O gerador acrescenta o aviso de afiliado do canal; se nenhum servir, a seção sai.

Antes de entregar como final, executar `scripts/approval_gate.py <revisao.json>`: nove gates — roteiro, fatos_fontes, titulo_thumbnail, direitos_midias, video_render, qa_visual, qa_audio, legendas, kit_textual — precisam de status e evidência, além de `creator_decision`. Um campo preenchido não prova aprovação. Pendências produzem kit parcial e próxima ação concreta.

Sem acesso ao Drive e à planilha, o kit ganha a seção **Registro manual**: arquivos para subir com a pasta de destino e as linhas prontas de Produções e Ideias ([modo manual](../diazverso-drive-setup/references/modo-manual.md)).

O criador publica pessoalmente. Não executar nem ensinar envio, upload, agendamento ou postagem. PUBLICADO é registro posterior de URL e data reais, via skill Drive.

## Corrigir e acompanhar

Usar `../diazverso-decupagem/scripts/correction_loop.py` para tratar um achado por vez: alteração → novo render → revisão do mesmo achado → fechamento se passar. Preservar evidência de arquivos e hashes; não inferir aprovação.

Depois da publicação manual, `scripts/analyze_metrics.py` resume métricas reais com fonte, período e ID. Comparações exigem contextos equivalentes. Converter achados em hipóteses a pesquisar, sem afirmar causalidade ou desempenho futuro.

Detalhes de organização: `../diazverso-drive-setup/references/estrutura.md`.
