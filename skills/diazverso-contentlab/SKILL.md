---
name: diazverso-contentlab
description: "Use para configurar e diagnosticar o ambiente do Diazverso e para produzir ou retomar vídeos pelo Content Lab via MCP: conferir e conectar o servidor MCP, combinar o fluxo com o criador (automático, pausas, aprovação, voz própria) e conduzir as ferramentas da ideia ao vídeo final."
---

# Produzir pelo Content Lab

O Content Lab é o app local do criador que produz o vídeo inteiro. É uma ferramenta neutra, sem nada do canal: as regras, o Nox e o padrão do Diazverso vêm deste plugin, e o agente os aplica pelo MCP. Ele cuida de:

- roteiro e embalagem;
- mídias com direitos;
- narração por IA ou gravada;
- transcrição;
- motion design com o kit de motion do próprio Content Lab (`motion_kit`, `kit_docs`);
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

**Diagnóstico** (pedido de configuração, sem produção): conferir só o necessário (Content Lab, Google Drive/Docs/Sheets pela `../diazverso-drive-setup/SKILL.md`, Python e FFmpeg) e responder curto: o que funciona, o que falta e a próxima ação. Instalar o plugin ou dependências só a pedido do criador.

## 2. Combinar o fluxo

Uma pergunta só, antes de `project_create`. A resposta vira parâmetros do projeto:

| O criador quer | `project_create` |
| --- | --- |
| Tudo automático | `mode: "autonomous"` |
| Parar em pontos para revisar no app | `mode: "autonomous"`, `pauseAt: ["script", "narration", "review"]` (ou as etapas que ele escolher) |
| Aprovar cada etapa | `mode: "review"` |
| Gravar a própria voz | `narrationBy: "creator"` (combina com qualquer modo) |

Etapas, nesta ordem: `brief` (ideia), `packaging` (título e thumbnail), `script` (roteiro), `media`, `narration`, `edit`, `review`. Se o criador mudar de ideia, usar `project_flow_set`.

**O criador acompanha ao vivo.** Logo depois de `project_create`, e ao retomar um projeto, chamar `contentlab_open` com o `path`: o projeto abre no navegador padrão dele e a tela se atualiza sozinha enquanto a IA trabalha. Se não abrir, passar o `url` devolvido.

Em cada pausa, avisar no chat o que revisar e onde ("o roteiro está em Roteiro, no Content Lab; aprove ou peça mudança lá"). Depois, esperar com `stage_wait_decision`. Enquanto a IA espera, o app mostra o aviso na etapa, e o botão **Aprovar e seguir** (ou **Pedir mudanças**) devolve o sinal. O botão não trava a conversa: se o criador aprovar ou mandar seguir pelo chat, usar `stage_approve` com `userApproved: true` e continuar. Se ele pedir mudança, a resposta traz o motivo: corrigir e voltar a esperar. `stage_approve` recusa uma etapa de pausa sem a aprovação dele.

## 3. Conduzir a produção

1. `project_create` com o fluxo combinado, depois `contentlab_open`.
2. `creative_write`, uma etapa por vez, na ordem do app:
   - **brief:** tese, público, promessa;
   - **packaging:** títulos A/B, conforme `../diazverso-titulos/SKILL.md`, e o conceito da thumbnail; a descrição vem depois do roteiro, na [estrutura do canal](../diazverso-criacao-video/references/descricao.md), com os capítulos só depois do render;
   - **script:** usar `creative_write` com `script.chapters`, seguindo `../diazverso-roteiro/SKILL.md`. Reproduzir a organização audiovisual do VD_0008: capítulos temáticos livres alternando narração → cena com som original sem narrador → volta da narração que interpreta/avança, com direção visual em bloco próprio quando necessário. Cada capítulo: `id`, `title`, `blocks`; cada bloco: `id`, `type` (`narration`, `scene`, `direction`), `title`, `text`. Não colar cabeçalhos nem descrições dentro da fala. Só `narration.text` chega à voz; títulos e fontes não são lidos.
   - Para revisar só uma parte, ler `script_get` e usar `script_edit` com a revisão em `baseRevision` e operações `chapter.add/update/remove/move` ou `block.add/update/remove/move`; `beforeId` define a posição (omitido = fim). IDs estáveis preservam takes ao mover/renomear. Usar `dryRun: true` para conferir o lote; reler em conflito. A primeira versão pode vir inteira por `creative_write`; ajustes locais não precisam reenviar todo o roteiro.
   - `scene` registra a intenção, duração estimada e obra/trecho, mas não insere mídia nem áudio original e não pausa automaticamente a narração no modo composição. Conferir esses trechos na montagem; não declarar que o som da cena está pronto só por existir no roteiro.
