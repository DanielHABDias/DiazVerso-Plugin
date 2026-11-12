# Pacote de poses do Nox (stop motion)

Na edição, o Nox gesticula em stop motion. Cada fala troca o desenho inteiro, de uma pose direto para a outra, sem quadros intermediários. Por isso ele precisa de um PNG por pose, com os braços e as mãos na posição do gesto e a expressão dos olhos já desenhada.

O kit lê as poses de `assets/brand/nox/poses/<pose>.png`. Pose que ainda não existe cai no Nox canônico com a expressão pedida, e o vídeo não quebra.

## Formato de cada arquivo

- PNG com fundo transparente, a figura **inteira** (capuz até as botas), recortada rente, com os pés na base da imagem.
- Altura de 1200 a 1600 px, no mesmo traço, proporções e cores do `Nox.png`:
  - capuz preto com ponta;
  - rosto vazio;
  - olhos amarelos luminosos;
  - sobretudo, punhos dourados e emblema;
  - luvas e botas;
  - contorno de tinta e o deslocamento vermelho/azul nas bordas.
- Sem boca, nariz, dedos a mais, armas reais, cenário ou texto.
- Nome do arquivo exatamente como na tabela.

## Poses

| Arquivo | Gesto | Olhos | Uso |
| --- | --- | --- | --- |
| `pensando.png` | Uma mão na frente do rosto, na altura de onde seria o queixo; a outra segura o cotovelo | Um olho mais fechado | Pergunta, dúvida |
| `arminha.png` | Mão em "arminha" (indicador e polegar) apontada para a câmera, a outra na cintura | Piscando um olho | Piada, "te peguei" |
| `apontando.png` | Braço esticado apontando para o lado | Determinados | Opinião, "olha isso" |
| `ombros.png` | Os dois braços abertos, palmas para cima, ombros erguidos | Tédio, meio fechados | "Fazer o quê?" |
| `joinha.png` | Polegar para cima na frente do corpo | Felizes (arcos) | Aprovação |
| `facepalm.png` | Mão cobrindo a frente do rosto, cabeça um pouco baixa | Um olho aparecendo entre os dedos | Vergonha alheia, erro |
| `bracos-cruzados.png` | Braços cruzados no peito | Bravos | Discordância |
| `acenando.png` | Uma mão erguida acenando | Felizes | Abertura, "oi" |
| `rindo.png` | Mãos na barriga, corpo inclinado para trás | Arcos bem fechados | Humor |
| `assustado.png` | Mãos para cima perto do rosto, corpo recuando | Grandes e redondos | Surpresa |
| `comemorando.png` | Os dois punhos para cima | Felizes | Vitória, acerto |
| `explicando.png` | Uma mão aberta à frente, como quem mostra algo | Neutros (forma do original) | Explicação |

## Gerar com uma ferramenta de imagem

Passe o `Nox.png` como imagem de referência. Gere **uma pose por vez**, com este pedido (troque o gesto e os olhos):

```text
Usando a imagem anexada como referência exata do personagem, desenhe o mesmo personagem (mesmo estilo de
desenho, traço, proporções, cores, capuz com ponta, rosto escuro vazio, olhos amarelos luminosos, sobretudo,
punhos dourados, emblema, luvas, botas, contorno preto e deslocamento vermelho/azul nas bordas) de corpo
inteiro, de frente, fazendo: [GESTO]. Olhos: [OLHOS]. Fundo transparente, sem cenário, sem texto, sem
sombra no chão. Não acrescente boca, nariz, armas nem acessórios.
```

Depois de gerar:

1. Recortar rente e conferir a transparência.
2. Comparar com o `Nox.png` lado a lado (Character Lock, `../SKILL.md`). Reprovar se a silhueta, as proporções, as cores ou o estilo mudarem.
3. Salvar em `assets/brand/nox/poses/<pose>.png` e registrar a origem e a licença da ferramenta no `assets/manifest.json`.
4. No Content Lab, rodar `npm run scenes:diazverso` para a pose entrar no kit.

Uma ferramenta de imagem só pode ser usada se os termos dela permitirem uso comercial do resultado, porque o canal é monetizado.
