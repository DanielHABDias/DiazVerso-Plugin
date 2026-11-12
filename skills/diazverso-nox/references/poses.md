# Pacote de poses do Nox (stop motion)

Na edição, o Nox gesticula em stop motion. Cada fala troca o desenho inteiro, de uma pose direto para a outra, sem quadros intermediários. Cada pose é um PNG pronto do Nox, com o gesto dos braços e a expressão dos olhos já desenhados.

## Onde ficam e como o kit escolhe

```text
assets/brand/nox/poses/
  pensando.png
  pensando-2.png      # variante da mesma pose
  pensando-3.png
  arminha.png
  ...
```

- O nome do arquivo é o nome da pose. O plano do Content Lab pede a pose pelo tom da frase, e o kit usa o PNG com esse nome.
- **Variantes:** `-2`, `-3`… (ou `-b`, `-c`…) no fim do nome são variantes da mesma pose. O kit sorteia uma a cada fala, para o Nox não repetir o mesmo desenho. Quanto mais variantes, mais vivo fica.
- **Pose que não existe:** cai no Nox canônico com o humor pedido, e o vídeo não quebra.
- No Content Lab, `npm run scenes:diazverso` copia a pasta para o kit.

## Formato de cada PNG

- **Fundo:** transparente.
- **Figura:** o Nox **inteiro**, do capuz às botas, recortado rente, com os pés tocando a base da imagem. Ele entra subindo pela borda de baixo com o corpo inteiro.
- **Tamanho:** de 1200 a 1600 px de altura (o validador aceita de 600 a 2400).
- **Traço:** o mesmo do `Nox.png`, com as mesmas proporções e cores:
  - capuz preto com ponta;
  - rosto escuro, só com os olhos amarelos neon brilhantes na expressão da pose, com halo dourado dentro do capuz;
  - sobretudo, punhos dourados e emblema;
  - luvas e botas;
  - contorno de tinta e o deslocamento vermelho/azul nas bordas.
- **Proibido:**
  - boca e nariz;
  - dedos a mais;
  - armas reais;
  - cenário, texto e sombra no chão.
- **Nome:** minúsculas e hífen, exatamente como na tabela (`bracos-cruzados.png`).

## Poses que o plano usa

| Arquivo | Gesto | Olhos | Quando o plano usa |
| --- | --- | --- | --- |
| `pensando` | Mão no queixo, na frente da parte de baixo do rosto; a outra segura o cotovelo | Um mais fechado, desconfiado | Pergunta, dúvida |
| `ombros` | Os dois braços abertos, palmas para cima, ombros erguidos | Tédio, meio fechados | Pergunta, "fazer o quê?" |
| `apontando` | Braço esticado apontando para o lado ou para a câmera | Determinados | Opinião, "olha isso" |
| `arminha` | Mão em "arminha" apontada para a câmera, a outra na cintura | Piscando | Opinião com piada, "te peguei" |
| `maos-na-cintura` | As duas mãos na cintura, peito para frente | Determinados | Opinião confiante, "é óbvio" |
| `facepalm` | Mão cobrindo a frente do rosto, cabeça baixa, um olho entre os dedos | Tédio ou triste | Erro, vergonha alheia |
| `rindo` | Mãos na barriga, corpo inclinado para trás | Apertados em `> <` | Erro engraçado, humor |
| `assustado` | Mãos para cima perto do rosto, corpo recuando | Grandes e redondos | Surpresa |
| `explicando` | Uma ou as duas mãos abertas à frente, como quem mostra algo | Neutros (forma do original) | Explicação |
| `joinha` | Polegar para cima na frente do corpo | Piscada feliz | Aprovação |
| `cochichando` | Mão do lado do rosto, como quem conta segredo, corpo inclinado | Piscando | Bastidor, curiosidade |
| `bracos-cruzados` | Braços cruzados no peito | Estreitos e assimétricos, céticos | Discordância |
| `acenando` | Uma mão erguida acenando | Felizes | Abertura, "oi" |
| `comemorando` | Os dois punhos para cima | Felizes | Vitória, acerto |
| `parado` | Em pé, braços relaxados | Neutros e arredondados | Base |

Uma pose fora da tabela pode ficar na pasta para uso manual no `motion_plan_set` (`pose: "<nome>"`), mas o plano automático só pede as da tabela.

