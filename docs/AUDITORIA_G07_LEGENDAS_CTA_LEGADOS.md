# G07 — auditoria pontual de PersonagemEspiralLegenda e ComicPageCTA

**Data:** 11/11/2026. **Método:** arquivos TSX reais lidos no Drive, com importações, props e comportamento relevante inspecionados; **sem copiar arquivos para o pacote, sem compilar e sem renderizar**.

## PersonagemEspiralLegenda.tsx

[Origem única inspecionada](https://drive.google.com/file/d/1jT1saDfR3VA1_NrDTj0gAOhjGgkyFcYm/view). Importa `imageBoundsHQ` de `./HQMotion`, `HQComicPage` e `HQComicPageOptions` de `./HQComicPage`, React, Remotion (`AbsoluteFill`, `Img`, `delayRender`, `continueRender`, `cancelRender`, `useCurrentFrame`, `useVideoConfig`), `loadFont` de `@remotion/fonts` e `Caption` de `@remotion/captions`.

**Opções observadas:** fundo `espiral`/`crescente`, `captions` **ou** `words` com `start/end` e `transcriptOffset`, cores de destaque, fonte Bangers/Anton, escala e ancoragem da cabeça, animação de personagem e paginação de legendas. A função `spiralField` gera textura em canvas; o código usa `React.useLayoutEffect` e `ImageData` para espiral pixelada, necessitando navegador/render de verdade. `imageBoundsHQ` lê pixels de imagem com canvas, sujeito a CORS e disponibilidade do asset. Exige `assets.character` PNG transparente e URL de fonte, não inclui assets físicos.

**Riscos:** dependência `HQComicPage` ainda não validada neste catálogo; permissões das fontes; legibilidade/contraste; alinhamento de legendas por frame, `Caption.startMs/endMs` versus `Word.start/end` com unidades potencialmente diferentes; travamento ou cancelamento de render durante fontes/imagens. **Não torna a espiral obrigatória.** Preferir G07 como referência de boas ideias; a legenda padrão Diazverso deve usar o fluxo independente I02/I03 de captions e o validador H01.

## ComicPageCTA.tsx

[Origem única inspecionada](https://drive.google.com/file/d/1mK7Bbnx9k-pz58MkiH2ViT-MhIMm98FI/view). Importa `fitLabelHQ` de `./HQMotion`, `HQComicPage`, React, Remotion e `loadFont` de `@remotion/fonts`. Permite `channelName`, `topTitle`, `subscribeText`, `calloutText`, `headline`, `stripeColor`, `leftTitle`, `rightTitle` e assets opcionais de thumbnail esquerda/direita, thumbnail vertical, ícone, personagem e fontes.

**Comportamento observado:** ramifica layout conforme `width > height`, requer `assets.thumbnail` no modo vertical e `assets.character` nos dois modos; valida escala, `timingScale`, `fadeOutDuration` e cor. Calcula encaixe de texto usando `fitLabelHQ` e espera carregamento de fonte com `delayRender`. O conteúdo padrão contém textos CTA de inscrição e indicação de outros vídeos, com destaques e estruturas de balões/quadros do estilo anterior.

**Riscos:** adaptar identidade editorial e CTA ao vídeo real (não obrigar balões, chamadas ou tela final), direitos e disponibilidade de miniaturas/mascote, diferença de composição 16:9/9:16, métricas da fonte e telas pequenas. Não assumir que uma tela vertical precisa copiar o CTA legado. **Não copiar automaticamente.**

## Decisões

1. **G07 é auditoria**, não migração: os dois códigos permaneceram fora das skills distribuídas. Seu comportamento exige renders e revisão humana posteriores em G05/I04/L02/L03.
2. Para legendas, manter `diazverso-shorts` e contratos atuais. Para CTA, preferir solução condicional editorial simples antes de portar qualquer balão ou layout vintage.
3. Caso surja necessidade comprovada, migrar **apenas um componente por vez**, revisar a API atual `@remotion/captions`, fontes e licenças, testar compilação, 16:9/9:16, frames intermediários e áudios reais.
4. Não transformar espiral, balões, thumbnails de outros vídeos nem mascote em **padrões obrigatórios** de cada produção.

**Status G07:** análise técnica dos dois arquivos reais e decisão de não impor estéticas antigas concluídas; sem alegar execução TSX ou render. Testes de render estão em outras tarefas.
