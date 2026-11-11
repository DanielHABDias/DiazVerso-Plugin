# G08 — decisão de consolidação das utilidades HQ

**Data:** 11/11/2026. **Resultado:** não consolidar HQMotion.tsx/HQComicPage.tsx legados em runtime novo **neste momento**. A condição do item G08 era “quando necessário”, e a análise atual demonstrou que **não existe dependência funcional** dessas duas bibliotecas no sandbox Remotion independente.

## Evidência verificável no repositório

- `skills/diazverso-decupagem/runtime/src/root.tsx` registra somente a composição `SmokeScene`.
- `skills/diazverso-decupagem/runtime/src/smoke-scene.tsx` importa geometria de `references/motion/motion-math.mjs` e animação de texto de `kinetic-text-math.mjs`, não HQMotion/HQComicPage.
- `references/motion/motion-math.mjs` fornece `coverGeometry`, `cropAndPan`, `parallaxGeometry`, `clamp`, sem DOM/Canvas; a geometria é calculada para frames em pixels e pode ser testada isoladamente.
- `references/legacy/HQMotion.tsx` é a cópia de **referência** exata do arquivo histórico selecionado em G04. Funções legadas `imageBoundsHQ` e `fitLabelHQ` dependem de APIs DOM/Canvas, enquanto o runtime atual evita essa importação.
- `HQComicPage.tsx` é uma dependência de outros componentes do Content Lab antigo, **não localizada/validada** como arquivo fonte único neste ciclo; copiar uma das muitas variantes ou reconstruí-la sem necessidade ampliaria a superfície de erro e o tamanho do plugin.

## Decisão

1. **Há uma biblioteca única para geometria de câmera/parallax na V1:** `motion-math.mjs`. Evitar criar `HQMotion` alternativo ou cópias duplicadas.
2. **Não exigir uma implementação de HQComicPage** para compilar a composição já definida; o runtime independente usa sua própria cena de cor e moldura.
3. **A migração de componentes que dependam dessas APIs** só ocorrerá após G05/G06 comprovarem necessidade e compilação/render em 16:9 e 9:16. Nessa hipótese, adaptar utilitários pontualmente no módulo atual, sem importar TSX de 885 KB ou múltiplas versões do mesmo auxiliar.
4. **Não alegar** que G05/G06/H09/L02/L03 foram executados ou aprovados por esta decisão. G08 trata de arquitetura e eliminação da duplicação, não de vídeo renderizado.

**Status:** G08 encerrada por decisão de **não consolidar algo que não é usado**. Revisar a decisão apenas diante de uma nova dependência real. Sem escrita em Drive e sem postagem.
