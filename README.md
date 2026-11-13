# Diazverso

Plugin para pesquisar pautas, criar e revisar roteiros, organizar Google Docs/Sheets, preparar thumbnails e Nox, planejar edição Remotion e entregar um kit para publicação manual.

## Uso

A skill de entrada é [diazverso](skills/diazverso/SKILL.md): regras do canal, fluxo e qual skill abrir. A produção acontece pelo Content Lab via MCP ([diazverso-contentlab](skills/diazverso-contentlab/SKILL.md)). Peça “vamos criar um vídeo para o Diazverso”. A skill de entrada traz as regras de contexto e a tabela de qual skill abrir.

## Requisitos

- Google Drive, Docs e Sheets conectados para operações nesses serviços.
- Executor com Python para os utilitários locais; Node, React, Remotion e, para as cenas 3D, `@remotion/three`, `three` e `@react-three/fiber` no projeto de edição (o Content Lab já traz todos); FFmpeg para inspeção audiovisual.
- Ferramenta de imagem para gerar artes e acesso às mídias com direitos conferidos.

As skills não fornecem essas conexões nem instalam dependências automaticamente. A edição é feita no Content Lab (app separado e neutro), pelo MCP: o kit de motion é dele, e este plugin traz as regras do canal e o pacote do Nox, importado em cada projeto com `character_import`.

Nox canônico está em `assets/brand/nox/Nox.png`. Os SFX do kit ficam em `assets/sfx/motion/` (guia em `skills/diazverso-motion/references/som.md`). Fundos procedurais HQ dispensam imagens adicionais.

## Instalação e manutenção

No Claude Code, o plugin traz `.claude-plugin/plugin.json` e um gancho de início de sessão (`hooks/hooks.json`). Esse gancho injeta as regras da skill de entrada em toda conversa, então a IA as segue mesmo sem ter acionado uma skill:

```bash
claude plugin marketplace add DanielHABDias/DiazVerso-Plugin
claude plugin install diazverso@diazverso
```

O manifesto portátil é `plugin.json`; o catálogo `.agents/plugins/marketplace.json` permite instalar pelo repositório em clientes compatíveis.

No Codex, adicione o catálogo e instale o plugin:

```bash
codex plugin marketplace add DanielHABDias/DiazVerso-Plugin
codex plugin add diazverso@diazverso
```

No cliente com interface de plugins, adicione o marketplace pelo link https://github.com/DanielHABDias/DiazVerso-Plugin e selecione Diazverso. Inicie uma nova conversa após a instalação. Repositórios privados exigem acesso GitHub autenticado.

No ChatGPT com importação de workspace, um administrador usa Plugins → Adicionar → Importar marketplace, informa o mesmo repositório e deixa o caminho vazio. A disponibilidade desse fluxo depende da conta/cliente; colar um link na conversa não instala automaticamente.

Referências oficiais: [empacotamento e marketplaces](https://developers.openai.com/plugins/build/plugins) · [importação GitHub](https://help.openai.com/en/articles/20001504-importing-and-syncing-plugin-marketplaces-from-github). O onboarding confere as capacidades presentes. No Codex e no ChatGPT, as instruções valem quando o Diazverso é acionado; no Claude Code, o gancho de início de sessão as carrega sempre.

Para uso obrigatório no repositório aberto no Codex, `AGENTS.md` contém o ponto de entrada. Em outro workspace, a política desse workspace precisa acionar o Diazverso. O plugin não controla cache interno, raciocínio oculto ou métricas que o host não exponha.

`scripts/validate_plugin.py` confere estrutura, referências, assets, sintaxe e mapa. `scripts/build_plugin.py --output /caminho/fora/do/repositorio/diazverso.zip` gera o pacote. Essas ferramentas de manutenção não integram o ZIP instalado.

[Manutenção de skills](skills/diazverso-manutencao/SKILL.md) · [Licenças e atribuições](THIRD_PARTY_NOTICES.md)
