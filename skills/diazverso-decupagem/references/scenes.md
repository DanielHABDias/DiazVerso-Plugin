# Cenas TSX

Carregar somente o componente exigido pelo beat. São componentes React/Remotion independentes; a direção editorial vem de diazverso-core.

| Função | Componente | Props de referência |
| --- | --- | --- |
| Grafo de ideias, evidências e percurso | [BrainstormHQ](scenes/BrainstormHQ.tsx) | [cards](../examples/scenes/BrainstormHQ.json), [narrativa](../examples/scenes/BrainstormHQ-narrativa.json), [percurso](../examples/scenes/BrainstormHQ-percurso.json) |
| Comparação visual | [ComparativoIdeiasHQ](scenes/ComparativoIdeiasHQ.tsx) | [props](../examples/scenes/ComparativoIdeiasHQ.json) |
| Galeria de cartas | [GaleriaCartasHQ](scenes/GaleriaCartasHQ.tsx) | [props](../examples/scenes/GaleriaCartasHQ.json) |
| Imagem e frases | [ImagemFrasesHQ](scenes/ImagemFrasesHQ.tsx) | [props](../examples/scenes/ImagemFrasesHQ.json) |
| Página multipainel, split e parallax | [PaginaHQCenas](scenes/PaginaHQCenas.tsx) | [props](../examples/scenes/PaginaHQCenas.json) |
| Texto e palavras cinéticas | [TextoHQ](scenes/TextoHQ.tsx) | [props](../examples/scenes/TextoHQ.json) |
| Carrossel de frases | [CarrosselFrasesHQ](scenes/CarrosselFrasesHQ.tsx) | [props](../examples/scenes/CarrosselFrasesHQ.json) |
| Linha do tempo audiovisual | [LinhaDoTempoHQ](scenes/LinhaDoTempoHQ.tsx) | [props](../examples/scenes/LinhaDoTempoHQ.json) |
| Personagem, espiral e legenda | [PersonagemEspiralLegenda](scenes/PersonagemEspiralLegenda.tsx) | [props](../examples/scenes/PersonagemEspiralLegenda.json) |
| Diálogo contextual | [DialogoHQ](scenes/DialogoHQ.tsx) | [props](../examples/scenes/DialogoHQ.json) |
| Quadro sobre a cena | [QuadroHQSobreCena](scenes/QuadroHQSobreCena.tsx) | [props](../examples/scenes/QuadroHQSobreCena.json) |
| CTA de encerramento | [ComicPageCTA](scenes/ComicPageCTA.tsx) | [props](../examples/scenes/ComicPageCTA.json) |
| Caixa contextual | [CaixinhaHQ](scenes/CaixinhaHQ.tsx) | [props](../examples/scenes/CaixinhaHQ.json) |
| Barra de progresso | [BarraLoadingHQ](scenes/BarraLoadingHQ.tsx) | [props](../examples/scenes/BarraLoadingHQ.json) |

## Compor no projeto de edição

Os JSONs contêm component, duration_seconds, fps, props e required_files. São exemplos de entrada do componente, não o contrato completo de composição. Registrar a Composition no projeto Remotion, passar props e definir duração/dimensões a partir da produção aprovada.

Copiar os assets usados para public/ mantendo os caminhos relativos do plugin, ou resolver URLs explicitamente. Resolver também required_files: fontes e mídia do projeto não são presumidas como embutidas. Não executar um exemplo como produção aprovada.

Anton é o padrão dos componentes textuais. Fornecer sua URL local/licenciada em assets.anton; Bangers é opção explícita. [load-font](scenes/load-font.ts) usa FontFace no navegador e reutiliza o carregamento. Não há pacote de fontes ou download automático de fornecedor.

[HQMotion](scenes/HQMotion.tsx) oferece medição de alpha, ajuste de texto e movimento por frame. [SceneBackground](scenes/SceneBackground.tsx) configura o [fundo compartilhado](motion/hq-background.tsx), sem duplicar a implementação. Background opacity só afeta o fundo, não texto, cards ou imagens.

## Fundos e composição espacial

O fundo compartilhado oferece mode=solid, halftone, stars, film, paper, grid e comic-page. Stars usa movimento radial; film desenha riscos, poeira e flicker; paper alterna dobras; grid desliza continuamente. Solid e halftone usam baseColor. Ajustar opacity de 0 a 100.

A página transparente está em assets/brand/backgrounds/comic-page.png e é usada por [HQComicPage](scenes/HQComicPage.tsx), sem base64 no código. Em vertical, cover pode recortar bordas; conferir o enquadramento.

[NarrativeCamera](motion/narrative-camera.tsx) permite percorrer uma composição espacial com keyframes de posição, zoom e rotação; as camadas podem usar translateZ. Usar paradas motivadas pela narração, não um percurso fixo por obrigação.

Para repertório visual externo, consultar https://github.com/yihui-dev/awesome-opus5-5-videos somente quando necessário. É galeria de referências, não dependência instalada nem autorização automática sobre cada mídia.

Caixas, diálogos e CTA são opções contextuais; não substituem a identidade HQ madura nem devem aparecer por rotina. Sons, clipes e fontes precisam ser selecionados e revisados separadamente.
