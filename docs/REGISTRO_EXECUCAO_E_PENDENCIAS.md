# Diazverso 1.0 — Registro de execução, riscos e pendências

> Atualizado em 2026-11-10. Evidências e status devem ser conferidos no GitHub. **Não é relatório de plugin concluído.**

## Política confirmada pelo criador

1. Continuar implementando **microtarefas sucessivas sem perguntar "próximo"**, mantendo revisão e evidência de cada uma antes de marcar `[x]`. Não afirmar execução em segundo plano: registrar apenas o realizado na sessão.
2. **Skills externas selecionadas devem estar dentro do pacote distribuído**, com sua documentação, dependências, origem, versão e condições de licença. **Não copiar e redistribuir** skills sem licença de redistribuição inequívoca; nesse caso criar alternativa autoral independente e registrar o bloqueio para a skill original.
3. Plugin antigo e Content Lab antigo são **fontes obsoletas de exemplos**; decisões aprovadas no novo Diazverso prevalecem. O Content Lab será refatorado **após** o plugin 1.0.
4. O **Nox.png canônico precisa estar fisicamente no pacote** final. Não declarar o plugin pronto até o asset ter sido recuperado, validado visualmente/por integridade e incluído na distribuição.
5. **Documentos temporários usados para guiar a implementação serão deletados somente ao final da versão 1.0 completa, instalada e revisada**, após migrar decisões estáveis para fontes canônicas, garantir que não há referências dependentes e obter checklist de limpeza. Nunca eliminar cronograma, evidências e regras enquanto forem necessárias; preservar git histórico.
6. **B06 continua bloqueada** por ausência de confirmação de instalação/invocação real de ChatGPT e Codex. A autorização nova para implementar tarefas independentes **não aprova B06, não ignora seu teste e não autoriza marcar Gate B como concluído**. Trabalhos não dependentes de host podem ser implementados/revisados em paralelo. Reabrir B06 quando houver teste de host.

## Pendências e riscos (atualizar conforme trabalho efetivo)

| ID | Situação | Bloqueio ou risco | Critério de desbloqueio |
| --- | --- | --- | --- |
| P-B06-HOST | **PARCIAL — HOST BLOQUEADO** | Os ZIPs mínimo e completo foram gerados e validados no GitHub Actions, mas **não há instalação/invocação comprovada no ChatGPT ou Codex**. | Testar instalação/descoberta de setup e core em hosts disponíveis; manter B06 `[ ]` até comprovação. |
| P-PYTHON | **RESOLVIDO PELO CI** | O runner GitHub executou o empacotamento mínimo (runs `42895021889`, mais recente `42898444365`) e completo (runs `42895286304`, mais recente `42898444272`), com sucesso; o último ZIP completo verificado antes da auditoria continha **71 arquivos, 592.367 bytes**, SHA-256 `7c8af2fd919f2dd67902b6c215165b8c7bdd7dd265b67c66948071036fdd08fb`. As contagens mudam quando novas skills entram. Python local nesta sessão continua indisponível, mas deixou de impedir validação do pacote. | Revalidar CI após alterações de código/skills; não substituir teste de host. |
| P-EXTERNAL-LICENSE | **EM AUDITORIA** | `remotion-dev/skills` não apresentou arquivo LICENSE na raiz ao consultar GitHub em 2026-11-10; sem licença clara, **não copiar o código original ao pacote**. Outras skills devem ser auditadas individualmente. | Licença explícita ou autorização de redistribuição; caso contrário usar skill autoral, não cópia. |
| P-NOX | **INCORPORAÇÃO E ZIP APROVADOS; REVISÃO DE POSES PENDENTE** | `Nox.png` original em `assets/brand/nox/Nox.png`, Git blob `776d1b26983e6f9095178881c83b44f114a40336`, 415.179 bytes, 1408×768 RGBA, CRC válido. O pacote completo foi validado no CI contra hash e PNG. | Revisar visualmente novas poses/aplicações (G01), confirmar Nox presente no plugin instalado (L06). |
| P-RENDER | **PENDENTE** | Sem runtime Remotion/TSX comprovado nesta sessão; Content Lab legado não deve ser pré-requisito. | Teste de composição/render independente e revisão de quadros/áudio. |
| P-F06-SHEETS | **PARCIAL; NÃO APROVADO** | `diazverso-roteiro`, gerador UTF-16 e 7 testes unitários passaram no [CI 42898526361](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42898526361), mas nenhuma criação nativa + vínculo da célula ROTEIRO na linha de Produções foi testada como fluxo integrado. | Em produção de teste isolada, criar/mover/formatar Doc, gravar URL na linha exata, ler de volta, repetir sem duplicata e recuperar falhas. F06 permanece `[ ]`. |
| P-DRIVE | **PENDENTE** | Skills de Drive não criam permissões nem conectores; reparo e promoção de ideia têm risco de duplicata/perda. | Testar fluxos idempotentes com Drive/Sheets reais e permissões, com rollback lógico. |
| P-LIMPEZA | **ADIADA ATÉ 1.0 CONCLUÍDA** | Rascunhos e roadmaps ainda são necessários; exclusão prematura perde conhecimento e vínculos. | Release final validada, migração de regras canônicas, verificação de referências e checklist de exclusão. |

## Retomada efetiva após interrupção — 2026-11-10

