# Música

O plugin não distribui trilhas. A música vem de uma fonte com licença para canal monetizado, escolhida pelo criador, e entra no catálogo da produção com evidência.

## Fontes aceitas

| Fonte | Condição |
| --- | --- |
| YouTube Audio Library | Uso no YouTube, inclusive monetizado. Conferir a coluna de atribuição de cada faixa e copiar o crédito exigido para a descrição. |
| Biblioteca assinada pelo criador (Epidemic Sound, Artlist ou equivalente) | Assinatura ativa que cubra o canal; registrar a licença ou o ID da faixa. |
| Trilha original encomendada ou composta | Contrato ou declaração de cessão. |
| Incompetech (Kevin MacLeod), CC BY 4.0 | Crédito na descrição: faixa, autor, incompetech.com e o link da licença. |

Não usar trilha de filmes, séries, jogos ou covers dessas trilhas; não usar faixa encontrada em vídeo de terceiros; não sintetizar "música" procedural como trilha final (os SFX procedurais continuam permitidos).

## Registro

Cada faixa entra na produção com a licença verificável: no Content Lab, `media_import_files` com `role: "music"` e os direitos confirmados; fora dele, a evidência fica na pasta da produção (por exemplo, "YouTube Audio Library, sem atribuição"). Descrever o clima da faixa: tensão, mistério, épico contido, reflexivo, humor ou ação.

## Uso

- Uma faixa pode cobrir o vídeo inteiro em trechos (`music.trechos` no Content Lab): um trecho forte da própria faixa no gancho, a troca de trecho só onde a trilha está quase muda (um trecho com o áudio da obra) e o final natural da faixa sobre a tela final. Trocar de faixa, quando houver, também só nesses pontos ou entre blocos, nunca no meio de uma frase.
- Medir a faixa antes de planejar: muitas terminam em silêncio antes do fim do arquivo. A trilha toca até o último quadro do vídeo e sai em fade de ~4 s.
- A trilha abaixa sob a voz (o kit faz isso pelos tempos das palavras), mas continua audível: cerca de 15–20 dB abaixo da voz (`music.volume` ≈ 0,8, `music.duck` ≈ 0,55). Volta nos respiros. Silêncio de até 0,3 s antes de uma revelação, quando ajudar.
- **SFX em cada troca de beat**, com função:
  - `whoosh` ou `swish` em troca de cena;
  - `pop` em texto que entra;
  - `tick` em números;
  - `impact` ou `sub` em contradição;
  - `ding` em revelação;
  - `glitch` em erro ou virada;
  - `riser` antes do payoff;
  - `camera` em evidência.

  Volume abaixo da voz, nos níveis de [som](../../diazverso-motion/references/som.md); o som não pode competir com a fala.
- Sem faixa aprovada, renderizar sem trilha e deixar o áudio pendente. Não preencher com música improvisada: a base rítmica sintetizada do kit é só rascunho.
