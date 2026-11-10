# B06 — Teste de pacote, instalação e reconhecimento das skills

> **Data: 2026-11-10. Estado: EMPACOTAMENTO REAL APROVADO NO CI; INSTALAÇÃO NO HOST PENDENTE.**
>
> Esta microtarefa **NÃO está aprovada como concluída**. O usuário exigiu revisão obrigatória ao final de cada tarefa antes de avançar. A revisão estática do empacotador e do workflow foi concluída, mas **a instalação/invocação real das duas skills ainda não aconteceu**.

## Entrega realizada

- [Script de empacotamento e teste](../scripts/b06_package_smoke.py) em Python 3.11, apenas biblioteca padrão.
- [Workflow GitHub Actions](../.github/workflows/b06-plugin-smoke.yml) com execução por push dos arquivos pertinentes e disparo manual `workflow_dispatch`. Ele tenta gerar um ZIP de teste e publicá-lo como artifact com retenção de 7 dias.
- Nenhuma criação de servidor MCP, instalação silenciosa, publicação do plugin em diretório público ou inclusão de assets antigos.
- O pacote **mínimo de teste**, caso o script seja executado com sucesso, contém exatamente:
  ```text
  plugin.json
  skills/diazverso-setup/SKILL.md
  skills/diazverso-core/SKILL.md
  ```
- O Nox físico e os docs auxiliares não fazem parte **deste smoke test mínimo**. São entregas posteriores. As skills atuais operam com instruções resumidas e consultam GitHub/docs apenas se acessíveis.

## Como reproduzir o teste de empacotamento

No checkout do repositório, usando Python 3.11+:

```sh
python scripts/b06_package_smoke.py
```

O script verifica:
1. `plugin.json` como JSON válido no schema Agent Plugins 1.0, nome/versão, interface e ausência de chaves portáteis indevidas.
2. Ambas as skills no caminho exato, com frontmatter `name` correspondente, `description` e corpo.
3. `onboardingSkill=./skills/diazverso-setup/SKILL.md` resolvendo corretamente.
4. Arquivos selecionados, tamanho de skill, nomes únicos.
5. ZIP gerado **fora da raiz do repositório**, lista exata, CRC e bytes idênticos aos arquivos de origem.
6. Retorno JSON com `PACKAGING_PASS`, tamanho e SHA-256, mantendo `host_installation=NOT_TESTED` corretamente.

Saída produzida no GitHub Actions: `diazverso-plugin-0.1.0-b06-test.zip`, com resultado `PACKAGING_PASS` e SHA-256 registrado no log da execução; o script também admite `--output`.

**Execução comprovada:** [B06 smoke #22, verde](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42895021889). O job `packaging` executou o script com `PACKAGING_PASS` e publicou o artifact `diazverso-b06-test`, ID `13800885173`. SHA-256 do ZIP interno: `379e4b553c15a8dfba118d1fe92e3720ade604d45d692be486eea46e60c1d979`.

## Revisão efetivamente realizada nesta conversa

- Código-fonte do script, manifesto, duas skills e workflow lidos do GitHub após salvar.
- **21/21 verificações estáticas de inspeção do código passaram**, incluindo ausência de dependências externas, lista de arquivos permitidos, preservação do onboarding, validações, integridade prevista do ZIP, ausência de credenciais no workflow e declaração honesta de falta de instalação.
- **Python/container local nesta conversa permaneceu indisponível**, porém os scripts foram **realmente executados no GitHub Actions**. O ZIP foi produzido no runner e validado pelo próprio script (lista, bytes e CRC). A inspeção pelo CI não representa instalação no ChatGPT/Codex.
- As ferramentas conectadas nesta sessão **não disponibilizam ação para criar/instalar o plugin privado na conta nem iniciar uma sessão Codex com o plugin instalado**. Não simular esses resultados.
- O status, os steps, o log de `PACKAGING_PASS` e o artifact do [run #42895021889](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42895021889) foram confirmados posteriormente pela conexão GitHub.

## Evidência adicional — ZIP completo (Nox + skills externas)

- **Primeira falha real:** o workflow completo falhava ao rejeitar o arquivo `.gitkeep` como extensão inesperada. Log: [run #42895075994](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42895075994).
- **Correção:** `scripts/build_diazverso_plugin.py` passou a permitir explicitamente o nome `.gitkeep` (não todos os dotfiles). Commit `1baff562d8f72c7c4f2aa76292de80f161c59dee`.
- **Reteste aprovado:** [run #42895286304](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/runs/42895286304), job `package` com todos os steps verdes e artifact `diazverso-plugin-full-test` (ID `13800421739`).
- Script devolveu `PACKAGE_VALIDATED`, **66 arquivos**, ZIP **581.317 bytes** e SHA-256 **`96fb43a1a31c1ab4e0cdb12b936f6c1054b13b4660f18cab59bbb98091210499`**. O validador incluiu PNG do Nox, manifesto, skills e licenças, conferindo bytes e CRC. `host_installation=NOT_TESTED` permanece explícito.

## Gate de instalação real — PENDENTE

Para completar B06 sem antecipar nenhuma outra fase:

1. **CONCLUÍDO:** execução verde do workflow B06 e ZIP mínimo validado, com artifact e SHA-256 registrados nesta página.
2. Instalar/conectar o **pacote mínimo como plugin privado de teste** no host disponível, com ação/autorização do proprietário; não confundir com lançamento 1.0.
3. No **ChatGPT**, executar uma pergunta de setup, por exemplo: *“Verifique como configurar o Diazverso com o Google Drive, sem criar pastas ainda.”* Verificar que `diazverso-setup` é reconhecida e não inventa conexões.
4. Executar uma pergunta editorial: *“Qual tese sobre Marvel ou DC combina com o Diazverso?”* Verificar que `diazverso-core` é encontrada e usa a voz/estética corretas.
5. No **Codex**, quando houver host disponível, repetir teste de descoberta e aplicação das duas skills, sem exigir Content Lab antigo.
6. Registrar os resultados separados por host e evidência de invocação: `PASSOU`, `FALHOU` ou `NÃO TESTÁVEL`. Corrigir falhas, repetir revisão, **só então marcar B06 [x]**.

## Situação atual

| Critério | Estado |
| --- | --- |
| Arquivos do manifesto + duas skills existentes | PASSOU |
| Script e workflow criados no GitHub | PASSOU |
| Revisão estática independente (21 verificações) | PASSOU |
| Script executado e ZIP mínimo validado no runner do GitHub Actions | **PASSOU — CI** |
| Workflow executado com sucesso | **PASSOU — run 42895021889** |
| Instalação e invocação das skills no ChatGPT | NÃO TESTÁVEL NESTA SESSÃO |
| Instalação e invocação das skills no Codex | NÃO TESTÁVEL NESTA SESSÃO |
| **Conclusão integral da B06** | **PENDENTE** |

**O Gate B continua NÃO APROVADO**, mesmo com o pacote aprovado no CI. O criador autorizou executar microtarefas independentes (C01–C05 já realizadas) sem aguardar a instalação. O roadmap permanece com B06 desmarcada.
