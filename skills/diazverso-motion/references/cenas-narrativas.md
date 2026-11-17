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

## Compor no estilo do canal

- Usar Anton e as cores do kit; estrelas, halftone, escuro ou explosões gráficas. Nada de papel ou página decorativa como fundo. Imagens reais de páginas de HQ podem ser conteúdo das mídias.
- Associar cada entrada ao tempo real da fala. Se a cena precisar de vários passos legíveis, dar tempo a cada um ou dividir o beat; não despejar todo o texto.
- Usar `media:<id>` com os painéis e cenas citados; o motion organiza o argumento. Alternar com a obra sozinha em tela cheia.
- Traduzir `som.eventos[].fracao` do catálogo para `sfx[].at` em segundos do beat. Mover o som quando mudar `virada`; não tocar evento de uma etapa ausente. Rever som abaixo da voz.
- Nox é importado por projeto, nunca embutido no aplicativo. Poses especiais seguem a narrativa; não há obrigação de usar todas. Reação silenciosa pode ficar imóvel; a troca de pose acompanha fala quando houver fala.
- Verificar abertura, virada e conclusão, tanto em 16:9 como em 9:16. Conferir texto, foco da mídia, transparência e correspondência com a narração antes de renderizar.
