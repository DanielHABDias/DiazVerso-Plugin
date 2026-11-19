# Direção narrativa com as cenas do Content Lab

Ler `motion_kit` para nomes, props, exemplos e eventos de som vigentes. O Content Lab implementa as cenas; este guia só decide quando usá-las no canal. A obra continua sendo a evidência visual, com fonte e continuidade identificadas.

| Cena | Quando usar no Diazverso | Cuidado editorial |
| --- | --- | --- |
| `dossie` | Cruzar relatos, painéis e pistas de um mistério | Separar suspeita, hipótese e prova; Nox investigativo apenas quando há investigação |
| `cronologiaRamos` | Explicar o evento que separa continuidades ou origens | Nomear as linhas; sequência sem ramificações usa a linha do tempo existente |
| `revelacaoCamadas` | Desmontar a versão aparente até chegar à causa | A revelação precisa de fonte; não esconder uma informação essencial só por efeito |
| `contradicao` | Mostrar a distância entre o que alguém diz e o que faz | Uma prova que realmente contradiz; Nox desconfiado ou julgando em aparte pertinente |
| `efeitoDomino` | Acompanhar o custo de uma decisão nas próximas ações | Relação causal demonstrável, não só eventos consecutivos |
| `constelacao` | Reunir limite, custo, escolha e legado numa tese | Conexões simultâneas; não repetir o percurso de BrainstormHQ |
| `quadrosProfundidade` | Ler contexto, ação e detalhe em planos sobrepostos | Travelling lateral; o voo por casos continua sendo `paineis3d` |
| `lupaEvidencia` | Apontar um gesto, inscrição ou detalhe de um painel | Usar a mesma imagem; conferir coordenadas e resolução; não inventar detalhe por ampliação |
| `bifurcacao` | Explicar uma decisão e sua alternativa | Contrafactual deve ser rotulado como hipótese |
| `limiar` | Tornar visível o limite de um poder ou de uma pressão | Fonte ou rótulo simulação; não converter opinião em dado |
| `balancaCusto` | Discutir o ganho de poder e a perda pessoal | Pesos são avaliação editorial, explicitamente identificada |
| `ecoVisual` | Comparar o retorno de um motivo entre histórias | Nomear obras, datas e continuidades; recorrência não prova intenção do autor |
| `pecaAusente` | Mostrar por que uma explicação ainda não fecha | `revelar: false` se não há prova da peça que falta |
| `convergencia` | Levar investigação, ameaça e decisão ao mesmo encontro | As frentes avançam em paralelo; não confundir com causa em cascata |
| `vinculo` | Acompanhar confiança, conflito e ruptura entre duas pessoas | A virada deve corresponder a um acontecimento sustentado pela obra |
| `memoria` | Voltar a uma promessa ou relação anterior e retornar ao presente | Identificar as duas cenas; a lembrança não altera a cronologia canônica |
| `duplaVida` | Alternar vida pessoal e responsabilidade heroica | Usar as cenas correspondentes; foco visual não define um vencedor |
| `trilhaViva` | Navegar por capítulos, entrar na obra e retornar à linha do tempo | Reutilizar a mesma lista; `de` e `ate` começam em 1. Usar eventos reais, sem inventar causalidade |
| `personagemClose` | Nox ampliado, com balão de texto/ícone, para opinião, explicação e humor | Importar Nox; preservar o PNG e olhos sem pupilas. Escolher poses para a fala e dar 0,7–1 s por ideia |
| `pensamentoVivo` | Expor dois ou três pensamentos simultâneos ao redor do Nox grande | Balões surgem e permanecem; não substituir cenas da obra por conceitos genéricos |
| `rasgoCena` | Revelar outra cena da obra por um rasgo gráfico discreto | Usar em viradas pertinentes; as mídias tocam mudas sob a voz, sem imitar uma cena com som original |

As montagens por recorte, enquadramentos, faixas, anotações, retornos, cenas do Nox e transições de texto/cor estão no [guia de montagens e transições 2D](montagens-2d.md), com os nomes exatos das cenas e seus tempos.

## Como montar as cenas expressivas

**Linha do tempo navegável (`trilhaViva`).** `capitulos` recebe uma lista ordenada de `{ titulo, midia: "media:<id>", inicio, rotulo?, fonte? }`, com quantos capítulos a história pedir. `inicio` é em segundos da fonte. Repetir a mesma lista nos beats que retomam esse percurso; só os capítulos próximos da câmera são desenhados.