3. `media_import_files`:
   - **cenas das obras** citadas, com direitos confirmados e nomes descritivos (`batman-1940.jpg`);
   - **trilha licenciada**, com `role: "music"`.
   - **O Nox:** o Content Lab não traz personagem. Em todo projeto do canal, importar o pacote do Nox antes do plano de motion: `character_import` com `folder` = `assets/brand/nox` deste plugin (caminho absoluto; o catálogo fica em `assets/brand/nox/poses/catalogo.json`) e `rightsConfirmedByUser: true` (o Nox é do criador). `dryRun: true` confere o pacote sem importar. Sem o Nox no projeto, o plano sai sem apartes nem a cena `personagem`.
4. Narração:
   - **Voz de IA:** `narration_generate` e `job_wait`, depois `narration_assemble` e `job_wait` até concluir também a transcrição automática.
   - **Voz do criador:** pedir para gravar no app (Narração → Gravar; depois Montar narração). A tela mostra só as falas dos blocos de narração agrupadas por capítulo, com títulos apenas de orientação; a montagem transcreve automaticamente. Aguardar a conclusão e a aprovação com `stage_wait_decision`. `narration_generate` recusa nesse caso.
5. Esperar a transcrição automática com **Whisper `large-v3` completo**, em português, terminar antes de aprovar Narração. Não usar modelo menor/turbo nem tempos estimados como substituto. Se falhar ou faltar dependência, o áudio fica preservado: corrigir e retomar com `narration_transcribe` + `job_wait`. Ler `narration_transcript` (`offset`, `limit`; continuar com `nextOffset` até `null`) para obter `text`, `start` e `end` de cada palavra e posicionar imagens, cortes, beats e legendas na fala real.
6. `motion_plan_auto`, depois `motion_preview`. Abrir os PNG em `output/previas/` e conferir assunto, legibilidade e ritmo. Ajustar com `motion_plan_set`; o contrato está em `motion_kit` e as regras do canal em `../diazverso-motion/SKILL.md`. Conferir no plano:
   - **Nox:** entra como o personagem do projeto (apartes e cena `personagem`); troca de pose enquanto fala, e todas as poses do catálogo aparecem no vídeo longo. Se `motion_plan_auto` listar `poses.posesFaltando`, encaixá-las em apartes de tom compatível ([poses](../diazverso-nox/references/poses.md)).
   - **Legenda:** o tempo todo nos Shorts; no vídeo longo, só no gancho e nos apartes.
   - **Som:** cada SFX no quadro do evento, variando, sem cobrir a fala; os nomes válidos estão em `motion_kit` ([som](../diazverso-motion/references/som.md)).
   - **Encerramento:** o `cta` do Content Lab não tem nome de canal fixo; pôr `titulo: "DIAZVERSO"` nas props do beat `cta`.
7. `thumbnails_generate` e a revisão da thumbnail (`../diazverso-thumbnail/SKILL.md`).
8. `render_start` com `job_wait`. O Content Lab tira os metadados do vídeo final (etiquetas, capítulos embutidos e assinatura do encoder) sem recodificar. Depois, `deliverable_build`, cujo `verificacao.md` aponta as pendências, e `project_export`.

Use `project_get` para ver o que falta em cada etapa (`missing`). Trabalhos longos devolvem `jobId`: chame `job_wait` de novo enquanto vier `waiting: true` e conte ao criador o progresso.

## Sem o Content Lab

Se o criador recusar, a produção segue `../diazverso-criacao-video/SKILL.md` num editor à escolha dele. O kit de motion é do Content Lab e não vem neste plugin; as regras do canal ([motion](../diazverso-motion/SKILL.md), [som](../diazverso-motion/references/som.md), [Nox](../diazverso-nox/SKILL.md)) são as mesmas.
