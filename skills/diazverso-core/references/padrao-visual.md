# Padrão visual mínimo

Critérios objetivos para a montagem em motion (`../../diazverso-motion/SKILL.md`) e a revisão de frames. Um vídeo que falha em qualquer item **bloqueante** volta para correção antes do render final. Conferir em frames reais extraídos do render, não no plano.

## Bloqueantes

1. **Imagem com assunto em toda cena.** Cada cena mostra o personagem, a obra, o acontecimento ou o Nox de que a fala trata: painel de HQ, frame oficial, pôster, capa, recorte ou pose do Nox. Texto sobre fundo liso ou procedural só é aceito em ênfase curta (até 3 s) e no máximo em 1 de cada 5 cenas.
2. **Evidência visual do que é afirmado.** Quando a narração cita um personagem, uma edição, uma cena ou um número, a imagem correspondente aparece enquanto a frase é dita. Consultar [imagens e direitos](imagens-e-direitos.md).
3. **Ritmo de informação visual.** Algo relevante muda na tela a cada **1,5–3 s**, no ritmo do RunnyIA: nova imagem, palavra-chave, troca de painel, reação do Nox, número mudando. Imagem da obra sustentada por até 3–5 s só quando o argumento pede, sempre com câmera lenta. Nenhum beat parado acima de 6 s. A câmera nunca fica parada (ver `../../diazverso-motion/SKILL.md`).
4. **Tipografia Anton** (`assets/brand/fonts/anton/Anton-Regular.ttf`, OFL) para títulos, palavras de impacto e legendas. Fonte de fallback do sistema reprova o frame.
5. **Legibilidade.** Texto principal com no mínimo **64 px** em 1080p horizontal e **72 px** em 1080×1920; legenda com no mínimo **56 px** (16:9) e **64 px** (9:16); contraste mínimo 4,5:1, com contorno ou caixa quando o fundo variar. No máximo **6 palavras** por bloco de texto de ênfase.
6. **Legenda palavra a palavra** a partir de timestamps reais da fala (`../../diazverso-shorts/scripts/captions.py`). Legenda por cena ou frase inteira estática reprova o Short.
7. **Sem tela vazia.** Nenhum frame preto, branco ou só fundo entre cenas; transições cortam ou cobrem, nunca apagam para preto, exceto fim do vídeo.
8. **Nox fiel ao asset canônico** sempre que aparecer, nunca desenhado de memória nem substituído por texto com o nome dele.

## Linguagem HQ madura

- **Base:** fundo de página HQ (`assets/brand/backgrounds/comic-page.png`), halftone ou papel com opacidade 20–45%; nunca fundo liso chapado como cena inteira.
- **Paleta:** tinta `#0B0B10`, papel `#F2E8D5`, destaque amarelo `#F5C518`, vermelho `#E63946` e azul `#2676E8`. Uma cor de destaque dominante por cena.
- **Composição:** painéis com borda de tinta 6–10 px, leve rotação (±2°), sombra deslocada sólida; imagens recortadas em painéis, não soltas no centro.
- **Movimento:** a câmera está sempre em movimento suave (empurrão lento, leve deriva), com entrada por zoom em cada troca e tremor só em impacto. Evitar pulsar sem motivo e efeitos que competem com a leitura.
- **Hierarquia por cena:** um assunto principal, uma palavra de impacto e no máximo um elemento de apoio (seta, ícone, selo).

## Shorts

- Assunto e texto dentro do preset `../../diazverso-shorts/references/preset-vertical-v1.json`; legenda no terço inferior reservado, imagem principal entre 15% e 60% da altura.
- **Gancho visual no primeiro segundo:** a imagem mais forte do vídeo abre o Short, já com o texto do gancho.
- Duração preferida de pelo menos 60 s quando o conteúdo sustentar; menos que isso é decisão do criador, registrada.

## Revisão de frames

Extrair 1 frame por cena e mais 3 frames por minuto (`../../diazverso-decupagem/scripts/extract_review_frames.py`), montar a folha de contato e responder por frame: há assunto reconhecível? o texto é legível no celular? a fonte é Anton? a imagem corresponde à fala? Anotar o achado e corrigir pelo `correction_loop.py`.
