---
name: diazverso-thumbnail
description: "Use para transformar tese, promessa editorial e título de um vídeo Diazverso em conceitos de thumbnails horizontais A/B simples, legíveis e coerentes, antes de gerar ou revisar a imagem."
---

# Diazverso — Direção de thumbnails (G02)

**Objetivo:** criar **dois conceitos visuais realmente diferentes** para uma mesma tese e promessa do vídeo, sem fabricar a imagem, o link do Drive ou alegar taxa de cliques. Fazer **thumbnail para vídeo longo ou Short apenas quando houver uso editorial da peça**; não assumir que Shorts exigem a mesma embalagem.

## Entradas mínimas

- `production_id` (`VD_####` ou `SH_####`), `format`, `thesis` (tese aprovada ou marcada preliminar), `promise` (o que o vídeo realmente entrega), `title` (título proposto), `subject` (personagem/elemento principal) e `assets` com disponibilidade e situação de direitos **verificadas**.
- Quando o roteiro ainda não estiver aprovado, produzir conceitos **PRELIMINARES**, sem alegar thumbnail final.
- Consultar `../diazverso-core/SKILL.md` para a direção HQ contemporânea/madura. Não duplicar o núcleo editorial.

## Duas propostas A/B com hipóteses editoriais distintas

1. Reduzir a tese a **uma pergunta/tensão visual** diretamente respondida no roteiro. Não acrescentar conflito, fato, resultado ou personagem inexistente apenas para gerar curiosidade.
2. **A** usa um ângulo dominante, por exemplo contradição/comparação; **B** usa outro enquadramento narrativo, por exemplo consequência/revelação. Não chamar de teste A/B apenas duas cores ou dois recortes da mesma imagem. O revisor `scripts/validate_thumbnail_brief.py` exige `angle`, `visual_metaphor` e `layout` distintos em A e B.
3. Composição preferencial: **um assunto dominante**, um ponto focal imediato, poucas camadas, espaço negativo para texto, hierarquia visual clara. O conceito deve funcionar reduzido no celular. Não transformar referências FALL, Um Nerd, RunnyIA ou Baoyu em visual copiado.
4. Texto opcional e **curto** (preferência editorial: até 4 palavras). Texto não deve apenas repetir o título; pode criar contraste ou completar a promessa. Usar uma fonte legalmente disponível; **Anton é referência, não um binário autorizado a redistribuir**.
5. **Nox é opcional**, só quando ajudar a leitura da tese; se aparecer, usar o arquivo canônico `assets/brand/nox/Nox.png` e sua identidade original. Novas poses dependem do Character Lock da G01 e revisão da imagem gerada. Não afirmar que Nox está visualmente correto apenas porque o nome foi citado.
6. Arte HQ madura com contraste e profundidade a serviço da ideia, não painéis/balões infantis automáticos. Diretrizes de cor são hipóteses para o designer, **não validação de contraste de pixels**.
7. Cada asset indicado deve registrar direitos, evidência e fonte. Ausência de material aprovado gera `PENDENTE DE DIREITOS`, não troca silenciosa por imagem de terceiros.
8. Cada variante deve documentar `angle`, `visual_metaphor`, `layout`, `on_image_text`, `focus`, `contrast_plan`, `nox`, `assets_used`, `rationale`. Entregar dois conceitos A/B e uma recomendação editorial **sem prever CTR**.

## Contrato e validador offline

O JSON de conceito pode ser validado com:

```bash
python skills/diazverso-thumbnail/scripts/validate_thumbnail_brief.py <brief.json>
```

Veja `examples/thumbnail-brief.example.json`. O validador checa completude, promessas, diferenciação A/B, referências de assets e direitos declarados, e retorna estado `BRIEF_READY_FOR_HUMAN_CREATIVE_REVIEW` ou pendências. **Não gera a imagem**, não faz OCR, não comprova o direito legal, não inspeciona dimensões e não cria link do Drive. A geração e revisão do arquivo real pertencem à G03 e aos gates humanos. O revisor deve comparar o visual final com o briefing e o roteiro e confirmar legibilidade em tamanho reduzido.

**Segurança:** somente uma ferramenta de imagem realmente disponível e autorizada pode criar a arte; a produção termina no kit de postagem **manual** pelo criador. Jamais publicar, agendar ou enviar vídeos.
