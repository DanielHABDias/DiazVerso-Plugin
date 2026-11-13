# Descrição do YouTube

A descrição do Diazverso segue sempre esta estrutura, nesta ordem. `../scripts/build_publication_kit.py` monta o texto final a partir dos campos; escrever só o conteúdo de cada campo, nunca a moldura à mão.

## Estrutura

```text
{abertura}

{resumo}

────────────────────
CAPÍTULOS
────────────────────

00:00 {capítulo}
…
{mm:ss} Continue no Diazverso

────────────────────
ASSISTA TAMBÉM
────────────────────

{título do vídeo}
{chamada}:
{link}

────────────────────
LINKS E RECOMENDAÇÕES
────────────────────

{NOME EM MAIÚSCULAS}
{chamada}:
{link de afiliado}
…

Os links de compra acima podem ser de afiliado. Se você comprar por eles, o Diazverso pode receber uma comissão, sem custo adicional para você, e isso ajuda o canal.

────────────────────
SOBRE O DIAZVERSO
────────────────────

No Diazverso, o universo geek ganha histórias, análises, explicações e opiniões.

Marvel, DC, super-heróis, filmes, séries, animações, games e tudo que faz parte desse universo.

Inscreva-se no Diazverso:
https://www.youtube.com/@DiazVerso?sub_confirmation=1

Instagram:
https://www.instagram.com/diazversoyt/

────────────────────
FONTES E CRÉDITOS
────────────────────

Obras e arcos abordados:
{obra}
…

{Fonte} — {o que é}:
{link oficial}
…

Músicas: “{faixa}” e “{faixa}”, de {compositor}.
{faixa}: {link}
Canal do compositor: {link}

────────────────────
AVISO
────────────────────

Trechos e materiais de terceiros podem ser utilizados em contextos de comentário, crítica, análise, informação e entretenimento. Os direitos sobre esses materiais pertencem aos seus respectivos titulares.

────────────────────

#{Hashtag} #{Hashtag} … #Diazverso
```

## O que escrever em cada campo

- **Abertura:** um parágrafo que confirma a promessa do título com a tensão do vídeo (contradição, virada ou pergunta), sem entregar o payoff. Com travessão quando a frase vira: "O Carnificina dos filmes já é monstruoso — mas os quadrinhos mostram…".
- **Resumo:** um parágrafo em primeira pessoa, começando por "Neste vídeo, eu…". Cita as obras, arcos e adaptações que o vídeo percorre e termina no que o público vai entender.
- **Capítulos:** só com os tempos do render final conferido (o YouTube pede o primeiro em 00:00, pelo menos três e cada um com 10 s ou mais). Um capítulo por bloco do roteiro, com título curto em forma de pergunta ou afirmação. O último é sempre "Continue no Diazverso". Sem o render conferido, a seção fica pendente no kit.
- **Assista também:** um ou dois vídeos publicados do canal ligados ao tema, lidos da aba Produções (coluna VÍDEO RELACIONADO da produção, ou outras linhas PUBLICADO com LINK YOUTUBE). Título como publicado, uma chamada que diz o que a pessoa ganha ao assistir, terminando em dois-pontos, e o link.
- **Links e recomendações:** os afiliados com STATUS ATIVO da aba Afiliados (`../../diazverso-drive-setup/scripts/affiliate_selection.py`). Nome em maiúsculas a partir de PRODUTO / SERVIÇO (ou CATEGORIA, quando mais claro), uma chamada curta (de OBSERVAÇÕES, quando houver) e o LINK AFILIADO. O aviso de afiliado vem logo depois, com este texto. Sem afiliado pertinente, a seção sai inteira.
- **Fontes e créditos:** as obras e arcos citados, um por linha, com o número da edição quando houver; depois as páginas oficiais (Marvel, DC, estúdio) que sustentam os fatos, no formato "Fonte — o que é:" e o link na linha seguinte; por fim, a trilha com faixas, links e canal do compositor, conforme a licença pede.
- **Hashtags:** de 4 a 7, sem acento, a partir do personagem, da obra e do tema, com `#Diazverso` por último.

As seções Sobre o Diazverso e Aviso são fixas: copiar como estão. Nada de links ou fatos que não foram conferidos nesta produção.
