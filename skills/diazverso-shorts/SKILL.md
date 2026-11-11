---
name: diazverso-shorts
description: "Use para criar ou adaptar roteiro e plano audiovisual de Shorts Diazverso em 9:16, com gancho, ritmo, legendas e CTA contextual; não faz upload nem publicação."
---

# Diazverso — Shorts verticais

**Resultado:** preparar uma proposta de Short criativa e executável para a produção, sem prometer vídeo renderizado quando não houver runtime Remotion/editor. Seguir a tese, fatos, voz natural e humor contextual de `diazverso-core`. **O criador publica manualmente**; não há comandos nem instruções de postagem.

## Fluxo compacto

1. Receber uma pauta/tese ou roteiro aprovado, fonte factual, promessa de título e objetivo do Short. Se faltar somente um detalhe essencial, pedir esse detalhe; não reler o projeto inteiro.
2. Escrever **gancho imediato** com pergunta, contradição, revelação ou situação visual. O desenvolvimento precisa cumprir a promessa; não alongar por obrigação.
3. Preferir duração editorial de **pelo menos 60 s** quando o conteúdo sustentar. É preferência do criador, **não limite de plataforma**. Uma duração menor pode ser sinalizada para decisão editorial, nunca preenchida com enrolação.
4. Construir progressão curta: gancho → contexto mínimo → evidência/confronto → payoff → **CTA ao canal contextual e breve**. Não abrir com logo/longo preâmbulo nem interromper resolução da tese para CTA.
5. Planejar quadros com mudanças motivadas por informação: Nox (se relevante e fiel ao asset canônico), HQ moderna, recorte, parallax, câmera e tipografia de impacto, **sem colocar efeito em todo segundo**. Nunca inventar direito de uso de clipe/áudio.
6. Aplicar o preset `references/preset-vertical-v1.json`: **1080×1920, 30 fps, 9:16**. Manter textos e elementos essenciais dentro dos limites conservadores. Reservar a região de legendas e evitar sobreposição com título/CTA. Essas margens não são garantia sobre UI do YouTube; conferir em preview real.
7. **Legenda sincronizada com a fala por padrão**, com blocos naturais, contraste, leitura e duração suficientes. Trechos **exclusivamente de texto na tela** podem dispensar legenda redundante; não remover legenda só porque também existe elemento gráfico. Se sincronização não puder ser aferida em vídeo/áudio real, marcar `NÃO TESTADA`.
8. Preparar decupagem de cenas (skill `diazverso-decupagem` quando disponível), narrador × efeito × mídia × duração, e pontos de preview. Confirmar a mesma versão do roteiro aprovada pelo criador antes de produzir.
9. Encerrar com kit textual/roteiro/arte de referência conforme recursos disponíveis. **Não declarar render/legendagem sincronizada, retenção prevista ou publicação se não houve teste/ação real.**

## Critérios de aceitação do roteiro/plano de Short

- Gancho antes de explicação longa e tese cumprida; conclusão e CTA proporcionais.
- Formato 9:16 e zonas de segurança do preset respeitados no desenho planejado; na edição, verificar frames reais.
- Orientações visuais e áudio têm função narrativa e indicam fontes/direitos pendentes quando necessário.
- Legendas previstas ou exceção de cena só tipográfica claramente indicada; sincronização real fica pendente até revisão do render.
- Não importar o Content Lab antigo como dependência; produzir TSX/Remotion somente em runtime independente quando disponível.
- **Postagem exclusivamente manual pelo criador.** O plugin apenas entrega materiais e registra publicação posteriormente se ela for confirmada.
