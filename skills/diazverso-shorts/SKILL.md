---
name: diazverso-shorts
description: "Use para criar Shorts Diazverso em 9:16: por padrão, cortes do vídeo longo que funcionam sozinhos, com a mesma edição e a chamada para o vídeo completo; ou, a pedido, um Short do zero. Não faz upload nem publicação."
---

# Diazverso — Shorts verticais

**Resultado:** um Short em 9:16 com a mesma edição do vídeo longo do canal, só que vertical. O padrão é o mesmo e o nível de acabamento também: [padrão de edição](../diazverso-motion/references/padrao-de-edicao.md). Seguir a tese, os fatos, a voz e o humor de `diazverso-core`. **O criador publica manualmente.**

## Origem do Short

- **Corte do vídeo longo (padrão).** Depois que o vídeo longo está renderizado, os Shorts saem dele: trechos que funcionam sozinhos, adaptados para 9:16, com a mesma narração do criador e o mesmo nível de edição. Não se cria tema novo para Short sem pedido.
- **Short do zero (só a pedido do criador).** Pauta própria, roteiro na [estrutura do Short](../diazverso-roteiro/references/escrita.md) ("Estrutura do Short") e narração própria, seguindo toda a ordem da produção.

## Corte do vídeo longo

1. Ler a transcrição do longo (`narration_transcript`) e escolher **2 a 4 trechos** que se sustentam sem o resto do vídeo: um gancho próprio (revelação, contradição ou pergunta), uma história ou prova completa e um payoff que responde o gancho. Trecho que depende de algo dito antes fica de fora ou ganha a frase de contexto de outro ponto do longo.
2. Montar cada Short com intervalos reais da narração do longo (início e fim pelos tempos do Whisper, cortando em pausas, nunca no meio de palavra). Pode reordenar: a frase mais forte abre o Short a frio, mesmo que no longo ela venha depois. Registrar no brief do projeto os intervalos usados (`2:45–2:53`, `1:27–2:43`…).
3. Mesmos títulos e thumbnail próprios do Short (título A/B, thumbnail vertical no modelo do canal); a tese é a do trecho, sem prometer o que ele não entrega.
4. Projeto 9:16 no Content Lab com a narração cortada, as mesmas mídias do longo e a transcrição refeita sobre o áudio do Short. O plano de motion é refeito para vertical, no mesmo nível do longo (abaixo), não um recorte da tela 16:9.
5. **Fecho com o vídeo completo:** o Short termina na chamada para o canal, com a thumbnail do vídeo longo na tela. A fala é a gravação-padrão do criador ("vai lá no canal…"), importada como mídia do projeto; enquanto ela não existir, usar a frase de CTA da própria narração do longo e avisar o criador que falta gravar a chamada-padrão.

## Edição (os dois casos)

1. Produzir pelo Content Lab (`../diazverso-contentlab/SKILL.md`) em projeto 9:16, com a receita de Short de `../diazverso-decupagem/references/receitas.md` e o padrão de edição:
   - **abertura:** a imagem mais forte em alta resolução no primeiro segundo e 3–4 cortes nos primeiros 3 s; gancho antes de qualquer explicação, sem logo nem preâmbulo;
   - **ritmo:** troca de informação a cada 1,5–3 s, câmera sempre em movimento, cenas e fundos variando;
   - **Nox constante:** aparte ou cena `personagem` a cada 6–10 s, trocando de pose e de expressão enquanto fala;
   - **obra como base:** cena da obra sempre que a fala citar algo, cada imagem conferida aberta; um trecho com o áudio da obra quando houver fala marcante;
   - **legenda palavra a palavra o tempo todo**, pelos tempos reais do Whisper;
   - **som:** SFX em cada evento, abaixo da voz; trilha licenciada audível do começo ao fim ([som](../diazverso-motion/references/som.md));
   - **diagramação:** 1080×1920, 30 fps; conteúdo entre 12% e 72% da altura e legenda acima da interface do Shorts (preset `references/preset-vertical-v1.json`; as margens não garantem a UI do YouTube, conferir em prévia real).
2. Duração preferida de **pelo menos 60 s** quando o conteúdo sustentar (preferência do criador, não limite da plataforma). Menos que isso é decisão editorial registrada.
3. Fora do Content Lab, a legenda sai de `scripts/captions.py <entrada.json> --srt-output <saida.srt>` com os tempos das palavras (`start_ms`, `end_ms`, `text`; `visual_text_only` só marca intervalos sem fala). Gerar SRT não é aferir sincronia: conferir no render.
4. Conferir prévias de todos os beats e o render inteiro (padrão de edição, "Conferência do render").
5. **Descrição curta:** o título A, "LINK NA BIO!", uma explicação, uma chamada para o canal e as hashtags ([descrição do Short](../diazverso-criacao-video/references/descricao.md#short)), montada por `../diazverso-criacao-video/scripts/build_publication_kit.py` com ID `SH_`. No corte, o link na bio é o vídeo longo de origem. **Não declarar render, sincronia, retenção prevista ou publicação sem teste ou ação real.**

## Revisão

Com render e evidências, executar `scripts/review_short.py <entrada.json>` (gancho, duração, payoff, CTA, legenda, áudio, links, margens, direitos e inspeção do render). Ele devolve `REVIEW_REQUIRED`, `EDITORIAL_REVIEW` ou `READY_FOR_CREATOR_APPROVAL`, **nunca aprovação automática**. Sem render real, `render_checked=false`; sem escuta real, `captions=NOT_VERIFIED` e `audio_checked=false`.

## Aceitação

- Gancho antes de qualquer explicação; tese cumprida; payoff e CTA proporcionais.
- No corte: o trecho se entende sem o vídeo longo e fecha na chamada com a thumbnail do vídeo completo.
- O mesmo nível do vídeo longo: abertura forte, ritmo, Nox constante, imagens conferidas, trilha audível e SFX nos níveis do canal.
- 9:16 e zonas de segurança conferidos em frames reais; legenda sincronizada conferida no render.
- **Postagem exclusivamente manual pelo criador.**
