---
name: diazverso
description: "Ponto de entrada obrigatório do Diazverso. Use em qualquer pedido sobre o canal Diazverso ou seus vídeos: ideia, pauta, roteiro, título, thumbnail, narração, edição, motion, Nox, Shorts, Content Lab, revisão ou retomada de produção. Define as regras do canal, o fluxo e qual skill abrir."
---

# Diazverso: regras do canal

O Diazverso é um canal brasileiro centrado em super-heróis, com obras afins como Dragon Ball e possibilidades de grandes acontecimentos e ensino aplicado à vida real conforme a [identidade editorial](../diazverso-core/SKILL.md) e seus formatos. Estas regras são o gosto do criador e valem desde a primeira mensagem, mesmo sem conhecer quem pede. Só mudam por pedido explícito do criador. Pergunte apenas o que falta para avançar.

Shorts têm somente título A e thumbnail A (9:16), sem teste A/B. Título B e thumbnail B ficam vazios no Content Lab, no Drive e na planilha. Duas variantes A/B são exclusivas dos vídeos longos.

## Regras inegociáveis

1. **Contexto enxuto.** Uma skill principal por vez, escolhida pela tabela abaixo, e só as referências da próxima ação. Não reler o que já foi lido nesta sessão. Resumir saídas longas. Ao trocar de etapa, manter um checkpoint curto: produção, decisões, feito, bloqueios e próxima ação.
2. **Content Lab é o caminho padrão para produzir.** Na primeira produção da sessão, conferir se o MCP do Content Lab responde (`contentlab_status`). Se não estiver conectado, perguntar "Vamos usar o Content Lab?" e conectar seguindo `../diazverso-contentlab/SKILL.md`. Ao criar ou retomar o projeto, abrir no navegador do criador (`contentlab_open`) para ele acompanhar. Produzir fora dele só quando o criador recusar.
3. **Combinar o fluxo uma vez, numa pergunta só**, antes de criar o projeto:
   - **Tudo automático:** a IA faz tudo e avisa no fim.
   - **Parar em pontos:** a IA para, avisa o que revisar no Content Lab e espera o botão **Aprovar e seguir** do app (ou o ok no chat). Sugestão: roteiro, narração e revisão final.
   - **Aprovar cada etapa.**
   - **Voz:** voz de IA ou o criador grava a própria voz no Content Lab.
   - **Drive e planilha:** se as ferramentas Google não responderem, perguntar se o criador quer conectar ou seguir sem elas. Sem elas, nada é gravado no Drive; no fim, o kit traz o que subir e as linhas prontas para ele preencher à mão ([modo manual](../diazverso-drive-setup/references/modo-manual.md)).
4. **Ordem da produção** (nenhuma etapa é pulada):
   1. tema polêmico, que ensina algo ou que desperta curiosidade, e a tese pesquisada;
   2. título e thumbnail, antes do roteiro (o roteiro cumpre o que eles prometem);
   3. roteiro na estrutura do canal (`../diazverso-roteiro/references/escrita.md`): gancho, prova e promessa contável, casos, contraponto, payoff e pergunta, capítulos e blocos de narração, cena/som original e direção visual; só a fala vai à voz;
   4. revisão de fatos, estrutura e voz;
   5. aprovação;
   6. cenas das obras com direitos;
   7. narração (somente falas, por capítulo) e, com o áudio final definido, a transcrição Whisper `large-v3` completo, palavra por palavra, conferida (sem frase repetida nem buraco); consultar os tempos reais em `narration_transcript` antes da edição;
   8. plano de motion;
   9. prévias;
   10. enviar o render à fila e encerrar a resposta; revisão do arquivo e entrega são retomadas quando o criador voltar ao chat;
   11. thumbnail final no [modelo do canal](../diazverso-thumbnail/references/modelo-palavra.md): palavra atravessando o personagem com halo escuro (preenchimento brilhante atrás, contorno na frente), fundo simples de TV e Nox muito grande no canto, focado na cabeça, acima de tudo;
   12. kit de publicação manual (com o registro manual do Drive e da planilha, quando não houver acesso);
   13. Shorts cortados do vídeo longo: trechos que funcionam sozinhos, em 9:16, com a mesma edição e fechando na chamada para o vídeo completo ([Shorts](../diazverso-shorts/SKILL.md)). Short do zero só quando o criador pedir.
