# Música

O plugin não distribui trilhas. A música vem de uma fonte com licença para canal monetizado, escolhida pelo criador, e entra no catálogo da produção com evidência.

## Fontes aceitas

| Fonte | Condição |
| --- | --- |
| YouTube Audio Library | Uso no YouTube, inclusive monetizado. Conferir a coluna de atribuição de cada faixa e copiar o crédito exigido para a descrição. |
| Biblioteca assinada pelo criador (Epidemic Sound, Artlist ou equivalente) | Assinatura ativa que cubra o canal; registrar a licença ou o ID da faixa. |
| Trilha original encomendada ou composta | Contrato ou declaração de cessão. |

Não usar trilha de filmes, séries, jogos ou covers dessas trilhas; não usar faixa encontrada em vídeo de terceiros; não sintetizar "música" procedural como trilha final (os SFX procedurais continuam permitidos).

## Catálogo

Cada faixa entra em `audio/audio-plan.mjs` como `{id, path, kind:"music", durationFrames, tags, rights:"APPROVED", evidence}`. `evidence` descreve a licença verificável (por exemplo, "YouTube Audio Library, sem atribuição, baixada em AAAA-MM-DD"). Tags descrevem clima: `tensao`, `misterio`, `epico-contido`, `reflexivo`, `humor`, `acao`.

## Uso

- Uma faixa por bloco narrativo (abertura, desenvolvimento, payoff); troca de faixa coincide com mudança de bloco, nunca no meio de uma frase.
- Ducking de 18–24 dB sob a voz; sem música nos 0,3 s antes de uma revelação quando o silêncio ajuda.
- SFX com função: whoosh em troca de painel, ding em revelação de dado, boom em contradição, riser antes do payoff. No máximo 1 SFX a cada 4 s.
- Se não houver faixa aprovada, renderizar sem trilha e marcar `qa_audio` como pendente; não preencher com música improvisada.
