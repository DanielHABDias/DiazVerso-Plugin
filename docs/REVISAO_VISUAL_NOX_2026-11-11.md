# A05/G01 — Revisão visual do Nox canônico e teste de pose real

**11/11/2026 — Inspeção de arquivos de imagem reais, não testes sintéticos.** As imagens foram abertas com o conector Drive e visualizadas. A auditoria de geometria/bytes também foi feita localmente. **Não houve geração nova de imagem nem modificação no arquivo canônico.**

## Arquivo original A05

- Fonte inspecionada: [Nox.png](https://drive.google.com/file/d/1X6pabe9ZhBTmOycrtURwg7nDzmJf_M61/view).
- Imagem **1408×768, RGBA, 415.179 bytes**; Git blob SHA-1 `776d1b26983e6f9095178881c83b44f114a40336`, correspondente ao `assets/manifest.json` do repositório; SHA-256 `6c00a247735261a3fedb1c7059ace8ff486c18b8e18b2e71b6cce1bcccae31c3`.
- Inspeção visual: mascote de baixa estatura e cabeça grande, capuz preto/cinza escuro com abertura facial totalmente negra, **olhos amarelos luminosos** com formato inclinado, contorno estilizado com **efeito duplo azul/ciano à direita e vermelho à esquerda**, luvas escuras, botas pretas, aro dourado nos punhos e **emblema triangular amarelo** no peito. Visual contemporâneo de quadrinhos, com formas simplificadas.
- Identidade compatível com a direção Diazverso V1 de HQ moderna/madura. O objetivo é **preservar esses traços distintivos**, sem importar automaticamente restrições não aprovadas do Character Lock antigo. Não obrigar a presença do personagem em toda cena.

## Teste de uma pose existente G01 (sem redesign)

- Pose real inspecionada: [Nox_Acenando.png](https://drive.google.com/file/d/16IFsVHoRvAQ-nkmj_4RwJo4o2daFozeT/view).
- Imagem **1408×768, PNG indexado (P) com transparência**, **116.091 bytes**; SHA-256 `c854d73608cc4f37678d5bbe3f07d152efe2ecc4196719c161810b40802c4166`. O `scripts/character_lock.py` passou a aceitar PNG indexado 8-bit além de RGB/RGBA, pois esse é um formato realmente encontrado nas poses antigas.
- Comparação visual direta entre referência e pose:
  1. **Silhueta/proporções:** cabeça/capuz, tronco, botas e proporção do personagem preservados, com braço erguido para acenar.
  2. **Rosto/olhos:** face negra e dois olhos amarelos inclinados preservados; sem boca ou face nova.
  3. **Paleta:** preto/cinza, amarelo, vermelho e azul/ciano preservados.
  4. **Roupa/acessórios:** mesmo capuz/casaco, luvas, botas, punhos dourados e emblema triangular no peito.
  5. **Estilo gráfico:** bordas marcadas, volume e aparência de HQ preservados; o PNG de pose usa indexação e transparência diferentes da referência, **diferença de formato não é redesign**.
  6. **Redesign:** não detectado visualmente nas características principais.
- **Resultado do teste de pose real existente:** `APROVADO COMO EXEMPLO DE CONSISTÊNCIA VISUAL`. Não confundir esse resultado com aprovação geral de todas as poses futuras nem com a criação de nova imagem. Novas poses devem continuar a passar por revisão individual. A pose histórica não foi adicionada ao pacote; origem/permissão de redistribuição precisam ser verificadas se vier a ser incorporada.

**Limite:** esta é uma **revisão visual humana/assistida registrada a partir de duas imagens efetivamente abertas**, com identificação das características observadas, e não reconhecimento automático pelo validador, teste do runtime Remotion ou prova de direitos sobre toda mídia. A05 cobre validação da arte canônica e G01 cobre uma pose específica sem redesign.
