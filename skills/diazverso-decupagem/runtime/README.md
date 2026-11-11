# H09 — Remotion runtime independente

Ambiente mínimo de **verificação de compilação e render**, não uma biblioteca de publicação e não uma continuação do Content Lab antigo.

- Versões exatas `remotion` e `@remotion/cli`: **4.0.542**; React 19; instalar dependências apenas no projeto isolado.
- Entrada: `src/index.ts`, composição `DiazversoSmoke` com **1080×1920, 30 fps, 60 quadros**.
- Cena é sintética (gradiente e texto originais). Exercita `useCurrentFrame`, `cropAndPan`, contraste e entrada do texto. **Não contém Nox, trecho de filme, narração ou música**.
- Com Node/npm e acesso permitido ao registro npm, executar `npm install --ignore-scripts` dentro desta pasta, seguido de `npm run render:still` e `npm run render:clip`. Os outputs são criados em `out/`, não empacotados na skill.
- Confirmar arquivos PNG/MP4 válidos e inspecionar os quadros. Um render verde deste smoke test **não valida** todos os componentes de H03–H07, nem sincronização de legendas, áudio ou conteúdo real.
- A função de vídeos publicados continua **fora do escopo**. O criador posta manualmente.
- Atenção: Remotion possui termos de licenciamento próprios; verificar aplicabilidade à utilização do projeto antes de produção comercial. Dependências npm não são redistribuídas no ZIP do plugin.
