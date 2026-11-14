---
name: diazverso-thumbnail
description: "Use para criar, gerar com o kit e revisar as thumbnails A/B de um vídeo Diazverso: conceitos com ângulos diferentes, arte renderizada pelo kit de motion (obra, texto curto em Anton, Nox) e conferência no tamanho do celular."
---

# Diazverso — Direção de thumbnails (thumbnail-brief)

**Objetivo:** criar **dois conceitos visuais realmente diferentes** para uma mesma tese e promessa do vídeo, sem fabricar a imagem, o link do Drive ou alegar taxa de cliques. Fazer **thumbnail para vídeo longo ou Short apenas quando houver uso editorial da peça**; não assumir que Shorts exigem a mesma embalagem.

## Entradas mínimas

- `production_id` (`VD_####` ou `SH_####`), `format`, `thesis` (tese aprovada ou marcada preliminar), `promise` (o que o vídeo realmente entrega), `title` (título proposto), `subject` (personagem/elemento principal) e `assets` com disponibilidade e situação de direitos **verificadas**.
- Quando o roteiro ainda não estiver aprovado, produzir conceitos **PRELIMINARES**, sem alegar thumbnail final.
- Consultar `../diazverso-core/SKILL.md` para a direção HQ contemporânea/madura. Não duplicar o núcleo editorial.

## Duas propostas A/B com hipóteses editoriais distintas

1. Reduzir a tese a **uma pergunta/tensão visual** diretamente respondida no roteiro. Não acrescentar conflito, fato, resultado ou personagem inexistente apenas para gerar curiosidade.
2. **A** usa um ângulo dominante, por exemplo contradição/comparação; **B** usa outro enquadramento narrativo, por exemplo consequência/revelação. Não chamar de teste A/B apenas duas cores ou dois recortes da mesma imagem. O revisor `scripts/validate_thumbnail_brief.py` exige `angle`, `visual_metaphor` e `layout` distintos em A e B.
3. **Modelo do canal, sempre limpo:** fundo preto liso; **o rosto do personagem central grande no meio**, em arte de alta resolução; **uma ou duas palavras enormes na frente dele**, embaixo, que provocam: raiva no fã, curiosidade ou polêmica ("SÓ APANHA", "HUMILHADO"); **o Nox no canto** com a expressão da thumb (rindo, facepalm, assustado). Um ponto focal, nada além disso. Funciona reduzido no celular. Antes de criar, procurar thumbnails de vídeos sobre o mesmo tema com pelo menos 50 mil visualizações, no Brasil e fora, e anotar o padrão (enquadramento, cor, palavras); não copiar o visual de nenhuma delas.
4. Texto **curto**: uma ou duas palavras, no máximo quatro. Não repete o título; cria contraste ou completa a promessa. Usar Anton de `assets/brand/fonts/anton/` (SIL OFL) ou outra fonte licenciada.
5. **O Nox fica no canto** em toda thumb do modelo, com a expressão que conta a emoção, a partir das poses do pacote dele (o arquivo canônico é `assets/brand/nox/Nox.png`, com a identidade original). Novas poses dependem do Character Lock da character-lock e revisão da imagem gerada. Não afirmar que Nox está visualmente correto apenas porque o nome foi citado.
6. Arte HQ madura com contraste e profundidade a serviço da ideia, não painéis/balões infantis automáticos. Diretrizes de cor são hipóteses para o designer, **não validação de contraste de pixels**.
7. Cada asset indicado deve registrar direitos, evidência e fonte. Ausência de material aprovado gera `PENDENTE DE DIREITOS`, não troca silenciosa por imagem de terceiros.
8. Cada variante deve documentar `angle`, `visual_metaphor`, `layout`, `on_image_text`, `focus`, `contrast_plan`, `nox`, `assets_used`, `rationale`. Entregar dois conceitos A/B e uma recomendação editorial **sem prever CTR**.

## Gerar a imagem com o kit

