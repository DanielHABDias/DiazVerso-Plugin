---
name: diazverso-shorts
description: "Use para criar ou adaptar Shorts Diazverso em 9:16 no mesmo padrão e nível de edição do vídeo longo: gancho, ritmo, Nox constante, legenda o tempo todo, som e CTA contextual; não faz upload nem publicação."
---

# Diazverso — Shorts verticais

**Resultado:** um Short em 9:16 com a mesma edição do vídeo longo do canal, só que vertical. O padrão é o mesmo e o nível de acabamento também: [padrão de edição](../diazverso-motion/references/padrao-de-edicao.md). Seguir a tese, os fatos, a voz e o humor de `diazverso-core`. **O criador publica manualmente.**

## Fluxo

1. Receber a pauta ou o roteiro aprovado, a fonte factual, a promessa do título e o objetivo do Short. Se faltar só um detalhe essencial, pedir esse detalhe.
2. **Gancho imediato** (pergunta, contradição, revelação ou situação visual) e desenvolvimento que cumpre a promessa, sem enrolação.
3. Duração preferida de **pelo menos 60 s** quando o conteúdo sustentar (preferência do criador, não limite da plataforma). Menos que isso é decisão editorial registrada.
4. Progressão: gancho → contexto mínimo → evidência → virada → payoff → **CTA ao canal, contextual e breve**. Sem logo nem preâmbulo na abertura.
5. Produzir pelo Content Lab (`../diazverso-contentlab/SKILL.md`) em projeto 9:16, com a receita de Short de `../diazverso-decupagem/references/receitas.md` e o padrão de edição:
   - **abertura:** a imagem mais forte em alta resolução no primeiro segundo e 3–4 cortes nos primeiros 3 s;
   - **ritmo:** troca de informação a cada 1,5–3 s, câmera sempre em movimento, cenas e fundos variando;
   - **Nox constante:** aparte ou cena `personagem` a cada 6–10 s, trocando de pose e de expressão enquanto fala;
   - **obra como base:** cena da obra sempre que a fala citar algo, cada imagem conferida aberta; um trecho com o áudio da obra quando houver fala marcante;
   - **legenda palavra a palavra o tempo todo**, pelos tempos reais do Whisper;
   - **som:** SFX em cada evento, abaixo da voz; trilha licenciada audível do começo ao fim ([som](../diazverso-motion/references/som.md));
   - **diagramação:** 1080×1920, 30 fps; conteúdo entre 12% e 72% da altura e legenda acima da interface do Shorts (preset `references/preset-vertical-v1.json`; as margens não garantem a UI do YouTube, conferir em prévia real).
6. Fora do Content Lab, a legenda sai de `scripts/captions.py <entrada.json> --srt-output <saida.srt>` com os tempos das palavras (`start_ms`, `end_ms`, `text`; `visual_text_only` só marca intervalos sem fala). Gerar SRT não é aferir sincronia: conferir no render.
7. Conferir prévias de todos os beats e o render inteiro (padrão de edição, "Conferência do render").
8. **Descrição curta:** o título A, "LINK NA BIO!", uma explicação, uma chamada para o canal e as hashtags ([descrição do Short](../diazverso-criacao-video/references/descricao.md#short)), montada por `../diazverso-criacao-video/scripts/build_publication_kit.py` com ID `SH_`. **Não declarar render, sincronia, retenção prevista ou publicação sem teste ou ação real.**

## Revisão

Com render e evidências, executar `scripts/review_short.py <entrada.json>` (gancho, duração, payoff, CTA, legenda, áudio, links, margens, direitos e inspeção do render). Ele devolve `REVIEW_REQUIRED`, `EDITORIAL_REVIEW` ou `READY_FOR_CREATOR_APPROVAL`, **nunca aprovação automática**. Sem render real, `render_checked=false`; sem escuta real, `captions=NOT_VERIFIED` e `audio_checked=false`.

## Aceitação

- Gancho antes de qualquer explicação; tese cumprida; payoff e CTA proporcionais.
- O mesmo nível do vídeo longo: abertura forte, ritmo, Nox constante, imagens conferidas, trilha audível e SFX nos níveis do canal.
- 9:16 e zonas de segurança conferidos em frames reais; legenda sincronizada conferida no render.
- **Postagem exclusivamente manual pelo criador.**
