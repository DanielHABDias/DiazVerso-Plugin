# B06 — Teste de pacote, instalação e reconhecimento das skills

> **Data: 2026-11-10. Estado: PARCIAL / AGUARDANDO TESTES EM RUNTIME.**
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

Saída esperada do script: `diazverso-plugin-0.1.0-b06-test.zip` ao lado da pasta clonada do repositório, ou destino escolhido por `--output`. **Isso descreve o comportamento do script, não confirma que foi executado nesta conversa.**

Também pode ser disparado no GitHub: [Actions — B06 plugin smoke](https://github.com/DanielHABDias/DiazVerso-Plugin/actions/workflows/b06-plugin-smoke.yml). Abrir a execução, conferir que terminou com sucesso e baixar o artifact `diazverso-b06-test`. **O fato de o workflow estar gravado no GitHub não confirma uma execução bem-sucedida.**

## Revisão efetivamente realizada nesta conversa

- Código-fonte do script, manifesto, duas skills e workflow lidos do GitHub após salvar.
- **21/21 verificações estáticas de inspeção do código passaram**, incluindo ausência de dependências externas, lista de arquivos permitidos, preservação do onboarding, validações, integridade prevista do ZIP, ausência de credenciais no workflow e declaração honesta de falta de instalação.
- **Não foi possível executar Python/container local** neste ambiente: ferramentas de execução retornaram erro de infraestrutura. Logo, o **ZIP não foi produzido/inspecionado em runtime aqui**.
- As ferramentas conectadas nesta sessão **não disponibilizam ação para criar/instalar o plugin privado na conta nem iniciar uma sessão Codex com o plugin instalado**. Não simular esses resultados.
- Consulta de status de GitHub Actions não mostrou execução confirmada pela interface de ferramentas disponível. A execução real do workflow fica **não verificada**.

## Gate de instalação real — PENDENTE

Para completar B06 sem antecipar nenhuma outra fase:

1. Confirmar execução **verde** do workflow GitHub Actions e inspecionar o artifact ZIP; ou executar o script em ambiente Python e guardar o relatório de SHA-256 e testes.
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
| Script executado e ZIP real inspecionado | NÃO VERIFICADO |
| Workflow executado com sucesso | NÃO VERIFICADO |
| Instalação e invocação das skills no ChatGPT | NÃO TESTÁVEL NESTA SESSÃO |
| Instalação e invocação das skills no Codex | NÃO TESTÁVEL NESTA SESSÃO |
| **Conclusão integral da B06** | **PENDENTE** |

**Não iniciar C01 ou a próxima fase como se o Gate B tivesse sido aprovado.** O roadmap permanece com B06 desmarcada, conforme compromisso com revisão antes de avançar.
