# A03 — catálogo seletivo de TSX legados para motion (11/11/2026)

**Origem:** consulta de metadados de arquivos existentes no Google Drive antigo do Content Lab, sem importar bibliotecas indiscriminadamente. Estes arquivos são **referências históricas**, não dependências executáveis do plugin Diazverso. A pesquisa encontrou código real; copiar exige seleção deliberada.

| Prioridade | Arquivo | Tamanho de origem | Referência verificada no Drive | Uso/decisão |
| --- | --- | ---: | --- | --- |
| 1 | `HQMotion.tsx` | 2.958 bytes | [origem](https://drive.google.com/file/d/1IM6cmzsKrcAtDFUWEZz6v4DxUBjN3UN_/view) | **Escolhido G04**: um arquivo pequeno de utilitários para imagem/texto/progresso, copiado exatamente uma vez em `skills/diazverso-decupagem/references/legacy/HQMotion.tsx` |
| 2 | `TextoHQ.tsx` | 16.589 bytes | [origem](https://drive.google.com/file/d/1ojTb7ViaEj6WEYW2XiTNRLyWr1IO-Mer/view) | Referência de texto cinético; depende de `HQComicPage`, Remotion e `@remotion/fonts`; não copiar agora |
| 3 | `BackgroundHQ.tsx` | 6.825 bytes | [origem](https://drive.google.com/file/d/1-t41xttCihA1nJFR2AkKD-W2x_Mhr_nr/view) | Referência de fundo procedural; depende de `HQComicPage`, Remotion e React; G06 futura, não migrado |
| 4 | `QuadroHQSobreCena.tsx` | 5.764 bytes | [origem](https://drive.google.com/file/d/1a7XLpnQ4UAqzfUSoIw1NN--9c0Aqf10V/view) | Quadro sobre cena; avaliar na G06, não migrado |
| 5 | `PersonagemEspiralLegenda.tsx` | 9.807 bytes | [origem](https://drive.google.com/file/d/1jT1saDfR3VA1_NrDTj0gAOhjGgkyFcYm/view) | Auditado na G07: espiral + personagem + captions; **opcional**, não padrão |
| 6 | `ComicPageCTA.tsx` | 11.318 bytes | [origem](https://drive.google.com/file/d/1mK7Bbnx9k-pz58MkiH2ViT-MhIMm98FI/view) | Auditado na G07: CTA horizontal/vertical, com fontes e thumbnails; **opcional**, não padrão |

`HQMotion.tsx` também aparece repetido em vários caminhos do Drive, com metadados de tamanho iguais. O catálogo usa **somente um arquivo de origem específico**; duplicatas não integram a distribuição. `HQComicPage.tsx` não foi recuperado com sucesso nessa busca e continua dependência **não validada** para arquivos que o importam.

**Limites:** A03 identifica candidatos e decisões de escopo. Não afirma que TSX legado compila, renderiza ou é adequado ao Remotion atualizado. G05/G06/G08 mantêm gates de migração/render real. Não tornar arquivos legados dependências obrigatórias nem importar fontes ou mídias de terceiros.