Cada beat faz um movimento: `de` e `ate` são capítulos numerados a partir de 1. `entrar: true` mergulha no capítulo `ate` até tela cheia e sua mídia toca; `sair: true` começa dentro do capítulo `de` e retorna à linha. `ate < de` rebobina, com escurecimento, indicador de retorno e linhas de fita. Por exemplo, ir de 1 a 3 com `entrar: true`; depois de mostrar a obra, voltar de 3 a 2 com `sair: true, entrar: true`, conservando a lista de capítulos. A quantidade de capítulos não obriga uma quantidade fixa de casos no roteiro.

Para continuar em `evidencia` sem reiniciar o vídeo, usar a mesma mídia e `cheia: true`. Calcular `inicio` seguinte = `inicio` do capítulo + (frames do beat − frame da entrada) / fps. O cronograma vigente é `timelineSchedule(props)` em `src/motion/kit/narrative/trilha.js` do Content Lab: a entrada começa em `enterStart × (frames − 1)` (fração 0,68). Conferir o frame efetivo e o enquadramento. Se houver áudio original na continuação, prever pausa na narração e tradução. `fragmentos` e `mergulhar` são compatibilidade com planos antigos; para novos planos, usar `capitulos`, `de`, `ate`, `entrar` e `sair`.

**Nox em close (`personagemClose`).** Requer o pacote do Nox importado. `ideias` contém `{ texto?, icone?, pose?, humor? }`; a duração divide-se igualmente entre até seis itens. Usar nomes de poses do catálogo, com troca seca a cada 0,7–1 s da fala. `poses` pode listar gestos para alternar a cada 0,8 s independentemente do balão; sem essa lista, `pose` de cada ideia fixa o gesto ou `humor` escolhe as poses. `lado` escolhe esquerda/direita no horizontal; `midia` e `inicio` opcionais colocam a obra desfocada atrás. O PNG é ampliado e o corpo recortado pela borda: não desenhar olhos ou modificar proporções.

**Pensamentos (`pensamentoVivo`).** `ideias` aceita até três `{ texto?, icone? }` e `poses` lista gestos do catálogo; a pose muda a cada 0,8 s. `conclusao` é uma frase curta opcional, revelada em 76% do beat. Os balões entram em 8%, 27% e 46%. Usar ícones válidos do kit, por exemplo `raio`, `relogio`, `coracao`, `escudo` ou `interrogacao`.

**Rasgo (`rasgoCena`).** `antes` e `depois` são referências de mídia. `inicioAntes` e `inicioDepois` apontam os trechos nas fontes; a segunda começa a tocar na `virada` (fração do beat, padrão 0,35, limitada entre 0 e 0,58). O rasgo leva 42% do beat e termina com a segunda mídia em tela cheia. A continuidade seguinte usa `inicioDepois` + tempo entre a virada e o fim do beat, conferido no frame.

**Som e legenda.** Ler os exemplos e `som.eventos` em `motion_kit`; as frações são exemplos para 4 s. O utilitário `narrativeEvents` do Content Lab recalcula eventos conforme props, duração e fps; colocar a saída no `sfx` do beat. Na linha do tempo, passagens, retorno e entrada seguem o mesmo cronograma da câmera. O helper reduz a densidade para cerca de um SFX por segundo, priorizando `impact`, `error` e `sub`, com espaço entre sinais; não repor manualmente um som em toda entrada. Balões podem usar `pop`, conclusão `ding`, rasgo `whoosh`, conforme os eventos mantidos. No longo, os dois formatos de Nox contam como apartes para legenda (`legenda: true`); nos Shorts a legenda continua durante todo o vídeo. Conferir áreas seguras e evitar balão sobre os olhos.

## Compor no estilo do canal

- Usar Anton e as cores do kit; preferir Half-Tone (`halftone`) e meio-tom (`meio-tom`), alternando com estrelas, escuro e explosões gráficas. Os fundos de papel amassado disponíveis no kit não são a base estética do canal; não usar página decorativa como fundo. Imagens reais de páginas de HQ podem ser conteúdo das mídias.
- Associar cada entrada ao tempo real da fala. Se a cena precisar de vários passos legíveis, dar tempo a cada um ou dividir o beat; não despejar todo o texto.
- Usar `media:<id>` com os painéis e cenas citados; o motion organiza o argumento. Alternar com a obra sozinha em tela cheia.
- Traduzir `som.eventos[].fracao` do catálogo para `sfx[].at` em segundos do beat. Mover o som quando mudar `virada`; não tocar evento de uma etapa ausente. Rever som abaixo da voz.
- Nox é importado por projeto, nunca embutido no aplicativo. Poses especiais seguem a narrativa; não há obrigação de usar todas. Reação silenciosa pode ficar imóvel; a troca de pose acompanha fala quando houver fala.
- Verificar abertura, virada e conclusão, tanto em 16:9 como em 9:16. Conferir texto, foco da mídia, transparência e correspondência com a narração antes de renderizar.
