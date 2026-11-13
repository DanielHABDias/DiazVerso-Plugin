# Escrever o roteiro

O roteiro é escrito para ser **ouvido** e **montado em beats**. A fala mantém períodos naturais e conversacionais; as trocas visuais em beats são decididas na montagem, sem obrigar a quebrar toda frase em 1,5–3 s.

## Antes de escrever

- **Embalagem pronta:** título e conceito de thumbnail escolhidos (`../../diazverso-titulos/SKILL.md`). O roteiro existe para cumprir essa promessa, e a abertura confirma o clique nos primeiros segundos.
- **Uma frase-tese:** "[personagem] mostra que [ideia], porque [escolha/consequência]". Se não cabe em uma frase, a pauta ainda não está pronta.
- **Payoff definido:** o que o público entende no fim. Escrever o fim antes do meio.

## Estrutura do vídeo longo

A estrutura combina como as três referências do canal constroem o roteiro, medidas nos próprios vídeos:

- **RunnyIA:** dor do espectador → prova → promessa contável → cada item demonstrado na tela;
- **Um Nerd:** pergunta → definição → casos → padrão → contraponto → síntese;
- **FALL:** preparação → acontecimento → reação.

1. **Gancho (0–15 s).** Escolher uma das três aberturas, sem "hoje vamos falar" nem apresentação do canal:
   - **"Imagina…"** (RunnyIA): uma situação na segunda pessoa que o público reconhece ("imagina passar a vida inteira protegendo todo mundo… e ninguém lembrar de você").
   - **Teste direto** (Um Nerd): uma pergunta que o público tenta responder e erra ("quem foi o segundo Lanterna Verde?"). A diferença entre as respostas vira a tese.
   - **Premissa absurda ou contradição** (FALL): o fato estranho dito de cara ("o herói mais forte da DC é o mais chato de ler").
2. **Prova e promessa (15–40 s).** Uma prova curta de que o problema é real: uma cena, um dado, uma capa. Depois, a promessa **contável**: "três decisões", "cinco erros", "a cena que mudou tudo". A promessa vira um mapa na tela (`lista`), e o vídeo volta a ele a cada item.
3. **Definição (quando houver conceito).** Dizer em uma ou duas frases o que é a ideia antes dos casos ("legado não é qualquer substituto: é…").
4. **Casos, do mais fraco ao mais forte.** Cada caso segue a mesma batida:
   - **situação da obra:** a cena ou edição, mostrada na tela;
   - **escolha:** o que o personagem decide;
   - **consequência:** o que isso custa;
   - **o que revela:** o princípio.
   Entre um caso e outro vem um novo gancho ("e esse nem é o mais estranho…").
5. **Reação e humor.** Preparação → acontecimento → reação, com o Nox comentando em aparte sobre a cena. A piada nasce do caso e não interrompe a explicação antes de ela ser entendida.
6. **Contraponto.** O limite da tese ou o outro lado (o que a Marvel faz diferente, quando a regra falha). É ele que dá credibilidade.
7. **Síntese e payoff.** Responder a promessa do gancho com a imagem mais forte guardada para o fim. Em ensino, terminar na aplicação: o que o público pode fazer ou pensar diferente ([formatos](../../diazverso-core/references/formatos-editoriais.md)).
8. **CTA.** Uma pergunta que nasce do vídeo, para os comentários. Um CTA curto no meio, depois do primeiro caso forte, é opcional.

Ao longo do texto:

- **Ligações:** cada bloco liga ao seguinte por "mas" ou "então", nunca por "e aí".
- **Novos ganchos:** a cada 60–90 s.
- **Tamanho:** um vídeo longo tem de 3 a 5 casos. Mais que isso vira lista.

## Estrutura do Short (45–75 s)

1. **0–2 s:** a imagem mais forte e a frase do gancho juntas (contradição ou pergunta).
2. **2–10 s:** quem, onde, quando, em uma frase, com a cena na tela.
3. **10–40 s:** 2 ou 3 provas rápidas, uma por frase, cada uma com sua imagem.
4. **40–55 s:** a virada: "só que…", o aparte do Nox ou a comparação.
5. **55–70 s:** o payoff em até 6 palavras, que responde o gancho.
6. **Fim:** uma pergunta que faça a pessoa comentar. Se possível, a última frase conversa com a primeira para o vídeo rodar em loop.

