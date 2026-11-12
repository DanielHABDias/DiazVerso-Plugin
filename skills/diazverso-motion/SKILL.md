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
   - **Reação, piada ou dúvida:** `aparte` sobre a cena; `nox` de corpo inteiro só às vezes. **Princípio:** `formula`. **Aplicação:** `lista`. **Dado:** `numero`.
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

## O Nox na edição

A cena da obra é a base do vídeo, e o Nox não aparece o tempo todo:

- **Aparte (`aparte`):** a forma principal. A cena da obra desfoca, o Nox sobe pelo meio da cintura para cima e comenta em 1 a 4 tempos. A cada tempo ele muda de posição e de expressão, com um balão de ícone (`lampada`, `interrogacao`, `caveira`, `dinheiro`…) ou de texto acima dele. Depois ele desce, o balão some e o fundo volta nítido. Serve para piada, pergunta, ironia ou explicação rápida sobre o que está na tela.
- **Reação no canto:** `humor` em `evidencia` mostra só o rosto e o tronco, de vez em quando.
- **Corpo inteiro:** a cena `nox` fica para poucos momentos, como a abertura de um bloco ou uma reação forte.

## Shorts (9:16)

Todas as cenas do kit são diagramadas para 1080×1920:

- o conteúdo fica entre 12% e 72% da altura;
- a legenda fica acima da interface do Shorts;
- os painéis empilham, a comparação vira em cima e embaixo e a fórmula vira coluna.

O ritmo é o mesmo, com uma troca a cada 1,5–3 s.

## 3D

`kit/three.tsx` traz a cena `paineis3d`, em que a câmera voa por painéis HQ no espaço, cada um com uma imagem da obra e um rótulo. O render precisa de WebGL; o editor usa `gl: "swangle"`, que funciona sem placa de vídeo e leva cerca de 4 s de render por segundo de cena. É cena de destaque: no máximo uma a cada ~30 s. Novas cenas 3D seguem o mesmo padrão:

- tempos derivados de `useCurrentFrame()`;
- câmera posicionada a cada frame (`Rig`);
- texturas carregadas com `delayRender`.

## Thumbnail

A thumbnail sai do mesmo kit: a composição `DiazversoThumb` (`kit/Thumbnail.tsx`) renderiza um still de 1280×720. O contrato está no catálogo (`thumbnail`):

- a mídia da obra como assunto dominante;
- **limpa por padrão:** fundo preto ou branco e o personagem grande (um PNG transparente vira recorte);
- até 4 palavras em Anton, com a palavra entre *asteriscos* em cor; `fundo: "cena"` usa a mídia na imagem toda;
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
