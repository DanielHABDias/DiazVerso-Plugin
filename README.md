# Diazverso — Plugin 1.0 (em construção)

Plugin modular do canal **Diazverso** para pesquisa, tese, títulos, roteiro nativo no Google Docs, thumbnails, identidade do Nox, edição/QA audiovisual e preparação de publicação, sempre **uma microtarefa e uma revisão por vez**.

> **Não é ainda uma versão 1.0 pronta para instalação/uso completo. O plugin NÃO deve ser instalado durante o desenvolvimento; o criador fará a instalação manual do ZIP apenas depois de finalização, revisão e limpeza.** O manifesto atual é `0.1.0`. O pacote já passa em testes de empacotamento no GitHub Actions, mas faltam integração completa Drive/Sheets, render/QA e testes de ponta a ponta. **A instalação não é pendência de desenvolvimento; será feita pelo criador somente depois da entrega.**

## Para continuar no Codex (11/11/2026)

**Comece em [AGENTS.md](AGENTS.md) e [Passagem oficial para Codex](docs/HANDOFF_CODEX_2026-11-11.md).** Lá estão a visão aprovada do canal, a passagem histórica com **25/87 itens em 10/11**; no roadmap atualizado em **11/11 são 29 concluídos e 58 pendentes**, após F07–F10 (skills verificadas estaticamente, sem execução no host), os testes, a sequência sugerida, o B06 concluído como teste de ZIP e o F06 ainda parcial e **a lista de documentação TEMPORÁRIA a apagar somente após a V1.0 completa/validada**.

O [roadmap detalhado](docs/ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md) e a [especificação canônica](docs/ESPECIFICACAO_CANONICA_DIAZVERSO_V1.md) são **instrumentos de desenvolvimento**, não necessariamente arquivos da distribuição final.

## Skills especializadas prioritárias

O Codex deve estudar e selecionar as melhores competências externas de motion, pesquisa, thumbnails, QA e contexto. **Iris** é prioridade de **visão/análise real de vídeos** (confirmar produto/integração antes de implementar). Quando a licença não permitir redistribuir a skill original, desenvolver uma alternativa Diazverso **autoral e testada**, sem copiar material protegido. Ver [catálogo prioritário](docs/CATALOGO_SKILLS_PRIORITARIAS_E_IRIS.md).

## Estrutura atual

- `plugin.json` — manifesto portátil.
- `skills/` — habilidades Diazverso e quatro skills externas MIT com licenças individuais.
- `assets/brand/nox/Nox.png` — mascote canônico embutido; `assets/manifest.json` — integridade e direitos.
- `templates/` — modelos portáteis de roteiro longo e Short.
- `schemas/` — estrutura de estado da produção.
- `scripts/`, `.github/workflows/`, `docs/` e `AGENTS.md` — ferramentas e contexto **de implementação**, a revisar e enxugar na limpeza pós-release.

**Importante:** `B06` concluiu o build/validação no CI **sem instalar nada**. `F06` tem skill, gerador e **7 testes de código aprovados**, mas a sincronização real com a planilha ainda não foi verificada. A instalação será feita **pelo criador depois da V1.0**, não é bloqueio atual. **Não marcar F06 concluída até testar Drive/Sheets.**

A documentação de trabalho, inclusive este README provisório, será ajustada no fechamento: o **repositório final deve conter somente materiais úteis ao plugin, licenças e instruções essenciais de instalação**, após migrar decisões e remover referências quebradas.
