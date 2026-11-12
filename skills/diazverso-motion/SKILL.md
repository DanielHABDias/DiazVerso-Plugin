---
name: diazverso-motion
description: "Use para montar o vídeo Diazverso como uma composição única de motion design (roteiro em beats, cenas HQ do kit, Nox com expressões, cenas das obras, som em cada troca), no ritmo das referências do canal, a partir de roteiro aprovado e narração ou sem narração."
---

**Protocolo obrigatório Diazverso:** antes de agir, aplicar `../diazverso-contexto-eficiente/SKILL.md`. Ler uma vez por sessão/versão e reutilizar o contexto válido; abrir somente a skill principal e as dependências necessárias.

# Motion: o vídeo como composição única

O vídeo do canal é **uma composição Remotion** escrita como **roteiro em beats**, não clips colados. O kit (`kit/`) faz o trabalho visual:

- câmera sempre em movimento, com entrada por zoom e desfoque;
- grão, linhas de scan e vinheta;
- palavras gigantes com aberração cromática;
- Nox com 8 expressões;
- painéis HQ, meio-tom e linhas de velocidade;
- tremor nos impactos e clarões nas trocas.

O roteiro em beats diz **o que** aparece, **quando** e **com qual som**.

## Fluxo

1. Partir do roteiro aprovado e do [padrão visual](../diazverso-core/references/padrao-visual.md). Para técnicas de ritmo, consultar a [linguagem das referências](references/linguagem.md).
2. Reunir as **cenas das obras** citadas: imagens e trechos curtos, com direitos conferidos ([imagens e direitos](../diazverso-core/references/imagens-e-direitos.md)). Nomes de arquivo descritivos (`batman-1940.jpg`) ajudam a casar mídia e fala.
3. Com narração: gerar ou gravar a narração, depois **transcrever com tempos por palavra**. Os beats começam onde a frase é dita. Sem narração: o texto na tela conduz, e os tempos seguem a música (tempos de 0,5 s a 120 BPM).
4. Escrever os beats com as cenas do [catálogo](kit/catalog.json): uma troca de informação a cada 1,5–3 s e nenhum beat parado acima de 6 s.
   - **Gancho:** `titulo`. **Evidência:** `evidencia`, `pagina` e `comparacao`.
   - **Reação ou dúvida:** `nox`. **Princípio:** `formula`. **Aplicação:** `lista`. **Dado:** `numero`.
   - **Respiro e payoff:** `frase`. **Encerramento:** `cta`.
5. Pôr som em cada troca (catálogo de SFX do kit) e uma trilha **licenciada** abaixando sob a voz ([música](../diazverso-decupagem/references/musica.md)).
6. Revisar frames de prévia antes do render: o assunto aparece? O texto é legível? Há sobreposição? A cena muda a cada poucos segundos? Corrigir um achado por vez.
7. Render final, escuta completa e o kit de publicação (`../diazverso-criacao-video/SKILL.md`).

## Contrato

Cada beat segue o contrato `diazverso-motion-v1`:

```json
{ "id": "b001", "scene": "evidencia", "at": 12.4, "duration": 2.6,
  "props": { "midia": "media:<id>", "rotulo": "BATMAN #1 (1940)", "humor": "surpreso" },
  "sfx": [{ "name": "camera", "at": 0, "volume": 0.5 }], "flash": false }
```

- Os beats ficam **em ordem e contíguos**.
- As mídias aparecem como `media:<id>`. O editor resolve esse id e copia para a pasta pública só os arquivos citados.
- A composição também recebe os tempos das palavras, para a legenda palavra a palavra e para abaixar a trilha sob a voz.
- `kit/Composition.tsx` documenta as props de entrada. `kit/index.ts` é o ponto de entrada do Remotion.

## 3D

`kit/three.tsx` traz duas cenas em Three.js (`@remotion/three`):

- **`nox3d`:** o Nox em 3D, uma releitura procedural do canônico com:
  - capuz;
  - rosto vazio;
  - olhos amarelos com os 8 humores;
  - sobretudo, punhos dourados, emblema e botas;
  - contorno de tinta e luz de recorte vermelha e azul.

  Ele cai em cena, a câmera gira em volta e ele faz um gesto: `acenar`, `apontar`, `pular`, `pensar` ou `parado`.
- **`paineis3d`:** a câmera voa por painéis HQ no espaço, cada um com uma imagem da obra e um rótulo.

O render precisa de WebGL; o editor usa `gl: "swangle"`, que funciona sem placa de vídeo. Leva cerca de 4 s de render por segundo de cena 3D. As cenas 3D são destaque: no máximo uma a cada ~30 s. Para criar outras cenas 3D, seguir o mesmo padrão:

- tempos derivados de `useCurrentFrame()`;
- câmera posicionada a cada frame (`Rig`);
- texturas carregadas com `delayRender`.

## Thumbnail

A thumbnail sai do mesmo kit: a composição `DiazversoThumb` (`kit/Thumbnail.tsx`) renderiza um still de 1280×720. O contrato está no catálogo (`thumbnail`):

- a mídia da obra como assunto dominante;
- até 4 palavras em Anton, com contorno e aberração cromática; a palavra entre *asteriscos* fica amarela;
- o Nox com a expressão do vídeo;
- um selo curto opcional;
- com duas mídias, o layout VS.

Pelo Content Lab: `thumbnails_generate`. A direção e a revisão ficam em `../diazverso-thumbnail/SKILL.md`.

## Assets

- **Nox:** a composição usa `assets/brand/nox/nox-sem-olhos.png`, uma variante do Nox canônico em que só os olhos foram cobertos com a cor do rosto; os olhos são redesenhados por expressão, na mesma posição, cor e brilho ([Nox](../diazverso-nox/SKILL.md)).
- **SFX:** são procedurais, ficam em `assets/sfx/motion/` e são reproduzidos por `scripts/build_motion_sfx.mjs <pasta-nova>`; a opção `--base` gera também uma base rítmica, que é só rascunho.
- **Fonte:** Anton, em `assets/brand/fonts/anton/`.

## Limites

- O kit não busca nem licencia mídia.
- Números inventados para explicar uma ideia levam a marca "simulação".
- Prévia e render exigem um projeto Remotion ou um editor compatível; o Content Lab implementa esse fluxo pelo MCP.
- Não declarar escuta, retenção ou aprovação sem arquivos reais e a decisão do criador.
