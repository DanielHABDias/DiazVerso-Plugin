# AGENTS.md — Diazverso 1.0

Este repositório documenta a nova arquitetura do plugin Diazverso, ainda em fase de definição.

## Início obrigatório de cada sessão do agente
1. Ler `docs/DECISOES_E_CONTEXTO.md` e identificar o que é decisão confirmada, hipótese ou dado provisório.
2. Verificar o estado atual do repositório (branch, arquivos e alterações não commitadas) antes de editar.
3. Carregar apenas as skills e referências pertinentes ao pedido atual; economizar tokens, evitar recitar documentos inteiros e reutilizar contexto já válido.
4. Se faltar uma definição editorial que o criador ainda não forneceu, não inferir que versões antigas continuam válidas.
5. Manter a grafia da marca **Diazverso**. A documentação editorial oficial V1.0 será construída após novo briefing do criador.

## Desenvolvimento
- **Contrato de organização do Drive aprovado:** quando a tarefa envolver planilha, roteiros, thumbnails, criação de vídeo ou integração Google, ler sob demanda `docs/CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md`. A estrutura real foi montada no Drive, mas a **automação do plugin não foi implementada**. Não utilizar IDs da conta atual como globais, não duplicar documentos, criar Docs já formatados e preservar arquivos. Ao promover ideia para produção, registrar e verificar a produção antes de remover a linha da aba Ideias.
- Escolher as skills especializadas por tarefa e evitar regras globais contraditórias; uma fonte canônica por decisão.
- Para TypeScript/React/Remotion, priorizar documentação oficial da versão realmente instalada; checar tipos, lint, testes, composição/preview e renderização quando aplicável. Não afirmar que um teste passou sem executá-lo.
- Não reconstruir o Content Lab antes de auditar seu código, fluxos, dependências e limitações. Integração MCP depende de estudo de segurança, permissões e infraestrutura.
- Tratar métricas de YouTube e recomendações estratégicas como hipóteses verificáveis, nunca certezas sobre o algoritmo.
- Nenhuma exclusão de vídeos, canal, branches, arquivos ou outras ações destrutivas sem autorização explícita e específica.

## Memória entre sessões
- Atualizar `docs/DECISOES_E_CONTEXTO.md` ao final de uma etapa com decisões aprovadas, evidências datadas, alterações verificadas, próximos passos e pendências.
- Não inflar AGENTS.md com roteiro, cores, política social, prompts ou documentação técnica extensa: essas regras vão para skills/referências específicas consultadas sob demanda.
