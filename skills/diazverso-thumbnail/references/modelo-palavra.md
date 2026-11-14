# Modelo "palavra": o personagem dentro da palavra brilhando

Consultar ao montar a thumbnail do canal. Os exemplos aprovados pelo criador estão em `../examples/`:

- `palavra-a-knull-fraude.jpg`: "FRAUDE" em vermelho, Nox rindo à direita. Título A: "O KNULL é o vilão MAIS SUPERESTIMADO da Marvel".
- `palavra-b-knull-virou-pilha.jpg`: "VIROU PILHA" em amarelo, mais alta, Nox com a mão na cara à esquerda. Título B: "KNULL, o deus que PERDEU pros PRÓPRIOS FILHOS KKKKKKKKK".

## Camadas, de trás para a frente

1. **Fundo escuro.** A arte original do personagem escurecida e borrada, ou quase preto com um leve tom da cor da palavra. Por cima, o efeito de TV (linhas de varredura e faixas RGB sutis) e uma vinheta. Sem halftone e sem fundo colorido claro.
2. **A palavra cheia, brilhando.** Anton, alongada na vertical, ocupando quase toda a largura, na cor do tom com brilho forte.
3. **O personagem da obra.** Recorte PNG, da cabeça até a cintura, centralizado, com sombra escura em volta. Ele cobre parte das letras.
4. **A palavra só com o contorno.** A mesma palavra, no mesmo lugar, transparente e com um contorno branco fino. As letras reaparecem por cima do personagem.
5. **O Nox.** Grande, num canto inferior, cortado na cintura, virado para o centro, com a expressão da thumb.

## A arte do personagem

- **Imponente e sombria.** Para vilão, uma arte oficial em que ele domina o quadro (pose de ataque, expressão ameaçadora), nada de painel pequeno ou cena confusa.
- **Alta resolução e inteira.** A arte original com pelo menos 1800 px de altura. Capas sem texto ("virgin variant", "textless") são as melhores: só o personagem e fundo simples. A galeria da wiki da obra lista o tamanho de cada imagem pela API (`generator=images` + `prop=imageinfo&iiprop=url|size`); escolher pelas maiores e abrir antes. Para baixar quando o site recusa download por script, seguir [baixar mídia](../../diazverso-contentlab/references/baixar-midia.md).
- **Recorte com o BiRefNet.** No venv isolado do rembg: `rembg i -m birefnet-general arte.png recorte-<personagem>-alta.png` (o modelo tem cerca de 1 GB e baixa no primeiro uso). Ele preserva cabelo, garras e armas melhor que o `isnet-general-use`.
- **Conferir o recorte sobre verde** antes de importar: nada faltando (cabelo, mãos, armas), nada de fundo sobrando. Recorte com buracos ou partes cortadas não entra, mesmo que já esteja no projeto.
- **Importar os dois arquivos** com `media_import_files` (`role: "content"`): o recorte (`mediaId`) e a arte original (`backgroundMediaId`).

## Palavra e cor

- Uma palavra ou frase de até quatro palavras que zomba, provoca ou instiga, com outro ângulo em A e em B. Ela complementa o título e o vídeo cumpre o que ela diz ("VIROU PILHA" paga no trecho da Hela).
- O tom da palavra contrasta com o fundo escuro e com o personagem: vermelho ou amarelo para vilões escuros; branco quando o personagem já é muito colorido.

## Exemplo de chamada

```json
{
  "label": "B", "layout": "palavra", "text": "VIROU PILHA",
  "mediaId": "<recorte PNG>", "backgroundMediaId": "<arte original>",
  "tone": "amarelo", "texture": "tv",
  "pose": "facepalm", "humor": "triste", "side": "esquerda",
  "focus": "50% 0%", "zoom": 1.6, "textY": 0.26
}
```

## Conferência

Abrir a imagem inteira e a versão de celular (`output/previas/`):

- o personagem está inteiro e imponente, e o rosto aparece;
- a palavra se lê no celular, e o Nox não tampa nenhuma letra (se tampar, subir `textY`);
- o contorno da frente está fino e alinhado com a palavra de trás;
- o fundo está escuro e o Nox salta como o ponto de cor e humor.