A arte final não depende de ferramenta de imagem externa. O kit de motion do Content Lab renderiza a thumbnail (`thumbnails_generate`, composição `KitThumb`); o Nox aparece se o pacote dele foi importado no projeto (`character_import`). Cada conceito vira:

| Conceito | Prop do kit |
| --- | --- |
| Assunto dominante (obra com direitos) | `midia` |
| Contraste ou comparação | `midiaB` (layout VS) |
| Texto na imagem, até 4 palavras | `texto`, com a palavra-chave entre `*asteriscos*` |
| Emoção (Nox) | `pose` (nome do catálogo, ex.: `rindo`, `facepalm`) ou `humor` |
| Composição | `layout: "centro"` (o modelo do canal), `fundo: "preto"`, `lado` = canto do Nox, `tom` da palavra em cor, `focus` e `zoom` para enquadrar o rosto |

Pelo Content Lab, `thumbnails_generate` recebe as variantes A e B: `text`, `mediaId`, `layout`, `focus`, `zoom`, `pose`, `humor`, `side`, `tone`, `background` e, fora do modelo, `mediaIdB` e `badge`. As duas também ficam em `output/thumbnails/` do projeto. Ele grava as duas na embalagem e devolve as versões de 320 px em `output/previas/`. **Abrir as versões de celular** e responder: o assunto se reconhece em 1 segundo? O texto se lê? O que a imagem diz complementa o título? Ajustar e gerar de novo até passar.

## Contrato e validador offline

O JSON de conceito pode ser validado com:

```bash
python skills/diazverso-thumbnail/scripts/validate_thumbnail_brief.py <brief.json>
```

Veja `examples/thumbnail-brief.example.json`. O validador checa completude, promessas, diferenciação A/B, referências de assets e direitos declarados, e retorna estado `BRIEF_READY_FOR_HUMAN_CREATIVE_REVIEW` ou pendências. **Não gera a imagem**, não faz OCR, não comprova o direito legal, não inspeciona dimensões e não cria link do Drive. A geração e revisão do arquivo real pertencem à thumbnail-review e aos gates humanos. O revisor deve comparar o visual final com o briefing e o roteiro e confirmar legibilidade em tamanho reduzido.

## Inspeção de arquivo final — thumbnail-review

Depois de uma ferramenta de imagem realmente gerar as variantes e de os arquivos serem salvos em uma pasta local autorizada, executar `python skills/diazverso-thumbnail/scripts/review_thumbnail.py <revisao.json> --root <pasta-de-arquivos>`. O JSON referencia `production_id`, `brief_id` e variantes `A/B`, cada uma com `path`, `sha256` calculado sobre o **arquivo real**, `drive_link` (HTTPS real), `nox_used`, `reviewer` e seis `visual_checks` com status/evidência: `mobile_text_legibility`, `promise_matches_script`, `focal_point`, `contrast_readability`, `brand_identity`, `nox_character_lock`. Se Nox não aparece, marcar `NAO_APLICAVEL` somente nesse último campo; se aparece, exigir revisão `APROVADO` com evidência **após character-lock**.

O revisor confere arquivos PNG/JPEG locais pelo cabeçalho, hash SHA-256, dimensões **16:9 e pelo menos 1280×720**, sintaxe do link do Google Drive, completude da rubrica humana e referência da revisão. **Leitura de cabeçalho não garante decodificação total, validade gráfica ou conteúdo legível.** O código **não realiza OCR**, não reconhece Nox, não confirma identidade ou direitos, **não verifica por acesso conectado se o link aponta ao mesmo arquivo no Drive** e não transforma automaticamente notas fornecidas em aprovação verificada. Antes de marcar `titulo_thumbnail` como `APROVADO` em approval, abrir as imagens reais em tamanho reduzido, confirmar identidade, arte, título/roteiro, direitos e **ler de volta** o arquivo e link do Drive. Sem arquivos reais, permanecer `PENDENTE`.


**Segurança:** somente uma ferramenta de imagem realmente disponível e autorizada pode criar a arte; a produção termina no kit de postagem **manual** pelo criador. Jamais publicar, agendar ou enviar vídeos.
