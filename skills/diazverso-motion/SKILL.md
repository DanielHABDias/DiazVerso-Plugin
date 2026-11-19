---
name: diazverso-motion
description: "Use para montar o vídeo Diazverso como uma composição única de motion design no Content Lab (roteiro em beats, cenas HQ do kit do Content Lab, Nox em poses, cenas das obras, som em cada troca), no ritmo das referências do canal, a partir de roteiro aprovado e narração ou sem narração."
---

# Motion: o vídeo como composição única

O vídeo do canal é **uma composição Remotion** escrita como **roteiro em beats**, não clips colados. O kit de motion é do Content Lab (ferramenta neutra): o agente lê as cenas, props e SFX válidos em `motion_kit` e vê as cenas tocando na aba Documentação (`kit_docs`). Esta skill traz o padrão do canal para usar esse kit. O kit faz o trabalho visual:

- câmera sempre em movimento, com entrada por zoom e desfoque;
- grão, linhas de scan e vinheta;
- palavras gigantes com aberração cromática;
- o Nox, importado no projeto como personagem (`character_import`), em poses de stop motion;
- painéis HQ, meio-tom e linhas de velocidade;
- tremor nos impactos e clarões nas trocas.

O roteiro em beats diz **o que** aparece, **quando** e **com qual som**.

## Fluxo

1. Partir do roteiro aprovado, do [padrão de edição](references/padrao-de-edicao.md) (o nível que todo vídeo e todo Short precisa ter: abertura, ritmo, Nox, imagens, áudio da obra, som, tela final) e do [padrão visual](../diazverso-core/references/padrao-visual.md). Para técnicas de ritmo, consultar a [linguagem das referências](references/linguagem.md).
2. Reunir as **cenas das obras** citadas: imagens e trechos curtos, com direitos conferidos ([imagens e direitos](../diazverso-core/references/imagens-e-direitos.md)). Nomes de arquivo descritivos (`batman-1940.jpg`) ajudam a casar mídia e fala.
3. Com narração: gerar ou gravar a narração, depois **transcrever com tempos por palavra**. Os beats começam onde a frase é dita. Sem narração: o texto na tela conduz, e os tempos seguem a música (tempos de 0,5 s a 120 BPM).
4. Escrever os beats com as cenas de `motion_kit`: uma troca de informação a cada 1,5–3 s e nenhum beat parado acima de 6 s.
   - **Gancho:** `titulo`. **Evidência:** `evidencia`, `pagina` e `comparacao`.
   - **Opinião, piada ou dúvida:** `aparte` sobre a cena, com poses; `personagem` com `poses` só às vezes. **Princípio:** `formula`. **Aplicação:** `lista`. **Dado:** `numero`.
   - **Respiro e payoff:** `frase`. **Encerramento:** `cta`.
