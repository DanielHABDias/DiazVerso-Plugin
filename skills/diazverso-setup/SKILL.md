---
name: diazverso-setup
description: "Use quando o usuário instalar, configurar ou verificar o plugin Diazverso, conectar Google Drive/Sheets ou perguntar quais etapas de produção já são possíveis."
---

# Diazverso — Configuração inicial

**Função:** verificar o ambiente e orientar a primeira tarefa. Não produzir vídeo, criar pastas ou instalar dependências sem solicitação e capacidade real.

## Procedimento mínimo

1. **Identificar a intenção.** Configuração inicial, diagnóstico ou retomada? Não iniciar um fluxo completo só porque o plugin foi mencionado.
2. **Verificar o que está disponível nesta sessão**, sem supor acesso:
   - skills Diazverso realmente reconhecidas pelo host;
   - Google Drive, Docs e Sheets conectados e suas permissões, se a tarefa precisar deles;
   - repositório GitHub, se o pedido envolver desenvolvimento ou estado versionado;
   - ambiente capaz de executar Remotion/TSX e renderizar vídeo, se houver pedido de edição.
3. **Localizar antes de criar.** Havendo Drive autorizado, procurar a raiz `Diazverso`, a planilha do canal e as pastas necessárias ao trabalho. Não copiar IDs de outra conta, não duplicar estrutura nem criar itens faltantes sem autorização. Consultar o contrato operacional vigente somente se a operação exigir detalhes.
4. **Separar capacidades:** planejamento, pesquisa, roteiros e atualização de arquivos podem funcionar com ferramentas conectadas; renderização/automação de interface exigem executor compatível. Não tratar a existência da skill como prova de execução.
5. **Aplicar as decisões da versão atual.** O plugin antigo e o Content Lab antigo são apenas referências históricas; a refatoração do Content Lab ocorrerá **depois** da conclusão do novo plugin. Não importar regras ou TSX legados automaticamente.
6. **Retornar um diagnóstico curto:** o que foi verificado, o que está disponível, o que falta para o pedido e **uma próxima microtarefa**. Não pedir novamente dados já obtidos; não declarar sucesso de operações não realizadas.

## Economia de contexto

- Carregar **apenas** a skill necessária à etapa; abrir documentação complementar sob demanda.
- Em desenvolvimento, usar `docs/ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md` e `docs/DECISOES_E_CONTEXTO.md` quando esses documentos estiverem acessíveis.
- Em operações no Drive, consultar `docs/CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md` somente quando necessário.
- Para diferenciar capacidades de ChatGPT, Work/Codex e conectores em diagnósticos complexos, consultar `docs/MATRIZ_CAPACIDADES_E_PERMISSOES_V1.md` sob demanda; nunca pressupor instalação ou credenciais.
- Não recitar o histórico inteiro e não carregar as antigas 44 skills.

## Limites e segurança

- Não instalar programas, executar códigos, mover/apagar arquivos ou publicar conteúdos sem ferramenta disponível e autorização correspondente.
- Não inventar conexão, permissão, render, revisão aprovada ou disponibilidade do Nox/TSX no pacote. `Nox.png` é um asset obrigatório **a importar e verificar em tarefa própria**.
- Esta skill é somente o **onboarding**; a identidade editorial e a orquestração completa terão skills específicas.
