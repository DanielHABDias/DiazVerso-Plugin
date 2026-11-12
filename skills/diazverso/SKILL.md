---
name: diazverso
description: "Ponto de entrada obrigatório do Diazverso. Use em qualquer pedido sobre o canal Diazverso ou seus vídeos: ideia, pauta, roteiro, título, thumbnail, narração, edição, motion, Nox, Shorts, Content Lab, revisão ou retomada de produção. Define as regras do canal, o fluxo e qual skill abrir."
---

**Protocolo obrigatório Diazverso:** antes de agir, aplicar `../diazverso-contexto-eficiente/SKILL.md`. Ler uma vez por sessão/versão e reutilizar o contexto válido; abrir somente a skill principal e as dependências necessárias.

# Diazverso: regras do canal

O Diazverso é um canal brasileiro sobre super-heróis e universos relacionados. Estas regras são o gosto do criador e valem desde a primeira mensagem, mesmo sem conhecer quem pede. Só mudam por pedido explícito do criador. Pergunte apenas o que falta para avançar.

## Regras inegociáveis

1. **Contexto eficiente.** Uma skill principal por vez. Usar o [grafo de skills](../diazverso-contexto-eficiente/references/skill-map.json) para achar o caminho. Não reler o que já foi lido nesta sessão. Manter um checkpoint curto ao trocar de etapa.
2. **Content Lab é o caminho padrão para produzir.** Na primeira produção da sessão, conferir se o MCP do Content Lab responde (`contentlab_status`). Se não estiver conectado, perguntar "Vamos usar o Content Lab?" e conectar seguindo `../diazverso-contentlab/SKILL.md`. Produzir fora dele só quando o criador recusar.
3. **Combinar o fluxo uma vez, numa pergunta só**, antes de criar o projeto:
   - **Tudo automático:** a IA faz tudo e avisa no fim.
   - **Parar em pontos:** a IA para, avisa o que revisar no Content Lab e espera. Sugestão: roteiro, narração e revisão final.
   - **Aprovar cada etapa.**
   - **Voz:** voz de IA ou o criador grava a própria voz no Content Lab.
   - **Drive e planilha:** se as ferramentas Google não responderem, perguntar se o criador quer conectar ou seguir sem elas. Sem elas, nada é gravado no Drive; no fim, o kit traz o que subir e as linhas prontas para ele preencher à mão ([modo manual](../diazverso-drive-setup/references/modo-manual.md)).
4. **Ordem da produção** (nenhuma etapa é pulada):
   1. tema polêmico, que ensina algo ou que desperta curiosidade, e a tese pesquisada;
   2. título e thumbnail, antes do roteiro (o roteiro cumpre o que eles prometem);
   3. roteiro na estrutura do canal (`../diazverso-roteiro/references/escrita.md`): gancho, prova e promessa contável, casos, contraponto, payoff e pergunta, uma frase por beat;
   4. revisão de fatos, estrutura e voz;
   5. aprovação;
   6. cenas das obras com direitos;
   7. narração;
   8. plano de motion;
   9. prévias;
   10. render;
   11. thumbnail final, limpa: fundo preto ou branco e o personagem;
   12. kit de publicação manual (com o registro manual do Drive e da planilha, quando não houver acesso).
5. **Edição = motion design do kit** (`../diazverso-motion/SKILL.md`):
   - **Ritmo:** troca de informação a cada 1,5–3 s, no ritmo do RunnyIA, com a câmera nunca parada.
   - **Visual:**
     - estética HQ madura;
     - Anton em títulos e legendas;
     - a cena da obra é a base, muitas vezes sozinha em tela cheia;
     - o Nox em opinião e humor: aparte (cena desfocada, Nox inteiro subindo pela borda de baixo) gesticulando em stop motion: a pose troca enquanto ele fala, a cada 0,7–1 s, e todas as poses do [catálogo](../diazverso-nox/references/poses.md) aparecem ao longo do vídeo;
     - fundos, cores e cenas sempre variando, nunca iguais em seguida;
     - caixinhas HQ de lembrete (inscreva-se, like, opinião, spoiler) e recortes PNG do que está sendo falado;
     - cena da obra sempre que a fala citar algo; ela é a base do vídeo;
     - Shorts em 9:16 com o mesmo ritmo, diagramados para vertical.
   - **Som:**
     - SFX em cada troca;
     - legenda palavra a palavra: o tempo todo nos Shorts; no vídeo longo, só em trechos (gancho e apartes do Nox);
     - trilha licenciada abaixando sob a voz.
   - **Proibido:**
     - texto sobre fundo liso como cena;
     - clips estáticos colados;
     - componentes TSX escritos do zero quando o kit tem a cena.
6. **Escrita:**
   - **Voz:** conversada, opinativa, irônica e bem-humorada.
   - **Formato:** ensinar ou revelar algo através de histórias e personagens ([formatos](../diazverso-core/references/formatos-editoriais.md)).
   - **Abertura:** gancho no primeiro segundo, sem "hoje vamos falar".
7. **Nunca:**
   - publicar, agendar ou enviar vídeos (o criador publica);
   - inventar fatos ou falas canônicas;
   - usar mídia sem direitos ou música sem licença (o canal é monetizado);
   - redesenhar o Nox (`assets/brand/nox/Nox.png` é a fonte);
   - prometer CTR ou retenção.
8. **Verificar de verdade.** Abrir frames, medir o áudio e ler de volta o que foi gravado. Não declarar pronto o que não foi conferido.

## Qual skill abrir

| Pedido | Skill |
| --- | --- |
| Produzir um vídeo do começo ao fim, ou retomar | diazverso-contentlab (com o Content Lab) ou diazverso-criacao-video (sem ele) |
| Pauta, tese, pesquisa | diazverso-pesquisa |
| Títulos | diazverso-titulos |
| Thumbnail | diazverso-thumbnail |
| Roteiro | diazverso-roteiro, depois as revisões de fatos, estrutura e voz |
| Edição, motion, som, legenda | diazverso-motion |
| Nox, poses, expressões, Nox 3D | diazverso-nox |
| Shorts | diazverso-shorts |
| Identidade e linguagem | diazverso-core |
| Drive e Sheets | diazverso-drive-setup |
| Mudar o plugin | diazverso-manutencao |

O resto do roteamento está em [roteamento](../diazverso-contexto-eficiente/references/roteamento.md).
