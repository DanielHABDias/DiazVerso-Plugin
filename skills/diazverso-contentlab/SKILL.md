---
name: diazverso-contentlab
description: "Use para produzir ou retomar vídeos Diazverso pelo Content Lab via MCP: conferir e conectar o servidor MCP, combinar o fluxo com o criador (automático, pausas, aprovação, voz própria) e conduzir as ferramentas da ideia ao vídeo final."
---

**Protocolo obrigatório Diazverso:** antes de agir, aplicar `../diazverso-contexto-eficiente/SKILL.md`. Ler uma vez por sessão/versão e reutilizar o contexto válido; abrir somente a skill principal e as dependências necessárias.

# Produzir pelo Content Lab

O Content Lab é o app local do criador que produz o vídeo inteiro. Ele cuida de:

- roteiro e embalagem;
- mídias com direitos;
- narração por IA ou gravada;
- transcrição;
- motion design com o kit deste plugin;
- render;
- thumbnail;
- kit de entrega.

O agente opera o app pelo MCP. Tudo o que o agente faz aparece no app, e o que o criador aprova no app o agente enxerga. O Content Lab nunca publica.

## 1. Conferir a conexão

Chamar `contentlab_status`. Se a ferramenta não existir, o MCP não está conectado: perguntar "Vamos usar o Content Lab?" e, com o sim, conectar. A pasta do Content Lab é a do repositório `ContentLab` do criador; se não for conhecida, perguntar onde está.

- **Claude Code:**

  ```bash
  claude mcp add content-lab -- node <pasta-do-ContentLab>/src/adapters/mcp-server.js
  ```

- **Codex** (`~/.codex/config.toml`):

  ```toml
  [mcp_servers.content-lab]
  command = "node"
  args = ["<pasta-do-ContentLab>/src/adapters/mcp-server.js"]
  ```

- **App instalado:** comando `~/.local/share/contentlab/app/current/runtime/node ~/.local/share/contentlab/app/current/app/src/adapters/mcp-server.js` com `CONTENTLAB_INSTALLED=1`.

Depois de conectar, o cliente precisa ser reiniciado ou recarregado. Então `contentlab_start` abre o app em segundo plano. `contentlab_status` mostra:

- as vozes prontas;
- se a voz clonada existe;
- se a transcrição funciona;
- o que falta instalar.

## 2. Combinar o fluxo

Uma pergunta só, antes de `project_create`. A resposta vira parâmetros do projeto:

| O criador quer | `project_create` |
| --- | --- |
| Tudo automático | `mode: "autonomous"` |
| Parar em pontos para revisar no app | `mode: "autonomous"`, `pauseAt: ["script", "narration", "review"]` (ou as etapas que ele escolher) |
| Aprovar cada etapa | `mode: "review"` |
| Gravar a própria voz | `narrationBy: "creator"` (combina com qualquer modo) |

Etapas: `brief`, `script`, `packaging`, `media`, `narration`, `edit`, `review`. Se o criador mudar de ideia, usar `project_flow_set`.

Em cada pausa, avisar no chat o que revisar e onde ("o roteiro está em Roteiro, no Content Lab; aprove ou peça mudança lá"). Depois, esperar com `stage_wait_decision`. Se ele pedir mudança, a resposta traz o motivo: corrigir e voltar a esperar. `stage_approve` recusa uma etapa de pausa sem a aprovação dele.

## 3. Conduzir a produção

1. `project_create` com o fluxo combinado.
2. `creative_write`:
   - **brief:** tese, público, promessa;
   - **packaging:** títulos A/B, conforme `../diazverso-titulos/SKILL.md`;
   - **script:** gancho, desenvolvimento e payoff, conforme `../diazverso-roteiro/SKILL.md`; uma frase por linha, cada frase vira um beat.
3. `media_import_files`:
   - **cenas das obras** citadas, com direitos confirmados e nomes descritivos (`batman-1940.jpg`);
   - **trilha licenciada**, com `role: "music"`.
4. Narração:
   - **Voz de IA:** `narration_generate` e `job_wait`, depois `narration_assemble` e `job_wait`.
   - **Voz do criador:** pedir para gravar no app (Narração → Gravar; depois Montar narração) e esperar com `stage_wait_decision`. `narration_generate` recusa nesse caso.
5. `narration_transcribe` com `job_wait`: tempos de cada palavra.
6. `motion_plan_auto`, depois `motion_preview`. Abrir os PNG em `output/previas/` e conferir assunto, legibilidade e ritmo. Ajustar com `motion_plan_set`; o contrato está em `motion_kit` e em `../diazverso-motion/SKILL.md`.
7. `thumbnails_generate` e a revisão da thumbnail (`../diazverso-thumbnail/SKILL.md`).
8. `render_start` com `job_wait`. Depois, `deliverable_build`, cujo `verificacao.md` aponta as pendências, e `project_export`.

Use `project_get` para ver o que falta em cada etapa (`missing`). Trabalhos longos devolvem `jobId`: chame `job_wait` de novo enquanto vier `waiting: true` e conte ao criador o progresso.

## Sem o Content Lab

Se o criador recusar, a produção segue `../diazverso-criacao-video/SKILL.md`, com o kit `../diazverso-motion/kit/` num projeto Remotion. As regras do canal são as mesmas.
