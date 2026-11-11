# H09 — Remotion runtime independente

Ambiente mínimo de **verificação de compilação e render**, não uma biblioteca de publicação e não uma continuação do Content Lab antigo.

- Versões exatas `remotion` e `@remotion/cli`: **4.0.542**; React 19; instalar dependências apenas no projeto isolado.
- Entrada: `src/index.ts`, composição `DiazversoSmoke` com **1080×1920, 30 fps, 60 quadros**.
- Cena é sintética (gradiente e texto originais). Exercita `useCurrentFrame`, `cropAndPan`, contraste e entrada do texto. **Não contém Nox, trecho de filme, narração ou música**.
- Com Node/npm e acesso permitido ao registro npm, executar `npm install --ignore-scripts` dentro desta pasta, seguido de `npm run render:still` e `npm run render:clip`. Os outputs são criados em `out/`, não empacotados na skill.
- Confirmar arquivos PNG/MP4 válidos e inspecionar os quadros. Um render verde deste smoke test **não valida** todos os componentes de H03–H07, nem sincronização de legendas, áudio ou conteúdo real.
- A função de vídeos publicados continua **fora do escopo**. O criador posta manualmente.
- Atenção: Remotion possui termos de licenciamento próprios; verificar aplicabilidade à utilização do projeto antes de produção comercial. Dependências npm não são redistribuídas no ZIP do plugin.

## I04 — cena vertical canônica integrada

A composição `DiazversoI04NoxVertical` reutiliza `DiazParallax`, `DiazKineticText` e `HQBackground`; usa somente o PNG canônico do Nox (hash conferido) e whoosh PCM sintetizado de forma autoral. **Não há narração falada nem sincronismo de legenda com voz**: os cues descrevem a ação de tela. A fonte de mídia do Nox não é substituída por imagens genéricas.

Após `npm install --no-audit --no-fund` no runtime, preparar apenas os arquivos de teste locais e renderizar:

```bash
python scripts/prepare_i04_assets.py
npx --no-install remotion still src/index.ts DiazversoI04NoxVertical out/i04-frame-15.png --frame=15
npx --no-install remotion still src/index.ts DiazversoI04NoxVertical out/i04-frame-105.png --frame=105
npx --no-install remotion still src/index.ts DiazversoI04NoxVertical out/i04-frame-200.png --frame=200
npx --no-install remotion render src/index.ts DiazversoI04NoxVertical out/i04-9x16.mp4 --frames=0-239 --codec=h264
python scripts/review_i04_outputs.py out
```

O verificador usa Pillow e checa arquivos, dimensões, H.264, trilha de áudio, variação visual e região de legenda. **Não substitui revisão visual nem escuta humana**, especialmente para produção editorial. A execução de CI que já renderizou e permitiu inspeção real é [43054774403](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/43054774403). Os três recursos locais `public/i04-*` são **gerados**, não assets adicionais autorizados para o ZIP e são excluídos antes do empacotamento no workflow. Não instalar o plugin no host durante desenvolvimento.

## L02/L03 — integração técnica roteiro → decupagem → voz/legenda → Remotion

Os exemplos **inéditos e não aprovados** em `fixtures/integrated-demos.json` servem para testar o pipeline independente, **não são vídeos editoriais do canal**. `scripts/build_integrated_demos.py` mede a duração de cada WAV gerado localmente, produz planos de cenas e contratos H01 validados, arquivo SRT e os mesmos cues para a composição TSX. Os arquivos de teste saem de `public/` e `out/` e **não são distribuídos no plugin**. O Short de 13,5 segundos é só um ensaio; a preferência editorial de 60 segundos não é testada neste fixture.

O executor usa `espeak-ng` ou `espeak` local quando existe; caso contrário, `mespeak@2.0.2` (GPL, **dependência npm somente de desenvolvimento**, não vendorizada no ZIP) para gerar áudio PT-BR sintético. A voz não representa uma licença para narração de produção e a inteligibilidade deve ser aprovada por escuta e pelo criador. Sem acesso a ferramentas de síntese, o pipeline de voz não é executável; o contrato H01 e a revisão de dados continuam disponíveis.

Após `npm install --no-audit --no-fund`, e com Python/Pillow disponível para QA:

```bash
python scripts/prepare_i04_assets.py
python scripts/build_integrated_demos.py
npx --no-install remotion render src/index.ts DiazversoIntegratedWide out/l02.mp4 --frames=0-599 --codec=h264 --props=out/l02-input.json
npx --no-install remotion render src/index.ts DiazversoIntegratedShort out/l03.mp4 --frames=0-404 --codec=h264 --props=out/l03-input.json
```

Depois de gerar também os PNGs dos frames indicados em `.github/workflows/integrated-video-e2e.yml`, executar `python scripts/review_integrated_outputs.py out public`. O workflow preserva MP4, PNG, SRT, decupagem H01 e relatório de QA. **Não afirma reconhecimento de fala, sincronismo fonético, escuta crítica, aprovação criativa, publicação nem integração nativa automática do Work/Codex**; os áudios e clips sintetizados são exclusivamente para teste. Não instalar o plugin antes da V1.0 completa e não automatizar postagem.