5. Selecionar eventos relevantes para o som, no quadro certo, e uma trilha **licenciada** abaixando sob a voz. Onde entra cada som, como criar um som novo e como buscar sons prontos no Openverse: [som](references/som.md). Música: [música](../diazverso-decupagem/references/musica.md).
6. Revisar frames de prévia antes do render: o assunto aparece? O texto é legível? Há sobreposição? A cena muda a cada poucos segundos? Corrigir um achado por vez.
7. Enviar o render final à fila e encerrar o turno, conforme a [regra principal](../diazverso/SKILL.md#regras-inegociáveis). Quando o criador voltar e o render estiver concluído, conferir o vídeo, escuta completa e o kit de publicação (`../diazverso-criacao-video/SKILL.md`).

Para investigação, ramificações, revelações, mudança de vínculo (`vinculo`), lembrança e retorno (`memoria`), alternância entre responsabilidades (`duplaVida`), linha do tempo navegável por capítulos (`trilhaViva`), Nox em close (`personagemClose`), pensamentos em balões (`pensamentoVivo`) e rasgo entre cenas (`rasgoCena`), consultar [uso narrativo das cenas do kit](references/cenas-narrativas.md). A implementação e os exemplos executáveis ficam exclusivamente no Content Lab. Para encaixes, comparação alinhada, detalhe/contexto, faixas, anotações, retorno de imagem, texto com recorte, reações do Nox e transições 2D, ler [montagens e transições 2D](references/montagens-2d.md).

## Contrato

Cada beat segue o contrato `contentlab-motion-v1` do Content Lab:

```json
{ "id": "b001", "scene": "evidencia", "at": 12.4, "duration": 2.6,
  "props": { "midia": "media:<id>", "rotulo": "BATMAN #1 (1940)", "humor": "surpreso" },
  "sfx": [{ "name": "camera", "at": 0, "volume": 0.5 }], "flash": false }
```

- Os beats ficam **em ordem e contíguos**.
- As mídias aparecem como `media:<id>`. O editor resolve esse id e copia para a pasta pública só os arquivos citados.
- A composição também recebe os tempos das palavras, para a legenda palavra a palavra e para abaixar a trilha sob a voz. A legenda fica o tempo todo nos Shorts; no vídeo longo, só no gancho e nos apartes do Nox (`legenda: false` nos outros beats).
- O `cta` não tem nome de canal fixo: pôr `titulo: "DIAZVERSO"` nas props.

## Tradução das cenas com som original

Aplicar a [regra de seleção e idioma](../diazverso/SKILL.md#regras-inegociáveis). Com a cena em inglês:

1. Transcrever o trecho real e traduzir todas as falas, inclusive interjeições; usar início/fim reais de cada frase, sem estimar pelos tempos da narração.
2. Manter um único beat `evidencia` com o vídeo em movimento e `som: true`, dentro de uma `pausa` da narração. A tradução não reinicia nem fatia o vídeo.
3. Usar `extras` do kit: `tipo: "caixinha"`, `preset: "livre"`, `texto`, `canto`, `at` e `duracao`. `at` é relativo ao início do beat. Dividir o diálogo em frases curtas e trocar a caixinha conforme a fala; Anton, contraste alto, margens seguras e posição que preserve rostos e ação. Respeitar os limites de texto/duração do kit.
4. Não usar `props.legenda` para despejar o diálogo inteiro de uma vez. Não exibir a legenda da narração nesses beats (`legenda: false`); as caixinhas traduzem o áudio da obra. A tradução é obrigatória mesmo no vídeo longo.
5. Conferir prévias no início, meio e fim de cada troca; na retomada após o render, conferir a tradução, o sincronismo, a ausência do narrador e a volta da frase inteira depois da cena.

## Como o vídeo se monta

- **A cena da obra é a base.** Em muitos beats ela fica sozinha, em tela cheia (`evidencia` com `cheia: true`), sem motion design por cima. Nos outros, ela ganha painel, rótulo, legenda e fundo.
- **Variar sempre.** Fundo, cor, tipo de cena e movimento nunca se repetem de um beat para o outro. Preferir Half-Tone (`halftone`) e meio-tom (`meio-tom`), alternando com estrelas, escuro e explosões gráficas nas três cores de destaque. O Half-Tone é o antigo fundo pontilhado chamado papel; os IDs `papel`, `papel-dobras`, `papel-hq` e `papel-sutil` são fundos distintos de papel amassado, disponíveis no kit, mas não são a base estética do canal. Não usar página decorativa como estética; páginas reais de HQ são conteúdo. Em `evidencia`, definir `fundo` explicitamente; na `telafinal`, usar `pagina: false`.
- **O Nox entra em opinião e humor, com frequência:** a cada 10–20 s no vídeo longo e a cada 6–10 s no Short, em aparte ou cena `personagem`. Ele só aparece se o pacote dele foi importado no projeto (`../diazverso-contentlab/SKILL.md`, passo 3); sem ele, o Content Lab não gera `aparte` nem a cena `personagem`:
  - **Aparte (`aparte`):** a cena da obra desfoca e o Nox aparece **inteiro**, subindo pela borda de baixo, com as pernas fora do quadro. Cada fala é uma **pose nova em stop motion**: troca seca de desenho e de lugar, sem quadros intermediários, com uma tremidinha de stop motion. Ele gesticula com as mãos (pensando com a mão na frente do rosto, arminha, apontando, dando de ombros, facepalm…), com um balão de ícone ou texto acima. No fim ele sai de uma vez e o fundo volta nítido.
  - **Variações de aparte:** `personagemClose` amplia o Nox e alterna ideias em balões; `pensamentoVivo` mantém até três pensamentos ao redor dele. Importar o personagem, escolher poses pelo sentido e conferir os olhos e as áreas seguras. Consultar o guia narrativo acima para props, tempos, som e continuidade.
  - **Cena `personagem` com `poses`:** a mesma troca de poses em cena própria, com texto curto de impacto ao lado.
  - **Reação no canto** (`humor` em `evidencia`): rara.
  - **Poses:** um PNG pronto por pose (gesto e olhos desenhados), com variantes sorteadas, em cada fala, escolhidos pelo tom: pergunta pensa, opinião aponta, erro é facepalm, piada é arminha ou rindo ([poses](../diazverso-nox/references/poses.md)). Não repetir a mesma pose em falas seguidas. A expressão vem do desenho da pose; `humor` só escolhe a pose pelo tom.
- **Extras por cima de qualquer cena** (campo `extras` do beat):
  - **caixinhas HQ de lembrete,** que não precisam ser faladas: inscreva-se, like, sininho, "minha opinião, tá?", alerta de spoiler, fonte, comenta aí;
  - **recortes PNG** do que está sendo falado (um objeto, um personagem recortado), que estalam na tela em stop motion.

## Fundos e acabamento

Escolher `fundo` entre as opções aceitas pela cena no `motion_kit`, não apenas pelo catálogo geral. Half-Tone (`halftone`) é o fundo pontilhado quente, anteriormente chamado papel; `meio-tom` é outra opção do kit e também é preferida no canal. O kit ainda oferece `estrelas`, `explosao`, `escuro` e `branco`. Os papéis procedurais são distintos: `papel` tem facetas amassadas; `papel-dobras`, vincos mais realistas; `papel-hq`, tons chapados, sombras em meio-tom e vincos de tinta; `papel-sutil`, dobras discretas. Eles mudam em passos de stop motion. Disponibilidade no aplicativo não os torna o fundo padrão do canal.

O fundo `explosao` cobre as duas proporções durante a rotação; não acrescentar máscaras ou ampliação para compensar uma falha antiga. Conferir os indicadores de foco nos cantos da revelação, carimbos de conclusão legíveis e contraste dos títulos sobre a obra. Título é opcional: omitir quando não acrescentar informação, em vez de preencher a barra por hábito.

## Shorts (9:16)

Todas as cenas do kit são diagramadas para 1080×1920:

- o conteúdo fica entre 12% e 72% da altura;
- a legenda fica acima da interface do Shorts;
- os painéis empilham, a comparação vira em cima e embaixo e a fórmula vira coluna.

O Short segue o mesmo [padrão de edição](references/padrao-de-edicao.md) do vídeo longo, no mesmo nível: troca a cada 1,5–3 s, abertura com 3–4 cortes, o Nox constante trocando de expressão, legenda o tempo todo, trilha audível e um trecho com o áudio da obra quando houver fala marcante.

## 3D

A cena `paineis3d` do kit é aquela em que a câmera voa por painéis HQ no espaço, cada um com imagem ou vídeo da obra como textura e um rótulo. Vídeo no painel não liga áudio original; para uma fala da obra, usar a cena e a pausa apropriadas. As props de cada painel são `midia` e `rotulo`; não inventar `inicio` nessa cena: preparar o recorte da mídia antes. O render precisa de WebGL; o editor usa `gl: "swangle"`, que funciona sem placa de vídeo e leva cerca de 4 s de render por segundo de cena. É cena de destaque: no máximo uma a cada ~30 s.

## Thumbnail

A thumbnail sai do mesmo kit do Content Lab: a composição `KitThumb` renderiza um still de 1280×720. O contrato está em `motion_kit` (`thumbnail`):

- **modelo do canal (`layout: "palavra"`):** palavra principal brilhante atrás do recorte com halo preto, contorno fino do texto à frente, palavra complementar opcional sólida e brilhante na frente, fundo simples de TV e Nox muito grande no canto por cima de tudo, com foco na cabeça e expressão ([modelo](../diazverso-thumbnail/references/modelo-palavra.md));
- `layout: "centro"` (rosto grande no meio, palavra embaixo), `layout: "lado"`, `fundo: "cena"` e o VS com duas mídias ficam para casos específicos;
- um selo curto opcional.

Pelo Content Lab: `thumbnails_generate`. A direção e a revisão ficam em `../diazverso-thumbnail/SKILL.md`.

## Assets

- **Nox:** o pacote fica em `assets/brand/nox/` (o `Nox.png` canônico e `poses/` com os PNGs e o `catalogo.json`). Ele entra em cada projeto do Content Lab por `character_import` ([Nox](../diazverso-nox/SKILL.md)).
- **SFX:** os do Content Lab valem no plano (`motion_kit`). As gravações e licenças vigentes são as do aplicativo; arquivos e receitas locais do plugin são referências, não substitutos automáticos dos sons do kit. Onde cada som entra: [som](references/som.md).
- **Fonte:** Anton, em `assets/brand/fonts/anton/`.

## Limites

- O kit não busca nem licencia mídia.
- Números inventados para explicar uma ideia levam a marca "simulação".
- Prévia e render são do Content Lab, pelo MCP (`motion_preview`, `render_start`).
- Não declarar escuta, retenção ou aprovação sem arquivos reais e a decisão do criador.
