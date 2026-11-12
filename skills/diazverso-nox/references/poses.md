# Pacote de poses do Nox (stop motion)

Na edição, o Nox gesticula em stop motion. Cada fala troca o desenho inteiro, de uma pose direto para a outra, sem quadros intermediários.

As poses são **combináveis**:

- **Corpo:** cada pose é um PNG do Nox inteiro com o gesto dos braços e o **rosto vazio, sem olhos**.
- **Rosto:** o kit desenha por cima os olhos de um dos 8 humores, na posição gravada em `poses.json`.

Assim cada pose serve para qualquer humor, e uma mesma pose pode ter variantes desenhadas que o kit sorteia, para o Nox nunca repetir o mesmo desenho.

## Onde ficam

```text
assets/brand/nox/poses/
  poses.json          # pose → arquivo, olhos, variantes
  pensando.png
  pensando-b.png      # variante da mesma pose
  ...
```

Pose que ainda não existe cai no Nox canônico com o humor pedido, e o vídeo não quebra. No Content Lab, `npm run scenes:diazverso` copia a pasta para o kit.

## Rostos (humores desenhados pelo kit)

Não desenhar olhos nos PNGs. O kit tem estes humores, combinados com qualquer pose:

- `bravo` (forma do original)
- `feliz` (arcos ^ ^)
- `surpreso` (grandes e redondos)
- `tedio` (meio fechados)
- `confuso` (um aberto, um apertado)
- `piscada`
- `determinado`
- `triste`

## Formato de cada PNG

- **Fundo:** transparente.
- **Figura:** o Nox **inteiro**, do capuz às botas, recortado rente, com os pés tocando a base da imagem.
- **Tamanho:** de 1200 a 1600 px de altura (o validador aceita de 1000 a 2000).
- **Traço:** o mesmo do `Nox.png`, com as mesmas proporções e cores:
  - capuz preto com ponta;
  - **rosto escuro e vazio, sem olhos**;
  - sobretudo, punhos dourados e emblema;
  - luvas e botas;
  - contorno de tinta e o deslocamento vermelho/azul nas bordas.
- **Proibido:**
  - boca, nariz e olhos;
  - dedos a mais;
  - armas reais;
  - cenário, texto e sombra no chão.
- **Nome:** minúsculas e hífen (`bracos-cruzados.png`). A variante leva o sufixo `-b`, `-c`… (`pensando-b.png`).

## Poses (braços e corpo)

| Pose | Gesto | Humor que combina | Uso |
| --- | --- | --- | --- |
| `parado` | Em pé, braços relaxados, de frente (versão de frente do canônico) | qualquer | Base, transição |
| `pensando` | Uma mão no queixo, na frente da parte de baixo do rosto; a outra segura o cotovelo | confuso, tedio | Pergunta, dúvida |
| `pensando-b` | Mão fechada encostada no rosto, de lado, cabeça inclinada | confuso | Variante |
| `arminha` | Mão em "arminha" (indicador e polegar) apontada para a câmera, a outra na cintura | piscada, feliz | Piada, "te peguei" |
| `apontando` | Braço esticado apontando para o lado | determinado, bravo | Opinião, "olha isso" |
| `apontando-b` | Apontando para a câmera, braço em direção ao público | determinado | Variante: "você" |
| `ombros` | Os dois braços abertos, palmas para cima, ombros erguidos | tedio | "Fazer o quê?" |
| `joinha` | Polegar para cima na frente do corpo | feliz | Aprovação |
| `facepalm` | Mão cobrindo a frente do rosto, cabeça um pouco baixa | tedio, triste | Vergonha alheia, erro |
| `bracos-cruzados` | Braços cruzados no peito | bravo, tedio | Discordância |
| `acenando` | Uma mão erguida acenando | feliz | Abertura, "oi" |
| `rindo` | Mãos na barriga, corpo inclinado para trás | feliz | Humor |
| `assustado` | Mãos para cima perto do rosto, corpo recuando | surpreso | Surpresa |
| `comemorando` | Os dois punhos para cima | feliz | Vitória, acerto |
| `explicando` | Uma mão aberta à frente, como quem mostra algo | determinado, bravo | Explicação |
| `explicando-b` | As duas mãos à frente, como quem segura uma caixa invisível | determinado | Variante |
| `maos-na-cintura` | As duas mãos na cintura, peito para frente | determinado | Confiança, "é óbvio" |
| `cochichando` | Mão do lado do rosto, como quem conta um segredo, corpo inclinado | piscada | Bastidor, fofoca |

