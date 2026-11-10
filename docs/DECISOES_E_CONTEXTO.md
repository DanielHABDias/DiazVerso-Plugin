# Diazverso 1.0 — Registro de decisões e hipóteses

Atualizado em: 2026-11-10. Estado: plugin V1.0 ainda em planejamento; organização do Drive e planilha V1.0 já aplicada nesta conta.

## Diretriz prioritária e validação de criadores oficiais — 2026-11-10

- **Prioridade absoluta:** decisões de criação, edição, Drive e organização levantadas hoje para Diazverso 1.0. O plugin antigo (44 skills) é **obsoleto** e serve só como catálogo de exemplos selecionados, não como baseline a migrar.
- **Content Lab antigo também é obsoleto** para esta fase: a refatoração ocorrerá **após** concluirmos o novo plugin. Não bloquear a V1.0 por integração/migração do Content Lab; especificar motion/TSX por contrato Remotion independente.
- **Escolha técnica validada documentalmente:** Plugin Creator oficial OpenAI, **presente e lido neste ambiente** (`skills://plugins/plugin-creator/create-plugin`), mais Skill Creator oficial para cada skill quando disponível e padrão Agent Skills. Ver docs: https://developers.openai.com/plugins/build/plugins , https://developers.openai.com/plugins/build/skills e https://agentskills.io/specification .
- **Primeira implementação [B01] executada:** [`plugin.json`](../plugin.json) portátil na raiz, `name=diazverso`, `version=0.1.0`, parse/semver/schema/campos e leitura de retorno verificados. **Não implica plugin instalável ainda**, pois faltam as skills reais.
- **[B02] concluída:** [`diazverso-setup`](../skills/diazverso-setup/SKILL.md) criada no formato Agent Skills; validado frontmatter, localização, tamanho e leitura de retorno via GitHub. Diagnóstico mínimo de ferramentas/Drive/limites sem dependência do Content Lab legado. **Ainda não testada como skill instalada no ChatGPT/Codex.** **[B03] concluída e revisada:** [`diazverso-core`](../skills/diazverso-core/SKILL.md) criada com voz/editoria, Nox, HQ/Remotion e Shorts, com **revisão mandatória antes de avançar para outra tarefa**. Segunda passada no arquivo: **14/14 verificações positivas** (schema/frontmatter, links de 4 docs, tamanho, coerência, limites e ausência de falsa instalação). **Ainda não testada como skill instalada.** Próxima microtarefa: **B04**, validação do conjunto. Ver [roadmap](ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md).

- **[B04] concluída e revisada:** auditoria conjunta de `plugin.json`, `diazverso-setup` e `diazverso-core` contra a documentação instalada do Plugin Creator e o padrão Agent Skills. Primeira rodada: **18/18** checks; segunda revisão independente: **17/17** após eliminar dois falsos positivos de nomes de documentação confundidos com IDs. Sem conflitos de responsabilidade, URLs de Docs referenciadas existentes, sem IDs específicos de conta incorporados às skills. **Nenhum código precisou ser corrigido.** Restam teste de pacote/instalação e invocação (B05/B06), e importação física do Nox (D01). **Próxima: B05.**

## Decisões confirmadas pelo criador
- Reiniciar a arquitetura do plugin Diazverso na versão 1.0, construída do zero. Versões 1.4, 1.5 e 1.6 são histórico, não regras herdadas automaticamente.
- O criador ainda detalhará o posicionamento atual, a voz, o estilo e o processo de produção; NÃO congelar essas definições antecipadamente.
- O plugin deve incluir uma competência especializada para **economia de tokens/contexto**: núcleo mínimo, roteamento por intenção, leitura progressiva de referências e deduplicação.
- Pesquisar e avaliar skills reconhecidas para pesquisa de pautas, roteiro, revisão, thumbnail, motion design, TypeScript/React/Remotion, engenharia de software/testes e memória persistente para Codex.
- Referências a examinar: Remotion Agent Skills (oficial), Superpowers (obra), princípios de Context Engineering, vidIQ e estratégias de memória estruturada. Incorporar métodos compatíveis, não copiar regras indiscriminadamente nem presumir ferramentas acessíveis.
- Content Lab é frente separada: auditar o projeto antes de refatorar. Investigar servidor MCP para conectar ao ChatGPT, autorizações, segurança e custos. Não presumir arquitetura integralmente TypeScript.
- Preservar decisões e estado do trabalho em arquivos versionados no GitHub, de modo que novos agentes possam recuperar contexto entre sessões.

