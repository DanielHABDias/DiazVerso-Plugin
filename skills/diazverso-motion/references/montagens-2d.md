# Montagens e transições 2D do Diazverso

Consultar `motion_kit` para o contrato vigente, exemplos e SFX. O Content Lab usa nomes genéricos de personagem; no canal, importar o pacote do Nox por `character_import` antes de usar as três cenas de personagem. Estas cenas usam corte, escala, máscara, cor e PNGs prontos. Não articulam, deformam, redesenham ou interpolam membros do Nox; a pose muda inteira por corte seco. As aproximações são sobre imagens planas, sem reconstrução 3D da obra.

## Escolher pelo argumento

| Cena | Uso no canal |
| --- | --- |
| `montagemEncaixe` | Reunir situações concretas antes de aprofundar a última; não sugerir simultaneidade se a obra não a estabelece. |
| `enquadramentoAlternado` | Comparar adaptações, momentos ou representações; alinhar os rostos com foco/zoom e identificar as obras. |
| `detalheContexto` | Sair de uma expressão ou elemento pequeno para seu contexto; não ampliar além da resolução disponível. |
| `janelaMovel` | Contrastar situações relacionadas; evitar passar a faixa sobre uma informação que ainda precisa ser lida. |
| `faixasSequenciais` | Acompanhar até três ações; escolher trechos em que o recorte preserve a ação e o rosto. |
| `fotogramasMudanca` | Mostrar transformação visual por imagens verificadas; ordenar as fontes pela cronologia real. |
| `anotacaoCena` | Apontar algo de fato visível na obra; conferir a marca no frame congelado, sem inventar detalhes. |
| `retornoImagem` | Retomar uma imagem já apresentada; contextualizar a lembrança e voltar ao argumento atual. |
| `palavraRecortada` | Destacar um conceito por trás do personagem da obra; recorte deve ter transparência verdadeira e direitos conferidos. |
| `personagemPrimeiroPlano` | Nox comenta enquanto a evidência continua visível; importar o pacote e alternar poses por sentido. |
| `personagemReacao` | Nox reage depois de um acontecimento; entrada e saída por corte, sem animar o corpo ou os membros. |
| `personagemAlternado` | Nox apresenta uma observação, a obra demonstra, Nox conclui em outra pose; reservar cada corte à fala correspondente. |
| `legendaVirada` | Reformular uma impressão ou opinião; o texto é comentário editorial e não deve parecer fala canônica. |
| `divisaoResolvida` | Comparar duas situações e aprofundar uma; expandir não significa declarar um vencedor. |
| `corteCor` | Trocar de assunto com transição breve; usar as cores do canal e evitar efeito chamativo em cena emocional. |
| `revelacaoRecortes` | Introduzir uma imagem por fragmentos grandes e depois deixar a obra tocar; não ocultar prova essencial por suspense. |

## Entradas e montagem

Cada fonte é um objeto `{ midia: "media:<id>", inicio, titulo?, fonte?, foco?, zoom?, deslocamento? }`. `inicio` é em segundos da mídia, nunca em fração do beat. Os clipes ficam mudos sob a narração. `foco` segue `object-position`, por exemplo `50% 25%`; `zoom` ajuda a alinhar enquadramentos. `deslocamento: { x,y }` ajusta a posição por frações do quadro, com zero no alinhamento original. Reenquadrar as fontes e as marcas separadamente para cada proporção de vídeo. Páginas de HQ são conteúdo da obra, não fundo decorativo.

**`montagemEncaixe` — Montagem por encaixe.** Recortes diagonais com bordas de tinta e contorno azul ou vermelho entram em sequência; o último cresce até tela cheia e o contorno desaparece na ampliação. `cenas`: 2–4 itens { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }.

**`enquadramentoAlternado` — Mesmo enquadramento, outra versão.** Cortes secos alternam imagens ou vídeos alinhados, com rótulo e foco configurável por fonte. `cenas`: 2–4 itens { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `ordem`: até 8 índices de cenas; padrão 0,1,...; intervalos iguais. Ajustar foco e zoom de cada fonte para alinhar..

**`detalheContexto` — Detalhe e contexto.** Começa ampliado em um ponto da imagem e abre até mostrar a imagem inteira; círculo preserva a referência. `cena`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `detalhe`: { x, y, w?, h? }: frações 0–1 da imagem fonte, sem corte; padrão centro. Usar imagem com dimensões conhecidas.; `zoom`: ampliação inicial, padrão 2,3; foco escolhido deve ter resolução suficiente.

**`janelaMovel` — Janela móvel.** Uma faixa revela outra mídia ao atravessar o quadro; abre até completar a troca. `antes`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `depois`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }.

