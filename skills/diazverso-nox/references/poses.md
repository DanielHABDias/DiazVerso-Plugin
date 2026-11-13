# Pacote de poses do Nox (stop motion)

Na edição, o Nox gesticula em stop motion. Enquanto ele fala, o desenho inteiro troca a cada 0,7–1 s, de uma pose direto para a outra, sem quadros intermediários. Cada pose é um PNG pronto do Nox, com o gesto dos braços e a expressão dos olhos já desenhados.

## Onde ficam e como o kit escolhe

```text
assets/brand/nox/poses/
  pensando.png
  pensando-b.png      # variante da mesma pose
  arminha.png
  ...
```

- O nome do arquivo é o nome da pose. O plano do Content Lab pede a pose pelo tom da frase, e o kit usa o PNG listado no catálogo.
- **Variantes:** `-b`, `-c`… (ou `-2`, `-3`…) no fim do nome são variantes da mesma pose. O kit sorteia uma a cada fala, para o Nox não repetir o mesmo desenho. Quanto mais variantes, mais vivo fica.
- **No Content Lab:** o pacote (`assets/brand/nox/`, com o catálogo em `assets/brand/nox/poses/catalogo.json`) entra em cada projeto por `character_import`. O Content Lab não guarda o Nox; depois de mudar uma pose aqui, importar o pacote de novo no projeto.
- **A expressão é do desenho:** o kit não redesenha olhos; o humor só escolhe a pose pelo tom. Pose sem PNG não aparece.

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

## Catálogo: todas as poses disponíveis

A fonte é o [`catalogo.json`](../../../assets/brand/nox/poses/catalogo.json): cada pose com os arquivos, o gesto, os olhos e os tons em que entra. O plano automático do Content Lab lê o catálogo, e o agente consulta o mesmo arquivo ao ajustar o plano.

| Pose | Arquivos | Gesto | Olhos | Tons |
| --- | --- | --- | --- | --- |
| `acenando` | `acenando` | Uma mão erguida acenando | Arcos felizes | abertura |
| `apontando` | `apontando-b`, `apontando` | Braço esticado apontando para o lado; variante -b aponta para quem assiste | Determinados; na -b, cúmplices | opiniao, enfase |
| `arminha` | `arminha` | Mão em arminha para a câmera, a outra na cintura | Piscando | piada, opiniao |
| `assustado` | `assustado` | Mãos para cima perto do rosto, corpo recuando | Grandes e redondos | surpresa |
| `bracos-cruzados` | `bracos-cruzados` | Braços cruzados no peito | Estreitos, céticos | discordancia |
| `calma` | `calma` | Palma à frente do peito, cotovelo baixo | Curvas serenas, fechadas | ressalva |
| `cochichando` | `cochichando` | Mão do lado do rosto, como quem conta segredo | Um aberto, outro piscando | bastidor |
| `comemorando` | `comemorando` | Os dois punhos para cima | Arcos felizes | vitoria |
| `explicando` | `explicando-b`, `explicando` | Mão aberta à frente, mostrando algo; variante -b delimita uma caixa invisível | Determinados; na -b, ovais atentos | explicacao |
| `explicando-centro` | `explicando-centro` | Mãos abertas ao centro, em alturas diferentes | Ovais amigáveis | explicacao |
| `facepalm` | `facepalm` | Mão cobrindo o rosto, cabeça baixa | Um olho entre os dedos | erro |
| `high-five` | `high-five` | Palma aberta para o público, a outra mão na cintura | Arcos felizes | vitoria, aprovacao |
| `ideia` | `ideia` | Indicador erguido junto à cabeça | Abertos, de descoberta | descoberta |
| `joinha` | `joinha` | Polegar para cima na frente do corpo | Piscada feliz | aprovacao |
| `mao-na-cabeca` | `mao-na-cabeca` | Uma mão apoiada no capuz | Fendas baixas, sem graça | erro, ressalva |
| `maos-na-cintura` | `maos-na-cintura` | As duas mãos na cintura, peito para frente | Determinados | opiniao, enfase |
| `ombros` | `ombros` | Braços abertos, palmas para cima, ombros erguidos | Meio fechados, de tédio | pergunta, discordancia |
| `parado` | `parado` | Em pé, braços relaxados | Neutros e arredondados | base, explicacao |
| `pensando` | `pensando-b`, `pensando` | Mão no queixo; variante -b com a mão fechada junto ao rosto | Um mais fechado, desconfiado | pergunta |
| `rindo` | `rindo` | Mãos na barriga, corpo inclinado para trás | Apertados em > < | piada |
| `triste` | `triste` | Mãos unidas baixas, ombros caídos | Meias-luas descendentes | tristeza |

Tons:

- `abertura`: primeira aparição, "oi"
- `base`: neutro, transição
- `explicacao`: explica um fato ou mostra algo
- `enfase`: "olha isso", destaque
- `opiniao`: opinião do canal
- `piada`: ironia, piada, "te peguei"
- `pergunta`: pergunta, dúvida
- `surpresa`: revelação, "sério?"
- `discordancia`: discorda, critica
- `ressalva`: "mas calma", contraponto
- `bastidor`: curiosidade, bastidor, segredo
- `erro`: erro, decisão ruim, vergonha alheia
- `tristeza`: perda, morte, decepção
- `descoberta`: conclusão, "aí que está"
- `aprovacao`: acerto, elogio
- `vitoria`: vitória, sucesso

## Como usar no vídeo (obrigatório)

1. **O Nox troca de pose enquanto fala.** Num aparte ou na cena `personagem`, a pose muda de uma vez a cada 0,7–1 s de fala: um aparte de 3 s tem 3 ou 4 poses. Cada troca é seca, sem quadros intermediários.
2. **A pose segue o tom da frase.** A primeira pose do aparte é a do tom (pergunta → `pensando` ou `ombros`; piada → `rindo` ou `arminha`). As seguintes continuam no mesmo tom ou passam por `explicando`, `explicando-centro` e `parado`.
3. **Todas as poses aparecem no vídeo.** O plano prefere, dentro do tom, a pose que ainda não apareceu. No fim, toda pose do catálogo precisa ter aparecido pelo menos uma vez num vídeo longo; o Content Lab avisa quais faltaram, e o agente as encaixa em apartes de tom compatível pelo `motion_plan_set`.
4. **Sem repetir em seguida.** A mesma pose não aparece duas vezes seguidas, e as variantes `-b` são sorteadas.
5. **Nova pose:** o PNG entra na pasta, no `assets/manifest.json` e no `catalogo.json` com gesto, olhos e tons. O validador recusa PNG fora do catálogo.

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
3. Salvar em `assets/brand/nox/poses/<pose>.png` (ou `<pose>-b.png` para variante) e no `catalogo.json`.
4. Registrar cada PNG no `assets/manifest.json` com:
   - `size_bytes`;
   - `git_blob_sha1` (`git hash-object <arquivo>`);
   - `source`: a ferramenta;
   - `rights`.
5. Rodar `python3 scripts/validate_plugin.py`.

Uma ferramenta de imagem só pode ser usada se os termos dela permitirem uso comercial do resultado, porque o canal é monetizado.