## Pesquisa do canal em 2026-11-10 — estado PROVISÓRIO
- Canal vidIQ identificado: `@diazverso`; aproximadamente 2.720 inscritos, 28 vídeos públicos, 48.962 visualizações públicas no momento da consulta.
- Relatório histórico entre 2026-01-01 e 2026-09-14: 1.034.315 views de Shorts; não confundir com acervo público atual.
- Nova fase 2026-09-15 a 2026-11-07: 44.026 views de Shorts e 4.673 views de vídeos longos; foram identificados oito vídeos longos no acervo recente.
- Relatório de espectadores dos longos: Batman/Coringa 8 de 591 views vieram de inscritos; Venom 10 de 105; Spider-Man 2 10 de 1.953. Grande maioria das visualizações NÃO veio de inscritos: não há evidência de que o catálogo antigo esteja impedindo distribuição a novos públicos.
- Retenção em três longos merece análise de abertura e expectativa: Batman/Coringa 58,6% de audienceWatchRatio no marco de 5% de duração; Venom 46,3%; Spider-Man 2 42,9% (5% representa tempos absolutos diferentes). São amostras e não provas de causa.
- Discrepância entre métricas históricas e números públicos atuais; não atribuir causa a vídeos removidos/privados sem confirmação.
- Métrica de views mudou em 2026-08-24: YouTube passou a contar visualização desde o primeiro frame para todos os formatos; usar também engagedViews para comparações.
- Fontes oficiais: https://support.google.com/youtube/answer/141805 ; https://support.google.com/youtube/answer/16541080 ; https://support.google.com/youtube/answer/16559650 ; https://support.google.com/youtube/answer/2991785 .
- Recomendação provisória: NÃO apagar o canal. O YouTube documenta que desempenho depende principalmente de reação a cada vídeo/público, e pivot pode levar meses; reinício não garante redefinição útil de recomendações.
- Antes de decisão final, examinar impressões, CTR, público novo/recorrente, fontes de tráfego e curvas de retenção; avaliar estratégia de conteúdo atual. Nenhuma operação destrutiva sem solicitação explícita.

## Caderno temporário de briefing (não canônico)

- **Em desenvolvimento desde 2026-11-10:** [RASCUNHO_IDENTIDADE_DIAZVERSO_1.0.md](RASCUNHO_IDENTIDADE_DIAZVERSO_1.0.md).
- Reúne as análises dos três vídeos de referência (FALL, Um Nerd, RunnyIA), briefing do criador sobre voz, teses, aprendizado, Nox, edição Remotion/TSX, thumbnails, cenas e sourcing, além de hipóteses e pendências.
- **Não converter em regra final por antecipação.** Consultar apenas quando a tarefa envolver o briefing ou o projeto editorial/audiovisual V1.0; na conclusão, extrair decisões aprovadas e retirar o rascunho do fluxo ativo.
- Limitação relevante: a auditoria quadro a quadro dos três MP4s não foi concluída; material de referência apoiado nas transcrições e thumbnails já inspecionadas.

## Organização do Drive/Sheets V1.0 — aprovada e aplicada
## Roadmap do novo plugin V1.0 — criado em 2026-11-10

- Plano executável salvo em [ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md](ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md), com **87 microtarefas** distribuídas por auditoria, pacote mínimo, economia de tokens, Nox/assets, Drive/Sheets, pesquisa/roteiro, thumbnails, TSX, Remotion/Content Lab, Shorts, QA, publicação e testes.
- Drive legado conferido: antigo plugin tem **44 pastas de skills**; `Custom Cenas Diazverso` oferece TSX reais e previews; `Nox.png` está em `Assets/01 - Identidade Diazverso/Nox/`. **Nada disso foi copiado para o repositório novo neste planejamento.**
- O roadmap obriga **uma tarefa pequena por vez**, gate/evidência e retomada no próximo ID. Primeira tarefa futura: `A01` inventariar as skills; cópia física do Nox em `D01`, antes dos fluxos visuais.
- Estratégia de skills candidatas: `context-optimization`/compressão, Superpowers, Remotion oficial, Agent Skills e ferramentas de QA conforme compatibilidade; seleção e instalação ainda exigem testes. Antigo Content Lab preservado como motor vivo, sem reconstrução automática.