5. **Edição = motion design do kit do Content Lab** (`../diazverso-motion/SKILL.md`). O Content Lab é neutro: o Nox entra em cada projeto importando o pacote `assets/brand/nox/` deste plugin com `character_import`, antes do plano de motion:
   - **Ritmo:** troca de informação a cada 1,5–3 s, no ritmo do RunnyIA, com a câmera nunca parada.
   - **Visual:**
     - estética HQ madura: estrelas, halftone, fundos escuros e explosões gráficas; fundo de papel e página decorativa não fazem parte da edição. Imagens reais de páginas de quadrinhos continuam permitidas como conteúdo;
     - Anton em títulos e legendas;
     - a cena da obra é a base, muitas vezes sozinha em tela cheia;
     - abertura com a arte mais bonita do personagem em alta resolução e 5–6 cortes nos primeiros 5 s;
     - o Nox em opinião e humor, a cada 10–20 s (no Short, a cada 6–10 s): aparte (cena desfocada, Nox inteiro subindo pela borda de baixo) gesticulando em stop motion: a pose troca enquanto ele fala, a cada 0,7–1 s, com poses do [catálogo](../diazverso-nox/references/poses.md) escolhidas conforme a narrativa, sem obrigação de usar todas;
     - fundos, cores e cenas sempre variando, nunca iguais em seguida;
     - caixinhas HQ de lembrete (inscreva-se, like, opinião, spoiler) e recortes PNG do que está sendo falado;
     - cena da obra sempre que a fala citar algo; ela é a base do vídeo; cada imagem conferida aberta (mostra o que a fala diz, em resolução suficiente);
     - **Cena / som original = vídeo real da obra com seu áudio original**, com ação ou diálogo e a narração pausada: 2–3 trechos curtos em falas marcantes no longo. Painel de HQ, foto, frame congelado, slideshow ou imagem com zoom/parallax, trilha ou SFX não contam como cena original e nunca ocupam esse intervalo. Imagens e painéis entram durante a narração; vídeos de apoio também podem entrar durante a narração, mas com o áudio da obra mudo. Selecionar trechos pertinentes à fala, sem apresentador, react, rosto ou narração do criador do upload: somente a cena da obra. Buscar primeiro a mesma cena **dublada em português brasileiro**, com a dublagem da obra. Se só houver o trecho necessário em inglês, manter o áudio da cena e traduzir todas as falas em **caixinhas/balões HQ curtos que aparecem e trocam conforme o personagem fala**, com Anton, posição legível e sem cobrir a ação; nunca uma frase longa inteira parada. Conferir transcrição, tradução e tempos reais; seguir a [montagem das traduções](../diazverso-motion/SKILL.md#tradução-das-cenas-com-som-original). Identificar a adaptação quando ela difere da HQ e nunca usá-la como prova de um acontecimento exclusivo de outra continuidade. Sem vídeo pertinente com áudio e direitos conferidos, manter a pendência ou a narração, sem substituir por imagem com música;
     - no vídeo longo, tela final de 15–20 s depois da última fala, só com a trilha;
     - Shorts em 9:16 no mesmo padrão e no mesmo nível do vídeo longo, com o Nox constante ([padrão de edição](../diazverso-motion/references/padrao-de-edicao.md)).
   - **Som:**
     - SFX no quadro de cada evento da tela, variando, sem cobrir a fala; sons novos sintetizados ou do Openverse com licença comercial ([som](../diazverso-motion/references/som.md));
     - legenda palavra a palavra: o tempo todo nos Shorts; no vídeo longo, só em trechos (gancho e apartes do Nox). A tradução de cenas em inglês é obrigatória também no longo e segue as falas da cena;
     - trilha licenciada abaixando sob a voz, mas audível do começo ao fim; SFX abaixo da voz, explosão mais baixa ainda.
   - **Proibido:**
     - texto sobre fundo liso como cena;
     - clips estáticos colados;
     - componentes TSX escritos do zero quando o kit tem a cena.
6. **Escrita:**
   - **Voz:** conversada, opinativa, irônica e bem-humorada.
   - **Formato:** desenvolver a tese/pergunta em ciclos de curiosidade e resolução, com exemplos e evidências que fazem o argumento avançar; ensinar ou revelar algo através de histórias, personagens, obras e acontecimentos ([formatos](../diazverso-core/references/formatos-editoriais.md)).
   - **Abertura:** gancho no primeiro segundo, sem "hoje vamos falar".
   - **CTAs obrigatórias:** no vídeo longo, incluir pelo menos duas chamadas curtas e naturais durante o desenvolvimento, depois de entregar valor, distribuindo convites para se inscrever, dar like e comentar sem interromper uma prova ou cena importante. No encerramento, convidar explicitamente a se inscrever e dar like, indicar outros vídeos reais e relacionados do canal com uma razão concreta para assistir e terminar a última fala exatamente com **"falou"**. Depois dessa palavra, somente a tela final e a trilha, sem nova fala. No Short, usar uma CTA curta compatível com a duração, manter a chamada para o vídeo completo e terminar a fala com **"falou"**; não concentrar vários pedidos a ponto de prejudicar o corte.
7. **Nunca:**
   - publicar, agendar ou enviar vídeos (o criador publica);
   - inventar fatos ou falas canônicas;
   - usar mídia sem direitos ou música sem licença (o canal é monetizado);
   - redesenhar o Nox (`assets/brand/nox/Nox.png` é a fonte);
   - prometer CTR ou retenção.
8. **Verificar de verdade.** Abrir frames, medir o áudio e ler de volta o que foi gravado. Não declarar pronto o que não foi conferido.
9. **Render é envio à fila e fim da resposta.** A aba **Fila de processamento** do Content Lab reúne render, transcrição, voz de IA e montagem WAV de todos os projetos e executa um trabalho por vez, na ordem de envio. Na Edição/Revisão aparece só o render atual ou o último; o histórico fica na fila. Depois de `render_start` confirmar o envio, avisar brevemente "Já coloquei o vídeo na fila de renderização do Content Lab" e encerrar o turno, inclusive no modo automático. Não esperar, usar `job_wait` para render, consultar porcentagem repetidamente, dormir para acompanhar, criar monitor ou prometer retorno automático. O app renderiza em segundo plano; o criador volta ao chat quando quiser retomar. Só nessa nova interação consultar o estado e, se concluído, revisar o arquivo e seguir para a entrega. Se ainda estiver renderizando, informar e encerrar novamente; se o envio falhar, informar a falha sem declarar que entrou na fila.

## Qual skill abrir

| Pedido | Skill |
| --- | --- |
| Produzir um vídeo do começo ao fim, conectar o Content Lab, ou retomar | diazverso-contentlab (com o Content Lab) ou diazverso-criacao-video (sem ele, retomada, kit de publicação) |
| Pauta, tese, pesquisa | diazverso-pesquisa |
| Títulos | diazverso-titulos |
| Thumbnail | diazverso-thumbnail |
| Roteiro | diazverso-roteiro |
| Revisão de embalagem, fatos, estrutura, voz e aprovação | diazverso-revisao |
| Edição, motion, som, legenda | diazverso-motion |
| Decupar em beats, revisar o render | diazverso-decupagem |
| Buscar cenas e mídia das obras | find-broll |
| Nox, poses, expressões, Nox 3D | diazverso-nox |
| Shorts | diazverso-shorts |
| Identidade e linguagem | diazverso-core |
| Drive e Sheets | diazverso-drive-setup |
| Mudar o plugin | diazverso-manutencao |

Pedidos com várias etapas seguem a ordem da produção e abrem só a skill da próxima etapa.
