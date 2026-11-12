# Som da edição: onde entra, de onde vem

A voz manda. Os SFX marcam o que acontece na tela, e a trilha fica por baixo. Cada som está ligado a um evento visível; som sem evento é ruído.

## 1. Onde pôr cada som

O som cai no quadro do evento, não no começo do beat por hábito.

| Evento na tela | Som do kit | Quando |
| --- | --- | --- |
| Corte seco para cena nova | `whoosh` ou `swish`, alternando; `whoosh-rapido` nos cortes de ritmo acelerado | começa 2–3 quadros antes do corte (`at: -0.08`) |
| Transição longa, câmera voando, entrada de capítulo | `whoosh-lento` | começa ~1 s antes da cena nova (`at: -1`) |
| Botão, caixinha de inscrição ou like sendo "clicada" | `clique` | no quadro do clique da caixinha |
| Sininho, notificação, "acertou" | `sino` | no quadro em que o ícone aparece |
| Explosão, revelação enorme, fundo `explosao` entrando | `explosao` | no quadro do estouro; abaixar a trilha junto |
| Piada física, "toma!", correção seca, meme | `tapa` (seco) ou `tapa-eco` (o tapa de meme, com eco) | na palavra da piada; `tapa-eco` no máximo uma vez a cada 1–2 minutos |
| Palavra gigante, título, virada | `impact` (+ `sub` só nas viradas fortes) | no quadro em que a palavra bate |
| Nox entra no aparte, balão estala, caixinha ou recorte aparece | `pop` | no quadro do estalo |
| Número subindo | `tick` em cada degrau e `ding` no valor final | acompanha o contador |
| Texto sendo digitado | `type` | enquanto as letras aparecem |
| Painel da HQ, frame da obra | `camera` | quando o painel entra |
| Erro, "não é bem assim" | `error` ou `glitch` | na palavra do erro |
| Tensão antes da revelação | `riser` | termina exatamente no corte da revelação (`at` negativo) |

Sons de meme (`tapa-eco`, `explosao`, `sino`) perdem a graça quando repetem: no máximo um a cada 1–2 minutos de vídeo longo, um por Short.

Regras:

- **Um som principal por evento**, no máximo dois em camada (por exemplo `impact` + `sub`).
- **Variar:** o mesmo som não repete em trocas seguidas; alternar `whoosh` e `swish`.
- **Não cobrir a fala:** perto de palavras, o SFX fica entre 0,3 e 0,5 de volume; mais alto só nas pausas e nas viradas.
- **Silêncio é ferramenta:** antes de uma virada, a trilha some por meio segundo e o `impact` volta com ela.
- **Som da obra:** se a cena mostra um soco, uma explosão ou uma porta, o som combina com essa ação (soco → `impact`, porta → `camera` curto). O áudio original da cena não entra.
- **Conferir no render:** escutar o vídeo inteiro, medir o loudness (alvo −14 LUFS, pico abaixo de −1 dBTP) e procurar som atrasado, adiantado ou empilhado.

## 2. Criar sons novos

Os 12 primeiros SFX do kit (de `pop` a `camera`) são sintetizados pelo `../scripts/build_motion_sfx.mjs`: são originais e não usam amostras de terceiros. Os de `clique` a `whoosh-lento` vieram do Openverse em CC0 pelo processo da seção 3, com créditos em `THIRD_PARTY_NOTICES.md`. Para um som que falta (por exemplo, `soco`, `porta` ou `vidro`):

1. Acrescentar a receita no gerador, com nome curto em minúsculas.
2. Gerar o WAV em 48 kHz mono em `assets/sfx/motion/<nome>.wav` e escutar.
3. Pôr o nome na lista `sfx` do `../kit/catalog.json` e o arquivo no `assets/manifest.json`, com `rights` original.
4. Rodar `python3 scripts/validate_plugin.py --refresh-map` e, no Content Lab, `npm run scenes:diazverso`. O nome passa a valer no plano.

## 3. Buscar sons prontos (Openverse)

O [Openverse](https://openverse.org) reúne sons com licença aberta (a maior parte do Freesound) e tem uma API pública sem chave:

```text
https://api.openverse.org/v1/audio/?q=<termo em inglês>&license_type=commercial&page_size=10
```

- **Filtro obrigatório:** `license_type=commercial`. O canal é monetizado.
- **Preferência:** CC0 (sem crédito). CC BY entra só com o crédito na descrição do vídeo (título, autor, licença, link). NC, ND e licenças desconhecidas não entram.
- **Campos a guardar:** `title`, `creator`, `license`, `license_version`, `foreign_landing_url`, `url` e `attribution`. O campo `duration` vem em milissegundos.
- **Pesquisar em inglês** e pelo som, não pela cena: `punch impact`, `glass shatter`, `door slam`, `swoosh`.
- **Preparar:** baixar o arquivo de `url`, converter para WAV 48 kHz mono, cortar o silêncio e normalizar o pico em −3 dBFS.
- **Registrar:** o arquivo vai para o catálogo como na seção 2, com `source` = `foreign_landing_url` e `rights` = licença e crédito.
- **Disponibilidade não é permissão:** conferir a licença na página de origem antes de usar.
- **Trilha:** a música continua seguindo [música](../../diazverso-decupagem/references/musica.md).
