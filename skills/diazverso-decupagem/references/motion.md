# Biblioteca motion

Consultar apenas o componente exigido pela cena. Os TSX usam React/Remotion do projeto de edição; não instalam dependências.

| Função | Arquivo | Uso |
| --- | --- | --- |
| Câmera e enquadramento | motion/camera.tsx | Movimento contextual em duração definida |
| Profundidade | motion/parallax.tsx | Camadas, profundidade e limites seguros |
| Texto cinético | motion/kinetic-text.tsx | Palavras com startFrame/durationFrames relativos à cena; contraste mínimo 4,5:1 |
| Trecho de vídeo em monitor | motion/crt-panel.tsx | Mídia, duração e direitos verificados; áudio original exige autorização separada |
| Fundo procedural | motion/hq-background.tsx | Halftone, grade, estrelas, filme, papel ou cor |
| Overlay HQ | motion/hq-overlay.tsx | Texto e composição sem mídia externa |
| Matemática HQ | motion/hq-motion-math.mjs | Progresso por frame e geometria de entrada/saída |

Os módulos `motion/*-math.mjs` validam geometria, cores e tempos. Fontes só entram quando disponíveis e licenciadas; não presumir Anton instalado.

## Planejamento de som

`audio/audio-plan.mjs` expõe `planAudio(catalog, scene, options)`. O catálogo exige ID, caminho relativo seguro, tipo music/sfx, duração em frames, tags, rights=APPROVED e evidência de autorização real.

A cena informa duração, clima, tags de SFX, intervalos de voz e offsets. O planejador seleciona cues e ducking, sem ouvir, baixar ou licenciar mídia. Não inserir item pendente no catálogo aprovado. Verificar mix, silêncio, transições e inteligibilidade no render.

Nox segue `../../diazverso-nox/SKILL.md`. O fundo procedural é independente de imagens adicionais; qualquer imagem de outra origem exige direitos conferidos.
