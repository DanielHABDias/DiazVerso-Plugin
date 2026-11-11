---
name: diazverso-shorts
description: "Use para criar ou adaptar roteiro e plano audiovisual de Shorts Diazverso em 9:16, com gancho, ritmo, legendas e CTA contextual; não faz upload nem publicação."
---

**Protocolo obrigatório Diazverso:** antes de agir, aplicar `../diazverso-contexto-eficiente/SKILL.md`. Ler uma vez por sessão/versão e reutilizar o contexto válido; abrir somente a skill principal e as dependências necessárias.

# Diazverso — Shorts verticais

**Resultado:** preparar uma proposta de Short criativa e executável para a produção, sem prometer vídeo renderizado quando não houver runtime Remotion/editor. Seguir a tese, fatos, voz natural e humor contextual de `diazverso-core`. **O criador publica manualmente**; não há comandos nem instruções de postagem.

## Fluxo compacto

1. Receber uma pauta/tese ou roteiro aprovado, fonte factual, promessa de título e objetivo do Short. Se faltar somente um detalhe essencial, pedir esse detalhe; não reler o projeto inteiro.
2. Escrever **gancho imediato** com pergunta, contradição, revelação ou situação visual. O desenvolvimento precisa cumprir a promessa; não alongar por obrigação.
3. Preferir duração editorial de **pelo menos 60 s** quando o conteúdo sustentar. É preferência do criador, **não limite de plataforma**. Uma duração menor pode ser sinalizada para decisão editorial, nunca preenchida com enrolação.
4. Construir progressão curta: gancho → contexto mínimo → evidência/confronto → payoff → **CTA ao canal contextual e breve**. Não abrir com logo/longo preâmbulo nem interromper resolução da tese para CTA.
5. Planejar quadros com mudanças motivadas por informação: Nox (se relevante e fiel ao asset canônico), HQ moderna, recorte, parallax, câmera e tipografia de impacto, **sem colocar efeito em todo segundo**. Nunca inventar direito de uso de clipe/áudio.
6. Aplicar o preset `references/preset-vertical-v1.json`: **1080×1920, 30 fps, 9:16**. Manter textos e elementos essenciais dentro dos limites conservadores. Reservar a região de legendas e evitar sobreposição com título/CTA. Essas margens não são garantia sobre UI do YouTube; conferir em preview real.
7. **Legenda sincronizada com a fala por padrão:** quando existirem timestamps de palavras verificados, executar `scripts/captions.py <entrada.json> --srt-output <saida.srt>` para gerar SRT e cues por frame (short-audio). Cada entrada em `words` informa `start_ms`, `end_ms`, `text`; `visual_text_only` só pode indicar intervalos **sem fala**. O programa rejeita palavras sobrepostas e tentativas de ocultar fala em cenas tipográficas. **Gerar SRT não equivale a aferir sync real**: no render, comparar imagem, áudio e legendas; até lá, `audio_sync_verified=false`.

8. Preparar decupagem de cenas (skill `diazverso-decupagem`), narrador × efeito × mídia × duração, e pontos de preview. Confirmar a mesma versão do roteiro aprovada pelo criador antes de produzir.
9. Encerrar com kit textual/roteiro/arte de referência conforme recursos disponíveis. **Não declarar render/legendagem sincronizada, retenção prevista ou publicação se não houve teste/ação real.**

## Revisão de Short — shorts

Quando existir render e evidências, executar `scripts/review_short.py <entrada.json>` com gancho, duração, payoff, CTA, legenda, áudio, links, margens, direitos e inspeção do render. O revisor devolve `REVIEW_REQUIRED`, `EDITORIAL_REVIEW` ou `READY_FOR_CREATOR_APPROVAL` — **nunca aprovação automática**. Gancho tardio e duração abaixo de 60 s são observações editoriais, não previsão de retenção nem impedimentos da plataforma. Sem render real, marcar `render_checked=false`; sem sincronização ou escuta real, `captions=NOT_VERIFIED`/`audio_checked=false`. O criador decide a aprovação e posta manualmente.


## Critérios de aceitação do roteiro/plano de Short

- Gancho antes de explicação longa e tese cumprida; conclusão e CTA proporcionais.
- Formato 9:16 e zonas de segurança do preset respeitados no desenho planejado; na edição, verificar frames reais.
- Orientações visuais e áudio têm função narrativa e indicam fontes/direitos pendentes quando necessário.
- Legendas previstas ou exceção de cena só tipográfica claramente indicada; sincronização real fica pendente até revisão do render.
- **Postagem exclusivamente manual pelo criador.** O plugin apenas entrega materiais e registra publicação posteriormente se ela for confirmada.
