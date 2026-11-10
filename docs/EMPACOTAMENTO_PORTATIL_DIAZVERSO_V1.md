# Empacotamento portátil do Diazverso 1.0 — decisão B05

> **2026-11-10 — B05 concluída e revisada documentalmente.** A instalação/execução de fato nos hosts permanece **B06, não testada**. A estrutura abaixo é o formato-portátil do código-fonte atual, não o pacote completo final do canal.

## Decisão de compatibilidade

- **Um único manifesto canônico:** `plugin.json` **na raiz** (schema `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`). Os hosts modernos ChatGPT e Codex usam este formato portátil; não criar `.codex-plugin/plugin.json` ou `.agent-plugin/plugin.json` por rotina.
- **Skills autodetectadas:** cada skill pertence a `skills/<nome>/SKILL.md`, com `name` correspondente à pasta, `description` útil para disparo e corpo independente de ferramentas não declaradas.
- **Configuração inicial:** `extensions.com.openai.onboardingSkill` indica `./skills/diazverso-setup/SKILL.md`. O caminho foi vinculado no manifesto e verificado contra o arquivo real.
- **Compatibilidade legada:** somente se um **host real**, após teste, exigir `.codex-plugin/plugin.json`, criar uma camada de compatibilidade mínima e mantê-la sincronizada com o manifesto raiz. A documentação oficial informa que `extensions.com.openai` do root **substitui**, não mescla, as opções OpenAI do overlay. Não criar manifestos divergentes ou dependências inventadas.
- **Sem MCP ou app fictícios:** `mcp.json`, `.mcp.json`, `.app.json`, hooks e marketplace **não fazem parte do pacote de origem atual**. Só criar se uma integração real e autorizada for testada. Skills, isoladamente, não fornecem acesso ao Drive, ao navegador nem capacidade de renderização.
- **Recursos visuais:** `Nox.png` é obrigatório para a versão completa, mas **ainda não foi importado** (`D01`); não anunciar versão final nem publicar como plugin com Nox antes de testar o asset real. Os TSX serão selecionados e verificados em tarefas posteriores.

## Layout mínimo atualmente verificado

```text
diazverso/
├── plugin.json
└── skills/
    ├── diazverso-setup/
    │   └── SKILL.md
    └── diazverso-core/
        └── SKILL.md
```

**Nota de empacotamento:** no repositório há `AGENTS.md` e documentação extensa em `docs/`. O pacote pode conter referências auxiliares, desde que realmente usadas; **se uma skill precisar ler `docs/*.md` sem acesso ao GitHub, incluir esses documentos no pacote** e testar os links relativos. Não embutir no texto curto da skill o briefing completo para não desperdiçar contexto. Nunca incluir tokens, credenciais, `node_modules` ou mídia cuja redistribuição não esteja autorizada.

## Evidências de B05

- **Documentação oficial consultada:** [Package your plugin](https://developers.openai.com/plugins/build/plugins), `skills://plugins/plugin-creator/create-plugin/references/plugin-packages.md` e `.../references/zip-requirements.md` do Plugin Creator instalado.
- **Alteração real:** adicionado `extensions.com.openai.onboardingSkill="./skills/diazverso-setup/SKILL.md"` ao `plugin.json`. Nome `diazverso`, versão `0.1.0`, `extensions.com.openai.interface` e demais campos preservados. Manifesto relido no GitHub após atualização.
- **Revisão pós-alteração, independente:** **12/12 verificações aprovadas:** schema, só um manifesto, duas skills válidas no local correto, nomes únicos, arquivo de onboarding existente, ausência de MCP/apps não verificados, ausência de overlay redundante, identidade/versionamento preservados, interface presente e ausência de logos fictícios.
- **Nenhum arquivo extra de compatibilidade foi criado:** `.codex-plugin/plugin.json`, `.mcp.json`, `mcp.json`, `.app.json`, `agents/openai.yaml` e marketplace local não existiam; não são pré-requisitos do pacote portátil atual.
- **Limites:** a revisão foi feita por inspeção das fontes oficiais e dos arquivos via GitHub. Não foi gerado/instalado ZIP, não foram invocados comandos Codex, nem houve teste real das skills no ChatGPT. Esses testes estão reservados à **B06**.

## Próxima microtarefa — B06 (não iniciada)

1. Preparar um pacote de **teste**, sem confundi-lo com release final.
2. Inspecionar arquivos, layout e referências no arquivo compactado.
3. Tentar instalação em host disponível com permissão explícita; verificar que as **duas skills** são descobertas e que o onboarding invoca `diazverso-setup`.
4. Testar um pedido de setup e um pedido editorial, confirmando roteamento e limitações.
5. Registrar resultado por host: `PASSOU`, `FALHOU` ou `NÃO TESTÁVEL`. Se o host exigir formato de compatibilidade adicional, adicionar **somente a estrutura estritamente necessária**, em tarefa separada e revisada.

**Estado B05:** contrato portátil aprovado; execução ainda não comprovada por teste de host.
