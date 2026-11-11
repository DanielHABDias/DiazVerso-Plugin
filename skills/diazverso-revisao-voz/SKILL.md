---
name: diazverso-revisao-voz
description: "Use para humanizar e revisar a narração PT-BR de roteiros Diazverso mantendo o raciocínio encadeado, humor contextual, opinião e fatos sem criar voz genérica de YouTuber."
---

**Protocolo obrigatório Diazverso:** antes de agir, aplicar `../diazverso-contexto-eficiente/SKILL.md`. Ler uma vez por sessão/versão e reutilizar o contexto válido; abrir somente a skill principal e as dependências necessárias.

# Diazverso — Revisão de voz e naturalidade (voice)

**Objetivo:** editar um roteiro para soar como uma fala natural do criador, preservando tese, evidências, referências da obra e personalidade. **Não imitar literalmente** outros criadores; FALL, Um Nerd e RunnyIA são referências de função, não vozes para copiar.

## Entradas

Roteiro `VD_####` ou `SH_####` identificado por versão, tese, contexto da cena e, quando houver, trechos de voz ou correções **aprovadas pelo criador**. Sem amostra autorizada, usar apenas diretrizes editoriais do Diazverso, **não inventar uma transcrição do Daniel**. Carregar `diazverso-core` somente quando houver dúvida; separar colunas `NARRAÇÃO` de `SOM DA CENA`, instruções visuais e kit não narrado.

## Método em cinco passagens

1. **Sentido antes do estilo:** identificar o que cada bloco realmente afirma e o papel dele na história. Não mudar fatos, conclusão, opinião, nível de certeza, nome de personagem nem promessa ao ajustar a voz. Quando detectar erro ou alegação sem fonte, sinalizar facts, sem “corrigir” por palpite.
2. **Fala natural editada:** preferir períodos de tamanho médio, frequentemente com orações conectadas por causa e consequência. A fala deve desenvolver o raciocínio, não virar sequência de slogans curtos, máximas “profundas” ou frases de trailer.
3. **Marcas de personalidade com medida:** usar “cara”, “mano”, “olha”, “só que”, “pra mim”, “eu acho”, “tipo assim”, “aí tu me complica” apenas quando a frase pedir. Humor nasce da situação, ironia ou observação específica. Evitar bordões automáticos, piada por obrigação, gíria a cada frase, gritos e palavrão gratuito.
4. **Cortar artificialidade:** identificar explicação escolar, linguagem de release publicitário, narração épica, repetição de “e é aí que tudo muda”, “no fim das contas”, “isso diz muito sobre”, perguntas retóricas sem função e reflexão genérica. Reescrever com detalhes da obra, não com enfeites.
5. **Ler em voz alta quando houver recurso humano/áudio real:** testar respiração, ênfase e inteligibilidade; **sem áudio disponível**, avaliar somente o texto, marcar `FLUIDEZ TEXTUAL AVALIADA` e não alegar ensaio ou análise vocal executada. Preservar pausas e picos seletivos de energia, sem aumentar dramatização em toda sentença.

## Entrega

Para cada trecho problemático, mostrar `ANTES`, `DEPOIS` e `MOTIVO` de modo breve. Preservar a estrutura do arquivo, cabeçalhos e campos não narrados. Não reescrever o roteiro inteiro se ajustes pontuais bastarem. Relatar:
- Quais vícios de voz foram removidos, com exemplos.
- Onde a opinião/humor foi preservada e se o tom mudou.
- Qualquer alteração que precise de nova revisão factual (facts), estrutural (structure) ou confirmação explícita do criador.
- Estado: `REVISÃO DE VOZ CONCLUÍDA`, `REVISAR COM CRIADOR` ou `BLOQUEADO`, com motivos.

## Gate

Uma revisão de voz só fica concluída quando o texto revisado preserva **fatos e hipóteses marcados**, mantém a promessa narrativa, soa conversado em PT-BR e não introduz persona artificial. Reabrir facts/structure se as modificações alterarem evidência, ritmo ou payoff. Não marcar `REVISÃO=APROVADO` em Sheets: voice aprova no máximo a **qualidade textual da voz**, não o roteiro inteiro; script-approval exige gate editorial/humano. Não escrever em Docs/Sheets sem conexão, autorização e leitura de retorno.