**`faixasSequenciais` — Sequência em faixas.** Até três fontes dividem a tela; a faixa ativa expande e toca, enquanto as outras congelam e escurecem. `cenas`: 2–3 itens { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; a duração é dividida igualmente entre as fontes.

**`fotogramasMudanca` — Fotogramas de uma mudança.** Três imagens congeladas entram sobrepostas e deslocadas; a última preenche o quadro. `cenas`: 2–3 itens { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; usa primeiro frame de cada inicio, mesmo se for vídeo.

**`anotacaoCena` — Cena com anotação pontual.** Vídeo pausa em um frame escolhido, recebe marca localizada e retoma do mesmo frame. `cena`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `em`: fração do beat, padrão 0,32; `pausa`: fração do beat, padrão 0,35; não é segundo; `ponto`: { x, y, w?, h? } em frações 0–1 do quadro já recortado, conferido no frame da pausa; `marca`: circulo (padrão) | seta | sublinhado; `texto`: observação curta opcional.

**`retornoImagem` — Retorno de uma imagem.** Intercala uma lembrança breve em tela cheia; a fonte atual pausa durante o retorno e continua depois. `atual`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `lembranca`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `em`: fração do beat, padrão 0,35; `duracao`: fração do beat reservada à lembrança, padrão 0,2.

**`palavraRecortada` — Palavra atrás do personagem.** Palavra grande entra entre a obra de fundo e um recorte PNG transparente, sem modificar a figura. `cena`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `recorte`: media:<id> de PNG realmente transparente, fornecido pelo projeto; `palavra`: palavra curta; evitar frases longas.

**`personagemPrimeiroPlano` — Nox em primeiro plano.** PNG grande de um lado e obra do outro, separados por divisória inclinada; troca de poses a cada 0,8 s. `cena`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `poses`: nomes do pacote importado, alternados a cada 0,8 s; `humor`: humor para seleção de pose se poses não for informado; `texto`: frase curta opcional; exige character_import.

**`personagemReacao` — Nox com reação atrasada.** O personagem entra e sai por corte, depois do acontecimento; troca de PNG no meio da reação. `cena`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `poses`: dois nomes do pacote importado; `humor`: padrão surpreso; `texto`: comentário curto opcional; `em`: entrada como fração do beat, padrão 0,28; `ate`: saída como fração do beat, padrão 0,83; exige character_import.

**`personagemAlternado` — Nox e evidência alternados.** Personagem em destaque, corte para obra em tela cheia, retorno em outra posição e pose. Sem transição de corpo. `cena`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `poses`: nomes do pacote importado para troca seca a cada 0,8 s; `humor`: padrão determinado; `texto`: frase curta opcional; exige character_import.

**`legendaVirada` — Legenda que muda de sentido.** Mesma mídia, expressão curta com palavra riscada e substituída no instante da virada. `cena`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `prefixo`: início da frase, opcional; `antes`: palavra ou expressão inicial; `depois`: substituição; `sufixo`: fim da frase, opcional; `virada`: fração do beat, padrão 0,42; reservar ao menos 18% para mostrar a correção.

**`divisaoResolvida` — Quadro dividido que se resolve.** Duas fontes em tela dividida; a divisória se desloca até a escolhida preencher o quadro. `cenas`: dois itens { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `escolhida`: índice 0 ou 1; padrão 1; `virada`: fração em que a divisória começa a mover, padrão 0,33; reservar 45% da duração.

**`corteCor` — Corte por cor.** Faixa diagonal com cor do kit atravessa rapidamente o quadro e revela a próxima mídia. `antes`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `depois`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }; `tom`: cor da faixa; padrão vermelho.

**`revelacaoRecortes` — Revelação por recortes.** Quatro partes grandes revelam o frame inicial; depois a mídia completa começa a tocar. `cena`: { midia: media:<id>, titulo?, fonte?, inicio?: segundos, foco?: object-position, zoom?: número }.

## Tempos e continuidade

- `montagemEncaixe`: entradas em 0%, 16%, 32% e 48%, conforme a quantidade; último amplia entre 78% e 99%. Para continuar o último, usar seu `inicio` + tempo desde a entrada dele, sem reiniciar a fonte.
- `enquadramentoAlternado`: a ordem divide o beat em intervalos iguais. Cada corte começa no `inicio` da fonte correspondente. Comparação alinhada depende da escolha e do ajuste das imagens, não de reconhecimento automático de rosto.
- `detalheContexto`: a abertura do contexto acontece entre 15% e 78%. `detalhe` usa coordenadas da imagem inteira, exibida com contain; a marca acompanha o mesmo ponto. Usar fontes com dimensões conhecidas. Não misturar essas coordenadas com as de `anotacaoCena`.
- `janelaMovel`: percurso entre 3% e 62%; expansão entre 58% e 97%. As duas fontes avançam desde o início do beat.
- `faixasSequenciais`: cada faixa tem um intervalo igual. Antes de ativar, exibe o frame inicial; depois do seu intervalo, fica congelada no último frame exibido. As faixas mudam de largura no horizontal e de altura no vertical.
- `fotogramasMudanca`: imagens entram em 0%, 20% e 40%; o último cresce entre 79% e 99%. Cada fonte fica no primeiro frame do seu `inicio`.
- `anotacaoCena`: `em` e `pausa` são frações do beat. A fonte congela no instante `em`, a marca aparece e, ao terminar a pausa, a reprodução retoma desse mesmo frame. `ponto` usa o quadro já recortado: conferir posição antes de editar o resto.
- `retornoImagem`: a fonte atual pausa durante a lembrança e retoma do mesmo ponto, sem saltar conteúdo. Ao continuar no beat seguinte, descontar da fonte atual a duração da lembrança.
- `palavraRecortada`: palavra e recorte entram entre 6% e 23%. Escolher palavra curta que não repita o que o público acabou de ler; conferir se o recorte deixa parte suficiente das letras visível.
- `personagemPrimeiroPlano`: Nox troca PNG a cada 0,8 s, sem mover partes do desenho. A cena da obra segue ao lado; os olhos e a ação devem continuar legíveis.
- `personagemReacao`: Nox aparece em `em` (padrão 28%), troca para o segundo PNG no meio do intervalo e sai em `ate` (padrão 83%). Sem tween de entrada, saída ou corpo. Duas poses precisam representar a reação da fala.
- `personagemAlternado`: Nox entre 0% e 25%, evidência entre 25% e 62%, Nox novamente entre 62% e 100%. Durante a evidência a fonte começa em seu `inicio`; nos intervalos do Nox os PNGs trocam a cada 0,8 s. Ajustar duração do beat para as falas coincidirem com os cortes.
- `legendaVirada`: `virada` padrão em 42%; durante os próximos 18% o texto anterior aparece riscado junto à substituição. Depois fica só a frase corrigida. Preferir uma palavra ou expressão curta em cada campo.
- `divisaoResolvida`: padrão começa a expansão em 33% e termina em 78%. As duas fontes avançam desde o início do beat. Para continuar a escolhida, somar a duração inteira do beat ao `inicio` dela.
- `corteCor`: a faixa atravessa entre 25% e 71%. A segunda fonte começa em 25%; para continuar, somar 75% da duração do beat ao `inicio` dela. Usar em beat curto, com troca pertinente ao argumento.
- `revelacaoRecortes`: quatro fragmentos entram em 0%, 17%, 34% e 51%. O clipe completo começa em 72% e termina de aparecer em 90%. Para continuar, somar 28% da duração do beat ao `inicio` da fonte.

## Revisão do canal

Usar Anton, contorno de tinta discreto, estrelas, meio-tom e as cores do kit. Evitar sobreposição decorativa, textos longos e repetição da mesma transição. O Nox do plugin permanece com olhos amarelos sólidos, sem pupilas ou íris; qualquer mudança de expressão vem do PNG escolhido. Os recortes das obras também precisam corresponder ao argumento.

Ler `som.eventos` no catálogo e recalcular os eventos com `narrativeEvents` conforme duração, props e fps reais. Gravar a saída no `sfx` do beat: `camera` para entrada de fonte, `swish`/`whoosh` para troca, `pop` para entrada do Nox, `tick` na anotação e `type` na correção de texto. Não há áudio original embutido nessas cenas; a pausa de vídeo de `anotacaoCena` não pausa a narração. Um trecho com som original continua seguindo o fluxo de `evidencia` + pausa de narração.

No longo, usar legenda em comentários falados do Nox e no gancho; nos Shorts, o tempo todo. Conferir 16:9 e 9:16: olhos, marcações, texto e ação dentro das áreas úteis. O corpo pode ser cortado pela borda; não cortar o rosto para encaixar um texto. Para passagens temporais, conferir o frame de saída e de retorno, não apenas uma imagem representativa.