- **Em 2026-11-10 foi auditado o Google Drive conectado** e a planilha nativa `Canal do YT`; foi salvo o estudo [PROPOSTA_ORGANIZACAO_DRIVE_PLANILHA_V1.0.md](PROPOSTA_ORGANIZACAO_DRIVE_PLANILHA_V1.0.md).
- O estudo contém fatos verificados, abas atuais, inventário resumido de roteiros/thumbnails, nova estrutura proposta, modelo de planilha e templates, provisionamento idempotente e plano de migração sem perda.
- **Status operacional em 2026-11-10:** nova estrutura e planilha V1.0 criadas no Drive, com 33 produções, 15 ideias e 8 links de afiliados; 35 arquivos de roteiro e 30 thumbnails realocados, links de roteiros verificados. Ver seção 10 do estudo acima. A planilha histórica foi preservada; detalhes do formato ainda sujeitos à análise visual do criador. Nenhuma skill de inicialização de novas contas foi implementada ainda.
- **Base operacional aprovada:** [CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md](CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md). Uma pasta `Diazverso`, subpastas `Roteiros/{Longos,Shorts}` e `Thumbnails/{Longos,Shorts}` e planilha `Canal do YT — V1.0` (abas `Produções`, `Ideias`, `Afiliados`, `Config` oculta). O fluxo passo a passo vai de tema até render/revisão e pacote de publicação; o plugin que o automatiza ainda precisa ser construído.
- **Decisão de promoção:** ao aprovar uma ideia para produção, criar e verificar registro `VD_####`/`SH_####` em `Produções` e **remover a ideia da aba Ideias somente depois do sucesso**; preservar tese/origem nos dados da produção. Não duplicar ideias ativas.
- **Limpeza concluída:** pastas antigas de Roteiros/Thumbnail excluídas após mover produção, com arquivos auxiliares antigos guardados em acervo temporário fora da raiz ativa; 33 publicações marcadas `PUBLICADO`, observações artificiais eliminadas, links de thumbnail de 4 Shorts corrigidos.
- **Limite de permissão:** tentativa de excluir a planilha original compartilhada foi rejeitada pelo Google Drive como `FORBIDDEN`; ela permanece acessível. **Não afirmar que foi apagada.** A nova V1.0 está operacional e independente. Nenhuma skill de inicialização de outras contas foi implementada ainda.

## Bibliotecas de mídia no Google Drive — reorganização efetiva em 2026-11-10

- Por pedido do criador, **Backgrounds, Assets, Memes, Músicas e Sounds** foram integrados à **raiz Diazverso** no Drive, complementando roteiros, thumbnails e a planilha.
- O inventário e os links reais estão em [ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md](ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md). Esse documento passa a ser o guia de referência sob demanda para escolha e gestão de mídia.
- `Assets`: priorizar Nox/HQ e Motion; recursos genéricos/indeterminados foram preservados em `99 - Para avaliar`, não apagados. `Backgrounds`: loops e imagens estáticas separados por HQ/textura, cores e outras.
- `Músicas`: 239 arquivos organizados entre favoritas, clima, obras/referências, bibliotecas e não classificadas; 3 **possíveis duplicatas** separadas sem excluir. Nenhum nome de pasta ou arquivo prova licença.
- `Memes`: imagens/vídeos separados; 24 MP3 antes misturados com vídeos foram para `Sounds/Memes`; sons `Outros efeitos sonoros` realocados para revisão de reações. IDs/link dos arquivos preservados.
- **A mudança aplica-se já ao Drive conectado**, mas ainda **não** existe catálogo automático/manifesto, cópia de Nox/SFX para o plugin, auditoria completa de licença ou instalação automática dessas bibliotecas em outras contas. Para o futuro plugin, aproveitar apenas assets aprovados, licenciados e adequados a cada cena.
- **Atualização de escopo:** a regra anterior de Drive "somente roteiros e thumbnails" foi substituída; o Drive também abriga bibliotecas de mídia de produção, sem obrigar a empacotar tudo no plugin.

## Política de memória
- Separar SEMPRE **decisão confirmada**, **hipótese de trabalho** e **dado medido** (com período/fonte).
- Atualizar este registro apenas quando houver nova evidência ou decisão explícita, anotando data e sem apagar histórico relevante.
- Não tratar a memória de conversas ou skills de terceiros como fonte canônica quando diferir deste registro validado pelo criador.
