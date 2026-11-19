# Som da edição: onde entra, de onde vem

A voz manda. Os SFX marcam o que acontece na tela, e a trilha fica por baixo. Cada som está ligado a um evento visível; som sem evento é ruído.

## 1. Onde pôr cada som

O som cai no quadro do evento, não no começo do beat por hábito.

| Evento na tela | Som do kit | Quando |
| --- | --- | --- |
| Corte seco para cena nova | `whoosh` ou `swish`, alternando; `whoosh-rapido` nos cortes de ritmo acelerado | alinhar o ataque ao corte; antecipar só após escutar o arquivo atual |
| Transição longa, câmera voando, entrada de capítulo | `whoosh-lento` | ajustar o movimento à gravação atual (arquivo de ~2,16 s), conferindo o ponto de chegada |
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
| Tensão antes da revelação | `riser` ou `riser-reverso` | `riser` dura ~1,82 s; o prato invertido `riser-reverso` cresce por ~2,90 s até o corte. Posicionar o início para a chegada coincidir com a revelação |

Sons de meme (`tapa-eco`, `explosao`, `sino`) perdem a graça quando repetem: no máximo um a cada 1–2 minutos de vídeo longo, um por Short.

Regras:

- **Um som principal por evento**, no máximo dois em camada (por exemplo `impact` + `sub`).
- **Variar:** o mesmo som não repete em trocas seguidas; alternar `whoosh` e `swish`.
- **Não cobrir a fala:** corte (`whoosh`, `swish`) em 0,3; `impact`, `pop` e `camera` entre 0,35 e 0,45; `explosao` no máximo 0,35. Nunca empilhar `sub` e `impact` fortes junto da voz (satura o pico).
- **Silêncio é ferramenta:** antes de uma virada, a trilha some por meio segundo e o `impact` volta com ela.
- **Som da obra:** no plano comum, se a cena mostra um soco, uma explosão ou uma porta, o SFX combina com essa ação (soco → `impact`, porta → `camera` curto) e o vídeo da obra fica mudo. O áudio original entra só nos trechos escolhidos de 5–7 s (2–3 por vídeo longo, 1 por Short) com `pausas` no plano e `som: true` na cena, conforme o [padrão de edição](padrao-de-edicao.md).
- **Conferência da origem:** nos intervalos sem narrador, o áudio original acompanha o vídeo real da obra. Trilha/SFX criados para um painel, foto ou frame não são áudio original da obra; não criar uma pausa de narração para esse material. Escutar cada candidato, registrar fala/ação e fonte, abaixar a trilha do canal e verificar a reprodução efetiva no render.
- **A trilha se ouve:** cerca de 15–20 dB abaixo da voz enquanto ela fala (no Content Lab, `music.volume` ≈ 0,8 e `music.duck` ≈ 0,55), subindo nos respiros e quase muda sob o áudio da obra (`music.pausa` ≈ 0,08).
- **Conferir no render:** escutar o vídeo inteiro, medir o loudness (alvo −14 LUFS, pico abaixo de −1 dBTP) e procurar som atrasado, adiantado ou empilhado.

## 2. Criar sons novos

As gravações vigentes pertencem ao kit do Content Lab, consultado por `motion_kit` e `kit_docs`. `pop`, `whoosh`, `swish`, `camera`, `sub` e `impact` usam gravações CC0; `ding`, `error`, `riser`, `type` e `riser-reverso` vêm da coleção do criador/Pixabay. Conferir os créditos e as condições por arquivo no [registro de licenças do Content Lab](https://github.com/DanielHABDias/ContentLab/blob/main/licenses/THIRD_PARTY.md). Não atribuir automaticamente aos sons atuais a origem sintética ou a licença das referências locais do plugin.

Durações aproximadas dos arquivos do kit, incluindo suas caudas:

| SFX | Segundos | SFX | Segundos |
| --- | ---: | --- | ---: |
| `pop` | 0,093 | `camera` | 0,295 |
| `whoosh` | 0,667 | `swish` | 0,330 |
| `whoosh-rapido` | 0,330 | `whoosh-lento` | 2,161 |
| `impact` | 2,000 | `sub` | 1,332 |
| `ding` | 0,589 | `error` | 0,310 |
| `riser` | 1,820 | `riser-reverso` | 2,902 |
| `type` | 0,150 | `tick` | 0,050 |
| `clique` | 0,090 | `sino` | 1,328 |
| `explosao` | 2,591 | `glitch` | 0,350 |
| `tapa` | 0,131 | `tapa-eco` | 1,500 |

Duração de arquivo não é instante de ataque nem de pico. Escutar antes de alinhar; se os arquivos mudarem, medir de novo. Para uma revelação em T, começar o `riser-reverso` aproximadamente em T − 2,902 s e conferir a chegada no render. Se não houver espaço no beat, antecipar no beat anterior com tempo relativo válido; não cortar a subida para caber por hábito.

Nas cenas narrativas, recalcular `narrativeEvents` com props, duração e fps reais e usar sua saída em `beat.sfx`. O helper mantém cerca de um som por segundo, prioriza viradas (`impact`, `error`, `sub`) e espaça sinais em geral por 0,3 s; `sub` pode reforçar `impact`. Não acrescentar som a cada cartão para compensar a redução automática. Conferir caudas entre beats e deixar diálogos emocionais respirarem.

Para um som que falta, buscar uma gravação licenciada ou criar uma receita original. O gerador local `../scripts/build_motion_sfx.mjs` serve para novos rascunhos sintéticos, sem substituir as gravações do kit. Para usar um novo nome no plano, acrescentar o WAV e a licença ao repositório do Content Lab e registrar no catálogo; só então `motion_kit` passa a aceitá-lo. Se distribuir o arquivo no plugin, atualizar também `assets/manifest.json` e validar.

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
