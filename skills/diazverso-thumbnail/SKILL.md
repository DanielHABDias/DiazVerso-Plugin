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

## Variantes por formato

Short (SH_): criar e revisar somente a variante A, vertical 9:16. Não criar B nem teste A/B. Nos passos abaixo, referências ao par A/B e sua diferenciação se aplicam somente a vídeos longos (VD_); no Short, executar os mesmos cuidados de composição, direitos e legibilidade para A. Enviar apenas A ao Content Lab e deixar THUMBNAIL B vazia na planilha.

## Duas propostas A/B para vídeos longos

1. Reduzir a tese a **uma pergunta/tensão visual** diretamente respondida no roteiro. Não acrescentar conflito, fato, resultado ou personagem inexistente apenas para gerar curiosidade.
2. **A** usa um ângulo dominante, por exemplo contradição/comparação; **B** usa outro enquadramento narrativo, por exemplo consequência/revelação. Não chamar de teste A/B apenas duas cores ou dois recortes da mesma imagem. O revisor `scripts/validate_thumbnail_brief.py` exige `angle`, `visual_metaphor` e `layout` distintos em A e B.
3. Aplicar o [modelo do canal](references/modelo-palavra.md): fundo de TV simples e escuro; palavra principal sólida brilhante atrás; personagem em PNG transparente com halo preto; contorno fino da mesma palavra na frente; palavra complementar opcional sólida e brilhante em camada frontal; Nox muito grande no canto por cima de tudo. A referência define recorte, enquadramento, camadas e ajustes aprovados. Antes de criar, procurar thumbnails de vídeos sobre o mesmo tema com pelo menos 50 mil visualizações, no Brasil e fora; conferir e anotar título, canal, visualizações e padrão visual sem copiar a composição.
4. Texto **curto e forte**: uma palavra ou uma frase de até quatro palavras que zomba, provoca ou instiga ("FRAUDE", "VIROU PILHA"), grande na imagem. Não repete o título; cria contraste ou completa a promessa, e o vídeo cumpre o que ela diz. Usar Anton de `assets/brand/fonts/anton/` (SIL OFL) ou outra fonte licenciada.
5. Usar o Nox canônico de `assets/brand/nox/Nox.png` e suas poses, com foco na cabeça e expressão; não redesenhar. Preservar posição, escala e pose aprovadas ao revisar. Pose nova exige Character Lock e revisão real.
6. Arte HQ madura com contraste e profundidade a serviço da ideia, não painéis/balões infantis automáticos. Diretrizes de cor são hipóteses para o designer, **não validação de contraste de pixels**.
7. Cada asset indicado deve registrar direitos, evidência e fonte. Ausência de material aprovado gera `PENDENTE DE DIREITOS`, não troca silenciosa por imagem de terceiros.
8. Cada variante deve documentar `angle`, `visual_metaphor`, `layout`, `on_image_text`, `focus`, `contrast_plan`, `nox`, `assets_used`, `rationale`. Entregar dois conceitos A/B e uma recomendação editorial **sem prever CTR**.

## Gerar a imagem com o kit

A composição final usa o kit; recorte ou transformação da arte pode exigir uma ferramenta de imagem autorizada. O kit de motion do Content Lab renderiza a thumbnail (`thumbnails_generate`, composição `KitThumb`); o Nox aparece se o pacote dele foi importado no projeto (`character_import`). Cada conceito vira:

| Conceito | Campo de `thumbnails_generate` |
| --- | --- |
| Modelo do canal | `layout: "palavra"` |
| Personagem da obra dentro da palavra (recorte PNG inteiro, alta resolução) | `mediaId` |
| Fundo simples escuro; arte de fundo somente quando escolhida | omitir `backgroundMediaId` no fundo simples |
| Palavra ou frase (até 2 linhas com `/`) | `text` |
| Cor da palavra (o fundo escuro contrasta sozinho) | `tone`: `vermelho`, `amarelo`, `branco`, `azul`, `verde` |
| Textura do fundo | `texture: "tv"` (padrão) |
| Emoção (Nox) e canto | `pose` (`rindo`, `facepalm`…) com `humor`, e `side` |
| Enquadramento do personagem | `focus` e `zoom` conforme a pose e a leitura no celular; pode mostrar mais corpo |
| Altura da palavra | `textY` (0,5 = meio); subir para 0,26–0,36 quando o Nox ficar no lado do começo da palavra |

Pelo Content Lab, `thumbnails_generate` recebe as variantes A e B com esses campos; fora do modelo continuam `layout: "centro"`, `background`, `mediaIdB` (VS) e `badge`. As duas também ficam em `output/thumbnails/` do projeto. Ele grava as variantes na embalagem e devolve versões de 320 px em `output/previas/`. Para sombra, palavra complementar frontal e revisão de somente uma variante, seguir a execução e a preservação definidas no [modelo](references/modelo-palavra.md). **Abrir a imagem inteira e as versões de celular** e responder: o recorte está íntegro, com halo preto, tamanho imponente e rosto reconhecível? O texto se lê, sem o Nox por cima? O contorno da frente está fino? O fundo está escuro? O que a imagem diz complementa o título? Ajustar e gerar de novo até passar.

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
