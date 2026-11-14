# Padrão de edição do Diazverso

O nível que o canal exige em todo vídeo, longo (16:9) ou Short (9:16). Os números são a medida de um vídeo pronto: usar como alvo na decupagem e como conferência no render. Cenas, props e sons valem pelo `motion_kit` do Content Lab.

## Abertura (primeiros 5 s e primeiros 30 s)

- **Primeira imagem:** a arte mais bonita do personagem central, em alta resolução (lado maior com pelo menos ~1500 px), em tela cheia, com foco no rosto e zoom. Nunca miniatura de wiki ou imagem pequena ampliada.
- **Primeiros 5 s:** 5–6 cortes. Cada palavra forte do gancho troca a imagem: rosto do personagem → close → palavra gigante (`titulo`) → dois planos da obra. Flash e som em cada corte.
- **Primeiros 30 s:** cerca de 15 trocas. Lista de fatos do gancho em cortes secos, um som diferente para cada item, e o placar (caixinha `livre` no canto superior direito) atualizando a cada item.
- Legenda palavra a palavra em todo o gancho.

## Ritmo e variedade (vídeo inteiro)

- Média de 2,5–2,7 s por troca; nenhum beat parado acima de 6 s, salvo os trechos com o áudio da obra.
- A cena da obra é metade dos beats (`evidencia`, quase sempre em tela cheia ou em painel). O resto alterna `titulo`, `frase`, `personagem`, `aparte`, `lista`, `formula`, `comparacao`, `pagina`, `ficha`, `numero` e no máximo uma `paineis3d` a cada ~30 s.
- **O Nox aparece a cada 10–20 s** (aparte ou cena `personagem`), sempre trocando de pose enquanto fala e com balão de ícone ou texto. Todas as poses do catálogo aparecem ao longo do vídeo.
- Placar recorrente quando o roteiro conta vitórias ou derrotas ("KNULL 0 × 1 THOR"), na mesma caixinha e no mesmo canto.
- Rótulo amarelo só quando a imagem mostra exatamente o que ele diz (edição, obra, personagem).

## Imagens

- **Abrir cada imagem antes de usar.** O nome do arquivo pode estar errado: a imagem precisa mostrar o que a fala e o rótulo dizem. Imagem que não confere sai do beat; sem imagem certa, a fala vira `frase` ou `titulo`.
- **Resolução:** em tela cheia, lado maior com pelo menos ~1000 px; abaixo disso, só em painel pequeno. Trocar miniaturas por arte grande da mesma obra.
- **Capas e pôsteres verticais** entram em painel em pé (o kit faz isso sozinho em `evidencia` sem `cheia`), com o rosto inteiro. Em tela cheia, usar `foco` no rosto.
- Desenho em 4:3: `zoom` 1,15 para preencher o 16:9 e cortar bordas.

## Vídeos da obra

- `inicio` no segundo exato do plano: trailer começa com logos e corta rápido. Antes de escolher, montar uma folha de contato do trailer (um quadro a cada 2 s) e conferir o quadro no `inicio` escolhido; plano mais curto que o beat não serve.
- **Trechos com o áudio da obra:** 2 ou 3 por vídeo longo, 1 por Short, de 5–7 s, em fala marcante ou piada da obra que reforça o argumento. Entram pelo campo `pausas` do plano (a narração para) e `evidencia` com `som: true`, com a obra numa caixinha no canto. A trilha fica quase muda por baixo (`music.pausa` ≈ 0,08). Conferir a fala exata do trecho com Whisper antes e no render. Não usar trecho com canção licenciada (risco de Content ID).

## Som

- SFX em cada evento, abaixo da voz: corte 0,3; `impact`/`pop` 0,35–0,45; `explosao` no máximo 0,35. Nunca empilhar `sub` + `impact` fortes no primeiro segundo junto da voz (satura).
- **A trilha se ouve:** `music.volume` ≈ 0,8 e `music.duck` ≈ 0,55, ficando cerca de 15–20 dB abaixo da voz enquanto ela fala e subindo nos respiros. Trilha inaudível é erro.
- Uma faixa pode cobrir o vídeo todo com `music.trechos`: um trecho forte da própria faixa no gancho, a troca de trecho dentro de uma pausa com áudio da obra, e o final natural da faixa caindo sobre a tela final. Medir onde a faixa termina de verdade (o fim pode ser silêncio) antes de calcular.
- A trilha toca até o último quadro e sai em fade de ~4 s.
- Mix final: −14 LUFS integrado, pico abaixo de −1 dBTP.

## Fim do vídeo longo

- `cta` com `titulo: "DIAZVERSO"` e as caixinhas de inscrição e sininho.
- **Tela final de 15–20 s** (`telafinal`, a ComicPageCTA do Content Lab) depois da última fala, só com a trilha: dois vídeos do canal ligados ao tema e o espaço da bolinha do canal. Os mesmos vídeos vão em "Assista também" na descrição.

## Conferência do render

- Prévias de todo trecho alterado antes de renderizar; folha de contato dos frames.
- No arquivo final: duração, loudness e pico; os trechos com áudio da obra (a fala da obra aparece e a narração não); a tela final com música; os primeiros 5 s quadro a quadro.
- Fica só a versão final na pasta de saída; as anteriores vão para a lixeira quando o criador pedir.

## Shorts (9:16)

O Short tem exatamente este padrão, só que vertical:

- mesmo ritmo (troca a cada 1,5–3 s) e a mesma abertura (primeiros 3 s com 3–4 cortes e a imagem mais forte em alta resolução);
- **o Nox constante:** aparte ou `personagem` a cada 6–10 s, trocando de pose e expressão;
- legenda palavra a palavra o tempo todo;
- um trecho com o áudio da obra quando houver fala marcante;
- os mesmos níveis de som e trilha audível do começo ao fim;
- conteúdo entre 12% e 72% da altura (o kit diagrama todas as cenas para vertical);
- sem tela final; o `cta` fecha o Short.
