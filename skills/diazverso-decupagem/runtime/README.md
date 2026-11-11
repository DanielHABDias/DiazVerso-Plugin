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
