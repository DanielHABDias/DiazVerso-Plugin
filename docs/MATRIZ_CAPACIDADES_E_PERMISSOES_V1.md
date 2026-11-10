# Diazverso 1.0 — Matriz de capacidades, ferramentas e permissões

> **A06 — 10/11/2026.** Distingue **capacidade conceitual** de **ferramenta conectada e ação realmente executada**. Não equivale a teste de instalação do plugin nem à ativação de conectores.

## Onde cada etapa pode ocorrer

| Tarefa | ChatGPT com skills e conectores | Work/Codex ou ambiente de execução | Condição indispensável |
| --- | --- | --- | --- |
| Ideação, pesquisa, tese, títulos, análise editorial | Pode orientar e pesquisar com ferramentas acessíveis | Também pode, com arquivos e testes | Evidências reais para afirmações factuais |
| Google Drive/Docs/Sheets (localizar, criar, formatar, atualizar) | **Somente** se a conexão e a ação Google correspondentes estiverem disponíveis | Pode usar integrações e/ou interface autorizada | Conta/escopo/edição confirmados; leitura de retorno |
| Personagem Nox e thumbnails | Pode orientar e gerar imagem quando o gerador estiver disponível; usar **imagem de referência real** | Pode produzir/armazenar arquivos e integrá-los ao fluxo | `Nox.png` real e direitos; revisão visual |
| TSX/Remotion, FFmpeg, voz, trilha e render | Pode orientar/criar instruções e código, **mas skill não executa render por si só** | Exige executor com dependências, arquivos e permissão de comando | Runtime comprovado, dependências, validação de quadros/áudio |
| Abrir navegador, publicar ou agendar | Não presumir automação pelo simples fato de haver skill | Work/browser ou integração específica pode realizar ações se configurado | Autorização explícita, sessão autenticada, confirmação do serviço |
| GitHub (ler, desenvolver, registrar tarefa) | Pode realizar ações **quando GitHub conectado e permitido** | Também pode gerenciar repo, commits, testes e PRs | Credenciais/permissões, leitura de retorno e CI |
| Uso de skill externa incluída no pacote | Pode ser descoberta **se instalada no host** | Pode ser descoberta **se instalada no host** | Licença, referências/scripts presentes, host compatível |

A disponibilidade varia conforme conta, sessão, permissões, configurações do host, plano e ferramentas atuais. **Nenhuma linha garante que o recurso esteja disponível nesta conversa ou em outra instalação.**

## Antes de agir

1. Determinar **o próximo resultado** (uma microtarefa), e se é leitura, escrita, processamento local ou publicação.
2. Verificar **a ferramenta concreta e permissões** para esse resultado (Google, GitHub, render, geração de imagem, publicação). Não usar URL do Drive como prova de conexão.
3. Consultar o `SKILL.md` principal e referências somente quando houver necessidade. `diazverso-setup` pode fazer o diagnóstico; `diazverso-criacao-video` coordena a etapa, sem substituir a executor.
4. Diferenciar `EXECUTADO E VERIFICADO`, `APENAS PLANEJADO`, `TESTE ESTÁTICO`, `NÃO TESTÁVEL` e `BLOQUEADO`. Registrar estado sem inventar atos ou permissões.
5. Para atos destrutivos ou publicação no serviço, obter a autorização pertinente; ao criar arquivos, evitar duplicatas e ler de volta.
6. Se faltar ferramenta, **entregar a parte possível**, registrar o impedimento e continuar com outra tarefa independente. Não marcar o gate de integração que depende dela.

## Requisitos específicos do pacote Diazverso

- **B06:** exige ZIP real verificado e teste de instalação/reconhecimento/uso das skills no host. A validação de arquivos e manifesto no GitHub **não substitui** o teste.
- **D01:** `Nox.png` físico já foi inserido como blob binário no GitHub; verificação de CRC/tamanho foi feita. **Ainda falta** comprovar inclusão no ZIP completo e teste visual em fluxo G01/L06.
- **Skills de vídeo externas:** existem `video-editing`, `analyze-video-editing` e `find-broll`, mas seus scripts dependem de FFmpeg/Node/Remotion e execução local; importação no repositório **não instala** essas dependências.
- **Áudio externo:** o fork da skill de análise bloqueia envio de áudio por padrão; qualquer envio a serviços externos necessita autorização específica.
- **Content Lab antigo:** não é dependência e será refatorado **após** o novo plugin 1.0 concluído/validado.

## Resultado esperado de diagnóstico

> **Etapa solicitada:** ...  
> **Ferramentas realmente verificadas:** ...  
> **Entrega possível agora:** ...  
> **Permissões/limites:** ...  
> **Revisão e evidência:** ...  
> **Próxima microtarefa elegível:** ...

Não confundir instrução para executar com execução efetiva.