## Variantes e poses adicionais disponíveis

Todos estes PNGs incluem a expressão dos olhos amarelos neon. Variantes com `-b` pertencem à pose base e podem ser sorteadas pelo kit. As outras opções servem à escolha manual pelo nome no `motion_plan_set`.

| Arquivo | Gesto | Olhos | Uso |
| --- | --- | --- | --- |
| `pensando-b` | Mão fechada junto ao rosto, cabeça inclinada | Semicerrados, contemplativos | Variante de dúvida mais desconfiada |
| `apontando-b` | Indicador em direção ao público | Arco e meia-lua cúmplices | Variante para falar diretamente com quem assiste |
| `explicando-b` | Duas mãos delimitando uma caixa invisível | Ovais atentos | Variante para tamanho e comparação |
| `explicando-centro` | Mãos abertas ao centro, em alturas diferentes | Ovais amigáveis | Explicação paciente, gesto contido |
| `mao-na-cabeca` | Uma mão apoiada no capuz | Fendas baixas, constrangidas | Esquecimento, situação sem graça |
| `high-five` | Palma aberta para o público, outra mão na cintura | Arcos felizes | Convite à comemoração |
| `calma` | Palma à frente do peito, cotovelo baixo | Curvas serenas, fechadas | Pedir calma ou introduzir ressalva |
| `triste` | Mãos unidas baixas, ombros caídos | Meias-luas descendentes | Decepção, consequência emocional |
| `ideia` | Indicador erguido junto à cabeça | Abertos e assimétricos | Descoberta, conclusão |

## Gerar com uma ferramenta de imagem

Passe o `Nox.png` como imagem de referência e gere **uma pose por vez**. Use este pedido, trocando o `[GESTO]` e os `[OLHOS]`:

```text
Usando a imagem anexada como referência exata do personagem, desenhe o mesmo personagem (mesmo estilo de
desenho, traço, proporções, cores, capuz preto com ponta, rosto escuro vazio, olhos amarelos luminosos,
sobretudo, punhos dourados, emblema, luvas, botas, contorno preto e deslocamento vermelho/azul nas bordas)
de corpo inteiro, de frente, fazendo: [GESTO]. Olhos: [OLHOS]. Fundo transparente, sem cenário, sem
texto, sem sombra no chão. Não acrescente boca, nariz, armas nem acessórios.
```

Depois de gerar:

1. Recortar rente, com os pés na base, e conferir a transparência.
2. Comparar com o `Nox.png` lado a lado (Character Lock, `../SKILL.md`). Reprovar se a silhueta, as proporções, as cores ou o estilo mudarem, ou se aparecer boca.
3. Salvar em `assets/brand/nox/poses/<pose>.png` (ou `<pose>-2.png` para variante).
4. Registrar cada PNG no `assets/manifest.json` com:
   - `size_bytes`;
   - `git_blob_sha1` (`git hash-object <arquivo>`);
   - `source`: a ferramenta;
   - `rights`.
5. Rodar `python3 scripts/validate_plugin.py --refresh-map`.

Uma ferramenta de imagem só pode ser usada se os termos dela permitirem uso comercial do resultado, porque o canal é monetizado.

## Avançado: pose sem olhos combinada com o humor

Um PNG desenhado **sem olhos** pode ser combinado com os 8 humores do kit:

- bravo
- feliz
- surpreso
- tedio
- confuso
- piscada
- determinado
- triste

Para isso, a pose precisa de uma entrada no `poses.json` da pasta:

```json
{ "versao": 1, "poses": { "pensando-x": { "arquivo": "pensando-x.png", "pose": "pensando", "olhos": { "esquerdo": [512, 402], "direito": [700, 384], "largura": 150, "angulo": -4 }, "cobre": "nenhum" } } }
```

- **`olhos.esquerdo` / `olhos.direito`:** centro de cada olho em pixels do PNG, esquerdo e direito da imagem.
- **`largura`:** largura do olho esquerdo, cerca de 12% da altura da figura.
- **`largura_direito`:** opcional. O padrão é 75% da `largura`.
- **`angulo`:** opcional, a inclinação da cabeça em graus.
- **`cobre`:** o olho escondido pela mão (`nenhum`, `esquerdo`, `direito`, `ambos`).

PNGs soltos, com os olhos já desenhados, não precisam de `poses.json`.
