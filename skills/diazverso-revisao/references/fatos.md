# Diazverso — Revisão de fatos, fontes e promessas (facts)

**Finalidade:** auditar afirmações verificáveis de uma produção `VD_####` ou `SH_####` e a coerência das promessas de título, thumbnail e gancho. Esta skill **não** pesquisa por conta própria, não garante acesso à web e não aprova automaticamente um roteiro.

## Entradas e ativação

- Roteiro ou trecho identificado (versão/data), tese, títulos A/B, conceito de thumbnail, gancho e fontes já reunidas.
- Se estiverem disponíveis, fontes primárias da obra, créditos, entrevistas, documentação oficial, materiais dos criadores e dados reais; fontes secundárias confiáveis complementam, mas não substituem automaticamente uma fonte primária.
- Conferir datas e versão da obra: quadrinhos, adaptações, timelines, reboots e universos alternativos podem contradizer-se sem erro. Não misturar cânones.
- Não carregar biblioteca inteira, nem inventar acesso ao Drive, YouTube ou navegador. Consultar referências apenas para a alegação ativa.

## Procedimento obrigatório

1. **Extrair alegações relevantes.** Para cada frase verificável, marcar um ID de achado, localização no texto, afirmação exata/paráfrase fiel, obra/versão e consequência se estiver errada. Priorizar números, datas, causalidade, citações, identidade, origem, canon, recepção, bastidores, desempenho e declarações de terceiros. Evitar sobrecarregar com trivialidades sem risco editorial.
2. **Classificar antes de julgar:**
   - `FATO` — alegação externa verificável, com fonte rastreável;
   - `INTERPRETAÇÃO` — leitura da obra sustentada por cenas/argumento, não um fato universal;
   - `OPINIÃO` — julgamento pessoal do criador, claramente apresentado;
   - `HIPÓTESE/TEORIA` — possibilidade não confirmada, com incerteza expressa.
   Se mistura categorias, separar a frase e revisar a redação.
3. **Checar cada fato material contra a fonte.** Registrar URL/título/autoria/data ou referência verificável à obra (edição, episódio, capítulo, cena) e o que a fonte efetivamente confirma. Pesquisar com ferramentas reais **quando disponíveis**; caso contrário sinalizar `NÃO VERIFICADO`, nunca preencher fontes fictícias. Evidência insuficiente ou contraditória não vira confirmação.
4. **Separar evidência da inferência.** Uma obra mostrar um evento não prova intenção de roteirista; uma declaração isolada não prova consenso de público; recepção ou métrica não deve ser alegada sem dados apropriados. Rumores e vazamentos devem aparecer explicitamente como não confirmados, com data.
5. **Verificar as promessas.** Comparar título A/B, thumbnail e abertura com o conteúdo demonstrado e o payoff do roteiro. Se a embalagem promete um fato, conclusão ou revelação que o vídeo não sustenta, marcar `REVISAR` ou `REPROVAR`, mesmo que pareça clicável. Consultar `diazverso-revisao-embalagem` quando a dúvida exigir análise visual/packaging.
6. **Propor correções mínimas.** Para cada achado, sugerir reescrita em português brasileiro natural sem apagar humor/opinião legítimos; quando não houver base, recomendar pesquisa, atribuição explícita, qualificação ou remoção da afirmação. Não transformar hipótese em fato durante a reescrita.
7. **Revisar novamente** somente as afirmações corrigidas e suas consequências sobre título, gancho e conclusão. Não declarar que houve checagem em fonte não aberta.

## Formato de entrega

Apresentar um relatório breve por produção/versão:

| ID | Local/alegação | Tipo | Fonte e evidência | Estado | Ação |
| --- | --- | --- | --- | --- | --- |
| claim | Trecho identificado | FATO / INTERPRETAÇÃO / OPINIÃO / HIPÓTESE | Fonte verificável ou "não consultada" | CONFIRMADO / CONTESTADO / NÃO VERIFICADO / NÃO APLICÁVEL | Manter / reescrever / pesquisar / remover |

Depois registrar **promessa título–thumbnail–gancho–payoff**: `COERENTE`, `AJUSTAR` ou `NÃO SUSTENTADA`, com justificativa específica. Fechar com `APROVAR REVISÃO FACTUAL`, `REVISAR` ou `BLOQUEADO POR EVIDÊNCIA`, enumerando impedimentos. `APROVAR REVISÃO FACTUAL` significa apenas revisão factual concluída, **não** aprovação editorial definitiva (script-approval), aprovação humana, publicação ou verificação de render.

## Gate e segurança

- Alegações factuais relevantes têm fonte conferida ou foram **explicitamente** qualificadas/removidas. Achado material não verificado ou contestado bloqueia aprovação factual até correção.
- Interpretações, opiniões e teorias são identificadas sem serem censuradas ou apresentadas como prova.
- Promessa da embalagem não excede a evidência nem diverge do payoff.
- Preservar o roteiro original e registrar versão e achados; atualizar Doc/Sheets somente com ferramentas e autorização reais, relendo alterações. Nunca marcar `REVISÃO=APROVADO` na planilha apenas por esta skill.
- Para tom e identidade, carregar `diazverso-core` sob demanda. Para revisão de fluidez/gancho, usar a skill especializada correspondente, sem repetir todo o contexto.
