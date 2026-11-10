# AGENTS.md — Diazverso 1.0

Este repositório contém a consolidação inicial do novo plugin Diazverso 1.0. **As decisões de 2026-11-10 prevalecem. Plugin antigo e Content Lab antigo são obsoletos; usá-los somente como referência seletiva. A refatoração do Content Lab é posterior à conclusão deste plugin.**

## Início obrigatório de cada sessão do agente
1. Ler `docs/DECISOES_E_CONTEXTO.md` e identificar o que é decisão confirmada, hipótese ou dado provisório.
2. Verificar o estado atual do repositório (branch, arquivos e alterações não commitadas) antes de editar.
3. Carregar apenas as skills e referências pertinentes ao pedido atual; economizar tokens, evitar recitar documentos inteiros e reutilizar contexto já válido.
4. Se faltar uma definição editorial que o criador ainda não forneceu, não inferir que versões antigas continuam válidas.
5. Manter a grafia da marca **Diazverso**. A documentação editorial oficial V1.0 será construída após novo briefing do criador.

## Desenvolvimento
- **Criador oficial:** estruturar o plugin com Plugin Creator oficial OpenAI (skill `create-plugin`, quando disponível), escrever skills conforme Skill Creator oficial e padrão Agent Skills. Pacote portátil com `plugin.json` na raiz; nunca inventar MCP/instalações. Manifesto `plugin.json` B01 e `skills/diazverso-setup/SKILL.md` B02 criados e verificados no GitHub; **instalação/invocação ainda não testadas**. Próxima microtarefa B03: `skills/diazverso-core/SKILL.md`.
- **Roadmap de implementação em microtarefas:** quando o usuário solicitar criar/continuar o plugin Diazverso 1.0, ler `docs/ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md`, selecionar **um** checkbox pendente elegível e executar/validar **uma microtarefa por vez**, registrando evidência e resultado. Não importar as 44 skills antigas nem TSX em massa. Os arquivos Nox.png e TSX do Drive são fontes confirmadas, mas ainda precisam de importação/teste individual.
- **Bibliotecas de mídia no Drive:** para seleção/reorganização de Assets, Backgrounds, Memes, Músicas e Sounds, consultar sob demanda `docs/ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md`. Essas pastas já existem na raiz Diazverso. Priorizar assets aprovados; os diretórios `99` são acervo em revisão, **não lixeira nem licença de uso**. Não presumir que músicas “no copyright” são livres; verificar direitos antes de uso/empacotamento.
- **Contrato de organização do Drive aprovado:** quando a tarefa envolver planilha, roteiros, thumbnails, criação de vídeo ou integração Google, ler sob demanda `docs/CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md`. A estrutura real foi montada no Drive, mas a **automação do plugin não foi implementada**. Não utilizar IDs da conta atual como globais, não duplicar documentos, criar Docs já formatados e preservar arquivos. Ao promover ideia para produção, registrar e verificar a produção antes de remover a linha da aba Ideias.
- Escolher as skills especializadas por tarefa e evitar regras globais contraditórias; uma fonte canônica por decisão.
- Para TypeScript/React/Remotion, priorizar documentação oficial da versão realmente instalada; checar tipos, lint, testes, composição/preview e renderização quando aplicável. Não afirmar que um teste passou sem executá-lo.
- Não reconstruir o Content Lab antes de auditar seu código, fluxos, dependências e limitações. Integração MCP depende de estudo de segurança, permissões e infraestrutura.
- Tratar métricas de YouTube e recomendações estratégicas como hipóteses verificáveis, nunca certezas sobre o algoritmo.
- Nenhuma exclusão de vídeos, canal, branches, arquivos ou outras ações destrutivas sem autorização explícita e específica.

## Memória entre sessões
- Atualizar `docs/DECISOES_E_CONTEXTO.md` ao final de uma etapa com decisões aprovadas, evidências datadas, alterações verificadas, próximos passos e pendências.
- Não inflar AGENTS.md com roteiro, cores, política social, prompts ou documentação técnica extensa: essas regras vão para skills/referências específicas consultadas sob demanda.
