---
name: diazverso-contexto-eficiente
description: "Aplicar obrigatoriamente em toda tarefa do plugin Diazverso: economia de tokens, selecionar skills e navegar pelo grafo, reutilizar contexto válido, compactar o contexto de trabalho com preservação de decisões e retomar sem releituras."
---

# Contexto eficiente

## Protocolo obrigatório

1. Definir o resultado observável e a próxima ação. Verificar o que já existe antes de criar arquivos ou iniciar pesquisa.
2. Escolher uma skill principal pelo resultado esperado. Ler seu corpo e somente as referências necessárias à ação; nunca carregar todas as skills por rotina.
3. Reutilizar decisões, fontes e trechos já lidos nesta sessão enquanto a revisão/hash permanecer válida. Não reler esta política a cada chamada; revalidá-la quando mudar a versão do plugin.
4. Usar obrigatoriamente o grafo para descobrir dependências e a skill principal quando o caminho ainda não for conhecido e válido na sessão. Em pedido ambíguo, múltiplas skills ou sessão extensa, consultar primeiro o [mapa de skills](references/skill-map.json). Com executor, usar `scripts/context_map.py --root <plugin> --query "<resultado>"`: até três resultados, caminhos, hashes e dependências. Depois abrir a skill escolhida; o índice não executa seus procedimentos.
5. O índice incremental usa tamanho, mtime e ctime para invalidar metadados, preserva hashes e atualiza só nós alterados. O cache fica fora do pacote. Usar `--refresh` se houver inconsistência e `--no-cache` se não houver escrita disponível. Sem Python, usar o mapa portátil e as descrições das skills.
6. A navegação usa metadados; decisões e escritas usam a fonte real. Antes de modificar Docs, Sheets, arquivos ou estado, conferir a revisão atual da fonte e os campos afetados. Metadados em cache nunca comprovam fatos, permissões ou sucesso.
7. Resumir saídas volumosas para decisão, erro, evidência e caminho recuperável. Preservar mensagens úteis durante depuração; não imprimir arquivos inteiros nem recitar histórico resolvido.
8. Agrupar implementação, verificação proporcional e registro em uma entrega funcional. Parar ao satisfazer o pedido; não acrescentar scaffolding ou revisão cerimonial.
9. Gerenciar obrigatoriamente o contexto por compactação semântica quando houver histórico extenso, saídas volumosas, repetição, troca de etapa com contexto acumulado ou retomada. Consultar [compactação](references/compactacao.md) na primeira necessidade e reutilizar a regra válida. Manter uma síntese ativa em vez de recontar ou reler o histórico. Em tarefa curta com contexto já enxuto, reutilizá-lo sem gerar outra síntese. Ao pausar ou trocar de etapa, manter um checkpoint curto: objetivo, produção, fonte/revisão, restrições/permissões, decisões válidas, concluído, bloqueios e próxima ação. Para produções, usar `../diazverso-criacao-video/scripts/resume.py`; reler a fonte conectada ao retomar, sem recriar itens concluídos.

O roteiro de escolha está em [roteamento](references/roteamento.md). `scripts/route_request.py` oferece classificação lexical auxiliar; pedidos compostos exigem julgamento da orquestradora.

Para técnicas avançadas, carregar `../context-optimization/SKILL.md` somente quando o problema justificar. `scripts/compare_context_cost.py` compara telemetria real de tarefas equivalentes; não inventar contagens nem apresentar bytes como tokens.

## Limites

Esta política exige o melhor uso do contexto disponível. Não controla pensamento interno, KV-cache, compactação nativa, memória oculta ou recursos do host. Sem telemetria, não afirmar percentuais de economia. Índices descartáveis não guardam credenciais nem substituem as fontes de produção.