- **Primeiro snapshot restaurado:** roadmap com 87 microtarefas; **18 marcadas como concluídas** (A01, B01–B05, C01–C05, D01/D02/D06, E01, F01–F03). Não confundir aprovação documental de skills com testes de host.
- **Último item editorial criado:** F03, skill `skills/diazverso-revisao-embalagem/SKILL.md`, concluída e marcada após revisão.
- **Outros arquivos já adicionados e verificados em GitHub:** `Nox.png` binário e `assets/manifest.json`; skill externa MIT `context-optimization`; pacote MIT `video-editing`, `analyze-video-editing`, `find-broll` com licenças, refs, scripts/templates; proteção `--allow-external-upload` na análise de áudio; `docs/TERCEIROS_E_LICENCAS.md`; empacotador `scripts/build_diazverso_plugin.py` e workflow `.github/workflows/full-plugin-package.yml`. **Existência e inspeção estática não equivalem a ZIP/execução funcional aprovados.**
- **Ainda não iniciados quando a execução foi interrompida:** A02 (briefing canônico), A04 (decisão Content Lab), A06 (capacidades por host), F04 (modelo nativo de Doc longo) e os demais pendentes. Ordem: escolher a próxima tarefa **independente**, executar, fazer revisão separada e somente depois marcar a checklist.
- **B06 permanece não concluída:** instalação/invocação real em ChatGPT/Codex sem evidência; não a contornar ou marcar.
- **Progresso adicional após retomada:** A02 (especificação canônica), A04 (Content Lab pós-V1), A06 (matriz de capacidades) concluídas/revisadas. ZIP completo corrigido após falha `.gitkeep` e aprovado no [GitHub Actions run 42895286304](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42895286304); mínimo B06 aprovado no [run 42895021889](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42895021889). **B06 não concluída**: faltam instalação e invocação em ChatGPT/Codex. Próxima microtarefa elegível: A07 (teste real de retomada com GitHub) ou outra independente revisável.

## Falha diagnosticada e corrigida — empacotamento completo

- **Falha:** no [run 42895075994](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42895075994), o empacotador encerrava com `PACKAGE_FAILED: Extensão inesperada: skills/video-editing/assets/remotion-edit-template/public/media/.gitkeep`.
- **Causa:** o Python `Path.suffix` retorna string vazia para `.gitkeep`; a extensão estava na allowlist, mas a função não aceitava o nome do dotfile.
- **Correção em GitHub:** commit `1baff562d8f72c7c4f2aa76292de80f161c59dee` alterou `is_allowed` para aceitar explicitamente `LICENSE` e `.gitkeep`, sem aceitar dotfiles arbitrários.
- **Evidência:** [run 42895286304](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42895286304) passou: `PACKAGE_VALIDATED`, 66 arquivos, **581.317 bytes** e SHA-256 `96fb43a1a31c1ab4e0cdb12b936f6c1054b13b4660f18cab59bbb98091210499`; artifact privado `diazverso-plugin-full-test`, ID `13800421739`. **Não equivale a instalar o pacote no host**.

## Auditoria de passagem para Codex — 10/11/2026

**Estado verificado:** 87 microtarefas no [roadmap](ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md), **24 [x]**, **63 [ ]**. As 24 marcadas correspondem a escopo de documentação, skills, assets, modelos ou verificações concluídos; **não significam que o plugin está funcional de ponta a ponta**. Foram verificadas a existência dos artefatos texto relacionados, modelos nativos Google Docs, CI do empacotamento e testes da geração de requests. A consulta textual ao `Nox.png` falhou por tentar tratar PNG binário como UTF-8, **não por ausência do arquivo**; o empacotador validou o blob, hash e CRC no CI.

- **B06 [ ]:** ZIP mínimo/completo no GitHub Actions passou; instalação e invocação do plugin em ChatGPT/Codex **não demonstradas**.
- **F06 [ ]:** habilidade, gerador de requests UTF-16 e testes já criados; **7/7 testes e amostras LONGO/SHORT passaram** no [run 42898526361](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42898526361); **escrita Google Docs + link em Sheets não realizados como teste de integração**.
- **F04/F05 [x]:** os Docs nativos de modelo longo e Short seguem existentes, com estilos estruturados; blueprints portáteis em `templates/`.
- **Pendências críticas adicionais:** descoberta de skills, idempotência Drive/Sheets, promoção TF→VD/SH com rollback, revisão visual de Nox, render Remotion independente, thumbnails, Shorts, QA, publicação e instalação final.
- **Passagem ao Codex:** `docs/HANDOFF_CODEX_2026-11-11.md` descreve ordem de trabalho, gates e lista de todos os rascunhos/roadmaps/documentos transitórios que devem ser removidos **APENAS quando a V1.0 estiver completa, validada e sem dependências desses arquivos**. O `AGENTS.md` e o README inicial apontam para a passagem.
- **Próxima ação do Codex:** validar working tree e CI, completar B06 quando host permitir e F06 numa produção de teste, seguir às microtarefas independentes. Atualizar checkbox apenas com evidência.

## Revisão por tarefa

Para marcar qualquer item `[x]`, registrar **arquivo criado/editado + leitura de retorno + critérios e resultados + limitações reais**. Teste estático é distinto de teste de runtime. Em erro corrigir e rever antes de avançar.

**Nota de planejamento:** executar trabalho independente de B06 somente porque o criador pediu continuar sem depender de um "próximo"; não apagar ou falsificar falhas. Status de release permanece **não pronto**.
