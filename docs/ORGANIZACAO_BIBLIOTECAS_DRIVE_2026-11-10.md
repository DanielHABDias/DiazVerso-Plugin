# Diazverso — Bibliotecas de edição no Drive (estrutura aplicada)

> **Status em 2026-11-10: ALTERAÇÕES REALIZADAS E VERIFICADAS NO DRIVE, para avaliação do criador.**
>
> Esta documentação complementa [CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md](CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md). A organização operacional do Drive foi **ampliada por pedido do criador**: além de roteiros, thumbnails e planilha, agora existem **Backgrounds, Assets, Memes, Músicas e Sounds** dentro da raiz Diazverso. Isso substitui a hipótese anterior de não guardar bibliotecas reutilizáveis no Drive. **No futuro**, o repositório/plugin deverá incorporar ou referenciar os assets canônicos adequados, com inventário, critérios de qualidade, tamanho, direitos e controle de versão.

## 1. Raiz atual — links reais, NÃO universais

- [Diazverso](https://drive.google.com/drive/folders/1SbOI-GtWAaWzxFh1ysG5DOjf0DZ8XSYh) — pasta principal.
- [Canal do YT — V1.0 (Diazverso)](https://docs.google.com/spreadsheets/d/12_bYL2N9mwRj4lel_fNVOOPBruth-Ca2FsAjrgU1VQk/edit) — planilha de produção.
- [Roteiros](https://drive.google.com/drive/folders/1pYzyLLSPpH6HYu-sEaHt5JHs1gMlMNB6) — Longos/Shorts.
- [Thumbnails](https://drive.google.com/drive/folders/1gYR4s8oR6ZSHg-TnqL0EUA7yplU1H18B) — Longos/Shorts.
- [Assets](https://drive.google.com/drive/folders/1_DPaLie74I77ALn4t4ch_JBdrq9uGKBS).
- [Backgrounds](https://drive.google.com/drive/folders/1XPZSz653TZ3u4fzYh7uv1jN_IFdMHNxQ).
- [Memes](https://drive.google.com/drive/folders/1bOA6oQdyMbhb5xALF41T5_H7d_3znWaP).
- [Músicas](https://drive.google.com/drive/folders/1DMNhT3QaBqGYGJJjq1Ud9QkP_pxwlxpN).
- [Sounds](https://drive.google.com/drive/folders/1lhcCeidoYmRkdKa-nKDMfeTLMgS9vx3p).

As cinco bibliotecas foram movidas da raiz do Drive para `Diazverso/` preservando seus **IDs e URLs de acesso**; não duplicadas. Usuários/contas diferentes precisarão descobrir/criar seus próprios IDs. Nomes de pastas não são IDs globais nem identificadores suficientes para descartar ambiguidades.

## 2. Árvore atual, implementada

```text
Diazverso/
├── Canal do YT — V1.0 (Diazverso)  [Sheets]
├── Roteiros/
│   ├── Longos/
│   └── Shorts/
├── Thumbnails/
│   ├── Longos/
│   └── Shorts/
├── Assets/
│   ├── 01 - Identidade Diazverso/
│   │   ├── Nox/                         (inclui Nox.png)
│   │   └── HQ - Estética do Canal/
│   │       ├── Elementos Comic/
│   │       └── Banners/
│   ├── 02 - Motion e edição/
│   │   └── Edição/
│   │       ├── Overlays, Transições e Footage/
│   │       ├── Efeitos Elementais/
│   │       └── Shockwaves e Tintas/
│   ├── 03 - Recursos de apoio/
│   │   └── Gerais/                     (Marvel, setas/círculos, YouTube,
│   │                                   redes sociais, universo...)
│   └── 99 - Para avaliar/
│       ├── Imagens Avulsas/           (210 arquivos, maioria sem nome descritivo)
│       ├── ANIMAIS/                   (80 vídeos/imagens de origem mista)
│       ├── DINHEIRO/
│       ├── PESSOAS/
│       ├── GRÁFICOS/
│       ├── EMPRESAS/
│       └── Fora da identidade atual - revisar/
│           └── 39 comic style dialog boxes.zip
├── Backgrounds/
│   ├── Animados - MP4/               (30 vídeos/loops)
│   └── Estáticos - imagens/
│       ├── HQ e texturas/            (11 PNG)
│       ├── Cores sólidas/            (9 PNG)
│       └── Outros fundos/            (1 PNG)
├── Memes/
│   ├── Imagens/                      (138 imagens/GIFs)
│   └── Vídeos/                       (44 MP4)
├── Músicas/
│   ├── 01 - Favoritas e frequentes/
│   │   └── Muito usadas no YouTube/  (46 faixas; nome não assegura licença)
│   ├── 02 - Por clima/
│   │   ├── Lofi/                    (20)
│   │   ├── Animadas/                (6)
│   │   ├── Emocionantes/            (8)
│   │   ├── Sombrias/                (16)
│   │   └── Phonks/                  (8)
│   ├── 03 - Trilhas de obras (referências)/
│   │   ├── Filmes e Séries/         (14)
│   │   ├── Animes/                  (15)
│   │   └── Games/                   (41)
│   ├── 04 - Bibliotecas e origens/
│   │   ├── Biblioteca do YouTube/   (40, após separar possíveis duplicatas)
│   │   └── Clássicos do YouTube/    (6)
│   └── 99 - A classificar/
│       ├── 16 faixas de antigas pastas "Outras" consolidadas
│       └── Possíveis duplicatas - conferir/ (3 MP3)
└── Sounds/
    ├── Ambientes e Natureza/
    ├── Games e Referências/
    ├── Ações e Foley/
    ├── Cinemáticos e Tensão/
    ├── Interface e Notificações/
    ├── Impactos/
    ├── Memes/
    │   ├── Áudios extraídos de memes/     (24 MP3 antes em Memes/Vídeos)
    │   ├── Reações e efeitos diversos (a revisar)/ (48 MP3 antes na raiz Sounds)
    │   └── [pastas históricas BR, Reações, Anime, Cartoons...]
    └── Transições/                      (contém Whoosh, Glitch, Riser...)
```

A árvore distingue **origem/função** de **prioridade/uso**. Um arquivo em `Favoritas` é uma preferência histórica, não prova de autorização, de adequação a toda edição nem de qualidade. `99 - Para avaliar` é **acervo preservado** e NÃO lixeira: não considerar o conteúdo inútil sem avaliação visual/editorial.

## 3. Alterações efetuadas e verificadas

1. Mover as cinco pastas existentes (`Assets`, `Backgrounds`, `Memes`, `Musicas`, `Sounds`) para dentro de `Diazverso`; renomear `Musicas` para `Músicas`.
2. Criar quatro categorias de Assets, preservando `Nox`, HQ e Motion como recursos acessíveis. Colocar `Imagens Avulsas` (210), `ANIMAIS` (80), `DINHEIRO`, `EMPRESAS`, `PESSOAS`, `GRÁFICOS` em `99 - Para avaliar`. Os arquivos **não foram removidos**. Isolar um ZIP de balões de diálogo, desalinhado à atual preferência HQ sem balões, em revisão.
3. Backgrounds: renomear duas categorias para `Animados - MP4` e `Estáticos - imagens`; subdividir as 21 imagens em 11 HQ/texturas, 9 cores sólidas e 1 outro fundo; manter 30 loops MP4.
4. Memes: identificar 70 arquivos na antiga pasta `Vídeos` (44 MP4, 24 MP3, 2 JPG). Mover 24 áudios para `Sounds/Memes/Áudios extraídos de memes` e as 2 imagens para `Memes/Imagens`. Verificação posterior: **44 vídeos** em `Memes/Vídeos`, **138 imagens** em `Memes/Imagens`, **24 áudios** na nova pasta Sounds. Nenhum arquivo foi descartado.
5. Sounds: mover a antiga pasta `Outros efeitos sonoros` (48 arquivos) para `Sounds/Memes/Reações e efeitos diversos (a revisar)`, para reduzir confusão com sons utilitários e whooshes. Preservar demais categorias e subpastas de transições e seus efeitos.
6. Músicas: criar 5 grupos de navegação; mover 13 pastas originais entre eles; **consolidar 2 pastas duplicadas chamadas `Outras` em `99 - A classificar`** (16 MP3), excluir **somente as duas pastas vazias**.
7. Identificar candidatos a duplicata por **mesmo título/tamanho** em `Biblioteca do YouTube`: duas variantes de `Frightmare - Jimena Contreras` e uma variante `Nine Lives - Unicorn Heads`. Mover as 3 **para revisão, não excluir**. Sem comparar checksums ou áudio não podemos afirmar que são duplicatas bit a bit. 
8. Pastas de origem foram preservadas/movidas por ID, de modo que os links antigos aos arquivos permanecem os mesmos. A organização final foi conferida por listagens do Drive.

**Total de músicas conferido por listagens: 239 arquivos**, distribuídos entre Favoritas (46), Por clima (58), Obras/referências (70), Bibliotecas (46) e A classificar + duplicatas (19). A soma não constitui validação jurídica de licença. O item `Frightmare` ainda tem uma cópia fora da área de duplicatas.

## 4. O que NÃO foi feito e não deve ser assumido

- Nenhum arquivo de mídia foi apagado por "não parecer útil"; só as duas **pastas Outras vazias** foram excluídas após mover os 16 arquivos. Os recursos de `99` exigem revisão qualitativa antes de eventual descarte ou aprovação.
- Não foi feita uma audição faixa a faixa, reprodução/análise semântica de todos os vídeos, nem cálculo de hash de duplicatas. Classificação usou **nome, extensão, localização original e uso indicado pelo criador**. Portanto, "Animadas", "Cinemáticos", "Memes" etc. não são uma certificação de conteúdo/qualidade.
- A origem "Biblioteca do YouTube", "sem copyright", "royalty free" ou "no copyright" no nome de qualquer faixa **não comprova licença, monetização permitida ou isenção de Content ID**. OSTs de filmes/games/animes e músicas populares precisam de cuidado adicional; não publicar automaticamente sem avaliação de direitos.
- Os PNGs de personagens, memes, trilhas e overlays externos não devem ser distribuídos no pacote instalável do plugin sem confirmação de direitos de redistribuição.
- **Ainda não há biblioteca automatizada de busca por clima/duração/loudness/licença**, manifesto de assets canônicos, qualidade de áudio normalizada ou integração operacional Remotion/Content Lab. A reestruturação no Drive **não implementa as skills**.

## 5. Recomendações para o plugin Diazverso 1.0 (pendentes de implementação)

- Na inicialização da conta, localizar e vincular a raiz `Diazverso` e as 5 bibliotecas por IDs próprios, além de planilha, roteiros e thumbnails. **Não criar pastas duplicadas** quando já existirem e não assumir que a simples presença de pasta significa que os assets estão licenciados/validos.
- Construir **manifesto consultável sob demanda**: `asset_id`, link, coleção, subcategoria, formato, duração (quando medida), tags, descrição da função narrativa, volume/loudness (quando medido), licença/origem, restrições, preferência, status de auditoria. Não inferir metadados de áudio sem medir.
- Prioridade de importação ao futuro **repositório da skill/plugin**: Nox canônico após validação visual, backgrounds HQ aprovados, componentes TSX próprios e SFX recorrentes com direitos apropriados. **Não espelhar indiscriminadamente os 239 arquivos de música ou centenas de assets.**
- Em edição: consultar primeiro catálogos aprovados, depois a biblioteca de apoio; `99` deve ser consultada **somente quando o usuário estiver revisando o acervo ou precisar de um item específico**, não para inserção automática.
- Fazer QA de escolha de SFX/voz/trilha e evitar dependência do Google Drive em render (preferir cache/cópia de trabalho no ambiente autorizado, sem duplicatas permanentes).
- Documentar no bootstrap: quando o usuário disser apenas "vamos criar um vídeo", selecionar o próximo recurso de forma contextual, com evidência de licença, adequação narrativa e validação auditiva/visual quando ferramentas permitirem.

## 6. Próximas revisões (a decidir)

1. Avaliar visualmente as centenas de itens em `Assets/99`, em particular a coleção de imagens numéricas/avulsas e vídeos de animais: **manter, renomear, migrar para Memes ou descartar apenas com autorização específica**.
2. Verificar a licença e a procedência das músicas por fonte, além de **duplicatas por hash**, começando pelos candidatos já isolados. O nome da pasta não é certificação de direitos.
3. Criar seleção pequena de SFX de uso frequente (whoosh curto/longo/cinematográfico, ding, boom etc.) após escuta e medição para aproveitamento offline no plugin.
4. Validar qual `Nox.png` é canônico antes de integrar ao repositório e mapear backgrounds favoritos e TSX de referência.
5. Atualizar o futuro esquema de instalação do plugin para **bibliotecas opcionais**: Drive com pasta mínima de produção deve funcionar mesmo se o usuário não quiser carregar media libraries; quando as bibliotecas estiverem presentes, reutilizá-las sem recriação.

**Esta é a estrutura efetiva encontrada e aplicada; decisões sobre apagar/redistribuir arquivos continuam abertas.**
