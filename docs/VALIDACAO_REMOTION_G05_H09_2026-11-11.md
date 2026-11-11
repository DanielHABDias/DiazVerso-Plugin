# G05 / H09 — Render real Remotion independente e QA de quadros

**Resultado: APROVADO para o escopo técnico do smoke test.** Em 11/11/2026, a V1 do runtime Remotion independente compilou e renderizou quatro imagens reais e dois MP4 no GitHub Actions, sem importar o Content Lab. A execução completa do workflow [43050305634](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/43050305634) terminou com **sucesso** na revisão `961406be056b10d240d8b2dc48e29fb233d3a722`. Artefato oficial: [diazverso-remotion-smoke-16x9-9x16](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/43050305634/artifacts/13869207661), baixado e inspecionado localmente.

## O que foi efetivamente executado

- `npm install` com Remotion/CLI 4.0.542; `npm test` no runtime e testes Python/Node do pacote passaram no workflow.
- Remotion compilou as composições `DiazversoSmokeWide` (1920×1080), `DiazversoSmoke` (1080×1920), `DiazversoHQMigrationWide` e `DiazversoHQMigrationVertical`.
- `smoke-16x9.mp4` e `smoke-9x16.mp4`: H.264, 30 fps, **30 quadros/1 segundo** cada, dimensões confirmadas por leitura de caixas ISO BMFF (script `scripts/verify_remotion_outputs.py`) e também por `ffprobe` local após baixar os arquivos.
- Os quatro PNGs reais foram lidos integralmente e as dimensões conferidas. Os arquivos não são imagens de busca ou ilustrações inventadas.
- Frames **0, 15 e 29** foram extraídos dos dois MP4s. A diferença média de pixels entre o primeiro e o último foi **(8,01; 9,28; 12,10)** em 16:9 e **(9,02; 9,79; 11,76)** em 9:16, demonstrando movimento visual não nulo; não equivale a julgamento editorial de fluidez.
- Inspeção visual direta de **quatro imagens PNG**: títulos brancos legíveis, bordas/molduras dentro do quadro, fundo íntegro nos dois formatos; a cena HQ usa grade procedural, etiqueta e tarja claras. Não foi identificado corte evidente do texto nas imagens avaliadas.

## Hashes dos artefatos analisados

| Arquivo real | SHA-256 |
| --- | --- |
| `smoke-16x9.png` | `247648f2782a506449d14e25d7b078fba965591ec9a2822d73222ca790f15930` |
| `smoke-9x16.png` | `0e7a316a06b3d103230b0536f30ad7ca661bd5ad1e9edc0bd68458dd1a72f803` |
| `hq-migration-16x9.png` | `b23be2292a2d3e416f0041e4c8930bb360393f6d8317cde19a89cc69682294fa` |
| `hq-migration-9x16.png` | `0a08cf9e8eb29f8445bcf45ea132d83d664aeca043c9e9d8fc9b48c48913f863` |
| `smoke-16x9.mp4` | `f4858f8a141a42fd3c3d4fa04e860477de2e0cd87d50a5ae5b31867952d5747e` |
| `smoke-9x16.mp4` | `36e56d2c37efd4b5645fae2a1e868c760bf13f8708f6d7478ee5c321a9474d39` |

## Falhas encontradas e corrigidas antes da aprovação

1. [Run 43043716700](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/43043716700): teste de E08 esperava substituir `ROTEIRO` por `PUBLICADO` sem `allow_replace`; planner retornou corretamente `CONFLICT`. Corrigido o teste e incluído caso que preserva a proteção contra substituição sem autorização (commit `30bfdfbb47caa7301700e1c107bea5b2ebcaf5bf`).
2. [Run 43049311429](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/43049311429): **os renders 16:9 e 9:16 foram produzidos**, mas o verificador de MP4 falhou por ausência do executável `ffprobe` no runner. Criado `scripts/verify_remotion_outputs.py`, validador Python sem dependência externa de CLI; testado localmente contra dois MP4 reais gerados por FFmpeg e os seis arquivos do artefato final. Workflow atualizado em `961406be056b10d240d8b2dc48e29fb233d3a722`.

## Escopo dos itens encerrados

**G05 [x]:** cena do sandbox usa port seletivo do `HQMotion.tsx` legado para matemática pura; compilação e render real Remotion independente ocorreram em 16:9/9:16 com inspeção visual de quadros.

**H09 [x]:** smoke test de runtime Remotion independente passou em CI, gerou PNG/MP4 reais e confirmou resolução/codec/quadros sem depender do Content Lab.

**Não significa:** que roteiro/narração, Nox, legendas de Short, whoosh, sincronização de áudio, montagem completa ou vídeo final foram executados. **I04, L02 e L03 continuam [ ]**, assim como os gates de direitos de mídia e ZIP final L06/L07. Não instalar o plugin no ChatGPT/Codex durante o desenvolvimento e nunca automatizar postagem.
