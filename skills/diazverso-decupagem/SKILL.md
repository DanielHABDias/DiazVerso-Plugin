---
name: diazverso-decupagem
description: "Use para decupar um roteiro aprovado em beats de motion (fala, evidência da obra, cena do kit, som), escolher as mídias e revisar o vídeo renderizado: frames, áudio, ritmo, direitos e correções."
---

# Decupagem e revisão

A montagem é a composição de motion do kit (`../diazverso-motion/SKILL.md`); pelo Content Lab, é `motion_plan_auto` seguido de ajustes com `motion_plan_set`. Esta skill cuida do que vem antes e depois: decidir o que cada beat mostra e revisar o resultado.

## Decupar

1. Receber ID, formato e revisão aprovada do roteiro. Confirmar narração, mídias e direitos.
2. Quebrar o roteiro em beats de 1,5–3 s: uma frase ou meia frase por beat. Para cada um, definir:
   - a função: evidência, explicação, reação/humor ou orientação;
   - a cena do kit;
   - a mídia da obra;
   - o som.
3. Seguir a [receita do formato](references/receitas.md) e o [padrão visual](../diazverso-core/references/padrao-visual.md). Toda afirmação sobre a obra mostra a obra ([imagens e direitos](../diazverso-core/references/imagens-e-direitos.md)). Sem mídia, buscar com `../find-broll/SKILL.md` ou mudar a abordagem do beat.
4. Trilha e SFX seguem [música](references/musica.md).
5. Em diálogo didático com o Nox, definir dúvida → tentativa → consequência → explicação, sem inventar falas canônicas.

## Revisar

1. Antes do render: prévias de frames (`motion_preview` no Content Lab), conferidas beat a beat.
2. Depois do render: frames e áudio reais, com os utilitários de [QA e correções](references/qa.md). Um achado por vez; renderizar de novo e revisar o mesmo achado.
3. Vertical: `../diazverso-shorts/SKILL.md`.

## Som

Os SFX ficam em `assets/sfx/motion/` e seguem o [guia de som](../diazverso-motion/references/som.md).

## Limites

- Não simular análise visual, escuta, transcrição, render ou aprovação.
- Não publicar.
- O kit final depende da revisão real dos arquivos e da decisão do criador.
