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
| P-B06-HOST | **BLOQUEADO** | Ferramentas desta sessão não oferecem instalação/invocação de plugin privado em ChatGPT/Codex. Smoke test de Python e GitHub Actions não mostrou execução verificada. | Obter ZIP realmente gerado/inspecionado e evidência de descoberta e execução das duas skills em host compatível; manter B06 `[ ]`. |
| P-PYTHON | **BLOQUEADO NESTA SESSÃO** | Tentativas de Python/container para gerar ZIP retornaram erro de infraestrutura. | Execução reproduzível local/Actions com logs, sha256 e inspeção do ZIP. |
| P-EXTERNAL-LICENSE | **EM AUDITORIA** | `remotion-dev/skills` não apresentou arquivo LICENSE na raiz ao consultar GitHub em 2026-11-10; sem licença clara, **não copiar o código original ao pacote**. Outras skills devem ser auditadas individualmente. | Licença explícita ou autorização de redistribuição; caso contrário usar skill autoral, não cópia. |
| P-NOX | **PENDENTE** | O Nox no Drive foi localizado, mas ainda não há `assets/brand/nox/Nox.png` verificado no repositório. | Copiar bytes reais, validar PNG/hash/transparência, leitura de retorno e presença no pacote. |
| P-RENDER | **PENDENTE** | Sem runtime Remotion/TSX comprovado nesta sessão; Content Lab legado não deve ser pré-requisito. | Teste de composição/render independente e revisão de quadros/áudio. |
| P-DRIVE | **PENDENTE** | Skills de Drive não criam permissões nem conectores; reparo e promoção de ideia têm risco de duplicata/perda. | Testar fluxos idempotentes com Drive/Sheets reais e permissões, com rollback lógico. |
| P-LIMPEZA | **ADIADA ATÉ 1.0 CONCLUÍDA** | Rascunhos e roadmaps ainda são necessários; exclusão prematura perde conhecimento e vínculos. | Release final validada, migração de regras canônicas, verificação de referências e checklist de exclusão. |

## Revisão por tarefa

Para marcar qualquer item `[x]`, registrar **arquivo criado/editado + leitura de retorno + critérios e resultados + limitações reais**. Teste estático é distinto de teste de runtime. Em erro corrigir e rever antes de avançar.

**Nota de planejamento:** executar trabalho independente de B06 somente porque o criador pediu continuar sem depender de um "próximo"; não apagar ou falsificar falhas. Status de release permanece **não pronto**.
