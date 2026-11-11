# G04 — HQMotion.tsx legado: referência isolada, não runtime

**Fonte exata:** [HQMotion.tsx, Drive do Content Lab antigo](https://drive.google.com/file/d/1IM6cmzsKrcAtDFUWEZz6v4DxUBjN3UN_/view), arquivo de **2.958 bytes** na listagem. O conteúdo de texto foi copiado para `HQMotion.tsx` nesta pasta **como referência**, sem edição ou transpilação. Esse é o único TSX antigo selecionado para esta tarefa.

**O que contém e por que foi escolhido:**
- `imageBoundsHQ(src)`: usa `new Image()`, `document.createElement('canvas')` e pixel alpha para calcular bounding box; armazena até ~32 resultados num `Map<string, Promise<HQBounds>>`. É **específico de navegador** e pode falhar por CORS, navegador headless e leitura de canvas; não usar sem adaptar e testar no runtime de render.
- `progressHQ(time,start,duration,fps)` e `clampHQ`: matemáticas determinísticas, com especialidade no último frame; candidatas a reimplementar como utilitário puro e testar com frames reais.
- `fitLabelHQ(...)`: usa canvas e `measureText`, fonte precisa estar carregada no render para métricas corretas; variabilidade de ambiente.
- `edgeTravelHQ(...)`: cálculo determinístico de distância de viagem até borda.

**Dependências do arquivo selecionado:** nenhum `import` de `remotion`, `react` ou terceiro; requer TypeScript + APIs DOM `Image`, `document`, `HTMLCanvasElement` e contexto Canvas 2D. **Não é seguro importar o arquivo diretamente em testes Node sem DOM.** Dependentes históricos observados no Drive: `PersonagemEspiralLegenda.tsx` importa `imageBoundsHQ` e `ComicPageCTA.tsx` importa `fitLabelHQ`.

**Diferenças frente ao Diazverso atual:** preferir `references/motion/motion-math.mjs` para geometria determinística e o contrato H01 para frames/fps; manter mídias com origem/direitos, bloquear fontes não autorizadas e não usar DOM fora do render. `HQMotion.tsx` deve permanecer somente referência até G05 testar compilação, cena de composição e frames **16:9 e 9:16** no Remotion independente. Não presumir equivalência direta entre implementações ou compatibilidade de API.

**Status:** tarefa G04 (seleção, cópia de **um** arquivo e documentação de dependências/diferenças) concluída. **Render/TS TypeScript do legado não executados**; G05 continua pendente. Sem publicação de vídeos.