## Frases

- Uma ideia clara por frase, com períodos e pausas naturais. Dividir quando a compreensão pedir, sem limite obrigatório de palavras para acompanhar cortes visuais.
- Concreto antes de abstrato: o nome, a edição, a cena, o número, e só então o conceito.
- Palavra de impacto no fim da frase: é ela que vira o destaque na tela.
- Voz do canal: conversada, opinativa, irônica. Humor que nasce do assunto. Sem locução épica, bordões ou "e é aí que tudo muda" repetido.
- Separar fato da obra, interpretação e opinião ("na HQ, ele…", "pra mim, isso mostra…").

## Formato de entrega (pronto para a montagem)

No Content Lab, usar `creative_write` com `script.chapters`. Seguir a organização audiovisual do **VD_0008 — Carnificina** como referência de estrutura: packaging antes, capítulos temáticos, fala que prepara um trecho, trecho com áudio próprio sem narrador e retorno da fala que interpreta ou avança. Preservar essa lógica sem copiar o texto nem impor um número fixo de capítulos. Trechos de cena costumam ter 3–7 s, conforme a função e o material; estimativas não são timecodes verificados.

Cada capítulo tem `id`, `title` e `blocks`. Cada bloco tem `id`, `type`, `title` e `text`:

- `narration`: somente texto falado. Pode conter vários períodos e parágrafos conversacionais. Nunca incluir rótulo NARRAÇÃO, título de capítulo, nota de produção ou descrição da cena dentro de `text`.
- `scene`: descrição da cena com áudio original ou desenho sonoro, sem narrador. Informar a função narrativa, obra/trecho pretendido, duração estimada e som; não inventar diálogo, timestamp ou direitos.
- `direction`: imagem, enquadramento, movimento, Nox, texto na tela, efeitos e alternativas de edição; não é falado.

Títulos de capítulo/bloco e `script.sources` ficam fora da voz. A IA gera um take por bloco `narration`, na ordem dos capítulos e blocos. Ao gravar, o criador vê somente essas falas agrupadas por capítulo; o título orienta, mas não é lido. A montagem gera automaticamente a transcrição palavra por palavra com Whisper `large-v3` completo; a edição usa os tempos reais consultados em `narration_transcript`. Os blocos de cena e direção são preservados para a edição e no roteiro do kit; não viram fala. No Google Doc, manter os rótulos e estilos do template, com a mesma ordem de capítulos e blocos.

Para ajustar uma parte, usar `script_get` e `script_edit` com `baseRevision` atual e operações por IDs. Acrescentar, remover, renomear e mover capítulos/blocos, inclusive blocos entre capítulos, sem recriar os IDs do conteúdo preservado. `beforeId` indica posição; sem ele, inserir no fim. Validar com `dryRun` quando necessário e reler após conflito. Ferramentas e conexão: `../../diazverso-contentlab/SKILL.md`.

Um bloco `scene` descreve a intenção editorial: não seleciona clipe, não insere áudio original nem abre pausa automaticamente na composição. A IA precisa conferir os materiais e a execução na edição antes de certificar o audiovisual. Notas visuais orientam `motion_plan_set`; escolher as cenas do kit pela função, com mídia da obra como base e Nox nos apartes.

## Conferência rápida

- A abertura é uma das três ("Imagina…", teste direto ou premissa absurda) e mostra o assunto nos primeiros 3 segundos?
- A promessa é contável e aparece como mapa na tela?
- Os casos vão do mais fraco ao mais forte, cada um com situação, escolha, consequência e o que revela?
- Há contraponto?
- Cada bloco tem "mas" ou "então" ligando ao próximo?
- Há um novo gancho a cada 60–90 s?
- Toda afirmação sobre a obra tem uma mídia correspondente?
- O payoff responde exatamente o que o título e o gancho prometeram?
- Lido em voz alta, soa como conversa?
