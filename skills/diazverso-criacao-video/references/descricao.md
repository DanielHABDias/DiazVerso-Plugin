# Descrição do YouTube

O vídeo longo usa a estrutura completa abaixo; o Short usa a [descrição curta](#short). Nas duas, nesta ordem. `../scripts/build_publication_kit.py` monta o texto final a partir dos campos; escrever só o conteúdo de cada campo, nunca a moldura à mão.

## Vídeo longo

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

## Campos do vídeo longo

- **Abertura:** um parágrafo que confirma a promessa do título com a tensão do vídeo (contradição, virada ou pergunta), sem entregar o payoff. Com travessão quando a frase vira: "O Carnificina dos filmes já é monstruoso — mas os quadrinhos mostram…".
- **Resumo:** um parágrafo em primeira pessoa, começando por "Neste vídeo, eu…". Cita as obras, arcos e adaptações que o vídeo percorre e termina no que o público vai entender.
- **Capítulos:** só com os tempos do render final conferido (o YouTube pede o primeiro em 00:00, pelo menos três e cada um com 10 s ou mais). No Content Lab, os tempos vêm de `chapters_get` com `timing: "palavras"` (já contam os trechos com áudio da obra); com `timing: "estimativa"`, transcrever antes. Um capítulo por bloco do roteiro, com título curto em forma de pergunta ou afirmação. O último é sempre "Continue no Diazverso", no começo da tela final. Sem o render conferido, a seção fica pendente no kit.
- **Assista também:** os mesmos dois vídeos da tela final (um ou dois vídeos publicados do canal ligados ao tema), lidos da aba Produções (coluna VÍDEO RELACIONADO da produção, ou outras linhas PUBLICADO com LINK YOUTUBE). Título como publicado, uma chamada que diz o que a pessoa ganha ao assistir, terminando em dois-pontos, e o link.
- **Links e recomendações:** os afiliados com STATUS ATIVO da aba Afiliados (`../../diazverso-drive-setup/scripts/affiliate_selection.py`). Nome em maiúsculas a partir de PRODUTO / SERVIÇO (ou CATEGORIA, quando mais claro), uma chamada curta (de OBSERVAÇÕES, quando houver) e o LINK AFILIADO. O aviso de afiliado vem logo depois, com este texto. Sem afiliado pertinente, a seção sai inteira.
- **Fontes e créditos:** as obras e arcos citados, um por linha, com o número da edição quando houver; depois as páginas oficiais (Marvel, DC, estúdio) que sustentam os fatos, no formato "Fonte — o que é:" e o link na linha seguinte; por fim, a trilha com faixas, links e canal do compositor, conforme a licença pede.
- **Hashtags:** de 4 a 7, sem acento, a partir do personagem, da obra e do tema, com `#Diazverso` por último.

As seções Sobre o Diazverso e Aviso são fixas: copiar como estão. Nada de links ou fatos que não foram conferidos nesta produção.

## Tags

As tags do YouTube pesam pouco na busca, mas ajudam a ligar o vídeo ao assunto e a pegar grafias erradas. Escrever de 15 a 30, em minúsculas, separadas por vírgula, até 500 caracteres no total (o kit confere; tag com espaço conta 2 a mais), nesta ordem:

1. **Assunto principal:** o personagem ou a obra, sozinho e com a editora ("knull", "knull marvel").
2. **Buscas do público em PT-BR:** "quem é o …", "origem do …", "… explicado", "… vs …", o título do filme ou série no Brasil.
3. **Obras e arcos citados:** nome original e nome brasileiro ("king in black", "rei de preto").
4. **Personagens secundários fortes** do vídeo e o tema amplo ("vilões da marvel", "quadrinhos marvel").
5. **Grafias erradas comuns** do assunto, quando houver ("knul").
6. **Canal:** sempre `diazverso` e `diaz verso`, por último.

Sem tags de outros canais, de assuntos que o vídeo não trata ou repetidas. No Short, de 8 a 15, na mesma ordem.

## Short

A descrição do Short é curta. O mesmo `build_publication_kit.py` a monta quando o ID é `SH_`:

```text
{título A}

LINK NA BIO!

{explicação}

{chamada para o canal}

#{Hashtag} #{Hashtag} … #Diazverso
```

- **Título A:** a réplica exata do título A do Short.
- **LINK NA BIO!:** fixo, em maiúsculas; aponta para o vídeo relacionado ligado ao Short.
- **Explicação:** uma ou duas frases sobre o que o Short conta, sem entregar o payoff.
- **Chamada para o canal:** curta, na voz do canal ("Tem muito mais disso lá no canal, vai lá!").
- **Hashtags:** de 3 a 5, sem acento, com `#Diazverso` por último.

Sem capítulos, seções, fontes ou aviso.