Novas poses e variantes podem ser acrescentadas. O kit usa o que estiver em `poses.json`.

## poses.json

```json
{
  "versao": 1,
  "poses": {
    "pensando": {
      "arquivo": "pensando.png",
      "olhos": { "esquerdo": [512, 402], "direito": [700, 384], "largura": 150, "angulo": -4 },
      "cobre": "nenhum"
    },
    "pensando-b": { "arquivo": "pensando-b.png", "pose": "pensando", "olhos": { "esquerdo": [500, 410], "direito": [690, 396], "largura": 146 } },
    "facepalm": { "arquivo": "facepalm.png", "olhos": { "esquerdo": [520, 430], "direito": [705, 418], "largura": 140 }, "cobre": "direito" }
  }
}
```

- **`olhos.esquerdo` / `olhos.direito`:**
  - centro de cada olho, em pixels do PNG;
  - esquerdo e direito são **da imagem**, não do personagem;
  - medir onde os olhos ficariam no rosto vazio.
- **`largura`:**
  - largura do olho esquerdo em pixels, proporcional ao `Nox.png`;
  - no canônico, os olhos têm cerca de 80 px numa figura de 669 px, isto é, 12% da altura da figura.
- **`largura_direito`:** opcional. O padrão é 75% da largura, porque o canônico está um pouco de lado. Numa pose bem de frente, usar o mesmo valor da `largura`.
- **`angulo`:** opcional, a inclinação da cabeça em graus.
- **`cobre`:**
  - olho escondido pela mão: `nenhum`, `esquerdo`, `direito` ou `ambos`;
  - o kit não desenha esse olho, para ele não aparecer por cima da mão;
  - no facepalm, deixar um olho aparecendo entre os dedos.
- **`pose`:** só nas variantes; diz de qual pose ela é variante.
- **`olhos: null`:** para uma pose com o rosto todo escondido.

## Gerar com uma ferramenta de imagem

Passe o `Nox.png` como imagem de referência e gere **uma pose por vez**. Use este pedido, trocando o `[GESTO]`:

```text
Usando a imagem anexada como referência exata do personagem, desenhe o mesmo personagem (mesmo estilo de
desenho, traço, proporções, cores, capuz preto com ponta, sobretudo, punhos dourados, emblema, luvas, botas,
contorno preto e deslocamento vermelho/azul nas bordas) de corpo inteiro, de frente, fazendo: [GESTO].
O rosto dentro do capuz fica totalmente escuro e vazio: SEM olhos, sem boca, sem nariz. Fundo transparente,
sem cenário, sem texto, sem sombra no chão. Não acrescente armas nem acessórios.
```

Depois de gerar:

1. Recortar rente, com os pés na base, e conferir a transparência.
2. Comparar com o `Nox.png` lado a lado (Character Lock, `../SKILL.md`). Reprovar se a silhueta, as proporções, as cores ou o estilo mudarem, ou se aparecerem olhos ou boca.
3. Medir o centro dos olhos e a largura, e gravar no `poses.json`.
4. Conferir a montagem: desenhar elipses amarelas nos pontos medidos sobre o PNG e ver se caem dentro do rosto, na altura certa.
5. Registrar cada PNG no `assets/manifest.json` com:
   - `size_bytes`;
   - `git_blob_sha1` (`git hash-object <arquivo>`);
   - `source`: a ferramenta;
   - `rights`.
6. Rodar `python3 scripts/validate_plugin.py --refresh-map`.

Uma ferramenta de imagem só pode ser usada se os termos dela permitirem uso comercial do resultado, porque o canal é monetizado.
