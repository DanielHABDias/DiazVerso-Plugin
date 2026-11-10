# Diazverso — Plugin 1.0 (em construção)

Plugin modular do canal **Diazverso** para pesquisa, tese, títulos, roteiro nativo no Google Docs, thumbnails, identidade do Nox, edição/QA audiovisual e preparação de publicação, sempre **uma microtarefa e uma revisão por vez**.

> **Não é ainda uma versão 1.0 pronta para instalação/uso completo.** O manifesto atual é `0.1.0`. O pacote já passa em testes de empacotamento no GitHub Actions, mas faltam instalação real em ChatGPT/Codex, integração completa Drive/Sheets, render/QA e testes de ponta a ponta.

## Para continuar no Codex (11/11/2026)

**Comece em [AGENTS.md](AGENTS.md) e [Passagem oficial para Codex](docs/HANDOFF_CODEX_2026-11-11.md).** Lá estão a visão aprovada do canal, o estado dos **87 itens (24 concluídos, 63 pendentes)**, os testes, a sequência sugerida, os bloqueios B06/F06 e **a lista de documentação TEMPORÁRIA a apagar somente após a V1.0 completa/validada**.

O [roadmap detalhado](docs/ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md) e a [especificação canônica](docs/ESPECIFICACAO_CANONICA_DIAZVERSO_V1.md) são **instrumentos de desenvolvimento**, não necessariamente arquivos da distribuição final.

## Estrutura atual

- `plugin.json` — manifesto portátil.
- `skills/` — habilidades Diazverso e quatro skills externas MIT com licenças individuais.
- `assets/brand/nox/Nox.png` — mascote canônico embutido; `assets/manifest.json` — integridade e direitos.
- `templates/` — modelos portáteis de roteiro longo e Short.
- `schemas/` — estrutura de estado da produção.
- `scripts/`, `.github/workflows/`, `docs/` e `AGENTS.md` — ferramentas e contexto **de implementação**, a revisar e enxugar na limpeza pós-release.

**Importante:** `F06` tem skill, gerador e **7 testes de código aprovados**, mas a sincronização real com a planilha ainda não foi verificada. `B06` tem ZIP validado, mas falta a instalação/invocação no host. **Não marcar nenhuma das duas como concluída antes dos testes restantes.**

A documentação de trabalho, inclusive este README provisório, será ajustada no fechamento: o **repositório final deve conter somente materiais úteis ao plugin, licenças e instruções essenciais de instalação**, após migrar decisões e remover referências quebradas.
