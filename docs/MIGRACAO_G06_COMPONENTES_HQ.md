# G06 — migração seletiva dos componentes HQ para Remotion independente

**Data:** 11/11/2026. **Escopo:** substituir dependências do Content Lab antigo por duas implementações originais, sem redistribuir imagens e fontes incertas.

## 1. BackgroundHQ.tsx

**Origem estudada:** [BackgroundHQ.tsx no Drive antigo](https://drive.google.com/file/d/1-t41xttCihA1nJFR2AkKD-W2x_Mhr_nr/view).

O legado apresentava halftone, solid, stars, film, paper, grid e comic_page. Esse último estilo dependia de HQComicPage.tsx e de arte cujos direitos de redistribuição não estão comprovados.

**Migração independente:** runtime/src/hq-background.tsx e references/motion/hq-background-math.mjs, em commits próprios. Implementados fundos puramente procedurais: sólido, retícula, grade animada, estrelas discretas, filme e papel. Sem mídia PNG, fonte externa ou API proprietária. O modo comic_page é rejeitado intencionalmente.

## 2. QuadroHQSobreCena.tsx

**Origem estudada:** [QuadroHQSobreCena.tsx no Drive antigo](https://drive.google.com/file/d/1a7XLpnQ4UAqzfUSoIw1NN--9c0Aqf10V/view).

O legado dependia de HQComicPage, HQMotion.fitLabelHQ, @remotion/fonts e carregamento de Anton/Bangers por URL; disponibilidade e licenças de fonte não verificadas.

**Migração independente:** runtime/src/hq-overlay.tsx e references/motion/hq-overlay-math.mjs, em commits separados dos fundos. Suporta título superior, caixa inferior, etiqueta contrastante, revelação por frame e compactação só em widescreen. Usa fonte do sistema e quebra de texto automática. Não é cópia pixel a pixel do legado.

## Teste e integração

- A cena runtime/src/hq-migration-scene.tsx combina os dois componentes sem imagens externas.
- runtime/src/root.tsx registra DiazversoHQMigrationWide (1920×1080) e DiazversoHQMigrationVertical (1080×1920), ambos a 30 fps.
- tests/test_hq_components.mjs contém cinco casos de parâmetros, movimento, 16:9/9:16 e contraste.
- **9 verificações JS foram efetivamente executadas em V8 sobre o código dos módulos .mjs relido do GitHub e passaram**. Isso não comprova compilação TSX nem render Remotion.
- O GitHub Actions foi atualizado para renderizar stills dos dois formatos, verificar assinatura/dimensões PNG e guardar artefatos para inspeção; execução do CI após as mudanças ainda não confirmada.

**Critério da migração G06 atendido em código:** ambas as implementações foram adaptadas seletivamente, integradas e tiveram lógica testada. **G05/H09/L02/L03 seguem pendentes** de compilação Remotion e revisão visual real. Não instalar plugin, não escrever no Drive e não publicar vídeos.
