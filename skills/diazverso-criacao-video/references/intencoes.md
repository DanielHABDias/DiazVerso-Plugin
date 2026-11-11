# Intenções e despacho por etapa — Diazverso

**Consultar somente quando houver dúvida de roteamento.** A skill orquestradora `diazverso-criacao-video` controla o fluxo; as demais executam uma saída específica. Para ação externa, confirmar ferramenta e autorização.

| Pedido principal | Responsável atual | Tarefa/resultado esperado | Quando não existir a skill especializada |
| --- | --- | --- | --- |
| "me dê ideias" / pauta futura | `diazverso-criacao-video` + `diazverso-core` | Ideia distinta, pesquisa, tese e fontes | Planejar editorialmente; aba Ideias só com conector |
| "defina o título" / teste A/B | `diazverso-criacao-video` + `diazverso-core` | Títulos A/B e promessa | Não alegar teste real de CTR |
| "escreva roteiro" | `diazverso-criacao-video` + `diazverso-core` | Roteiro audiovisual | Usar `diazverso-roteiro`; Doc nativo depende de Drive/Sheets reais |
| "revise fatos" / "confira fontes" / "valide a promessa" | `diazverso-revisao-fatos` | F07: mapa de alegações, evidência, fato/opinião/hipótese e promessa | Sem fonte consultada, registrar NÃO VERIFICADO |
| "revise estrutura" / "melhore gancho" / "ritmo" | `diazverso-revisao-estrutura` | F08: batidas narrativas, redundância, payoff e hipótese de retenção | Não inventar métricas de audiência |
| "humanize roteiro" / "naturalize a narração" | `diazverso-revisao-voz` | F09: revisão ANTES/DEPOIS/MOTIVO preservando sentido e voz Diazverso | Sem áudio, não alegar escuta ou ensaio |
| "aprovar roteiro" / "liberar edição" | `diazverso-aprovacao-roteiro` | F10: gate factual, estrutural, voz, packaging e confirmação humana | Sem decisão explícita, não registrar aprovação |
| "revise roteiro" (pedido geral) | `diazverso-criacao-video` | Despachar F07 → F08 → F09 → F10 conforme pendências, uma por vez | Não tratar skill instalada como revisão realizada |
| "crie thumbnail" / capa | `diazverso-core` + ferramenta de imagem quando houver | Briefing ou imagem efetiva | Salvar no Drive somente com conexão |
| "Nox" / "pose do Nox" | `diazverso-core` | Personagem consistente com referência canônica | Nox.png já incluído; revisão visual de poses A05/G01 pendente |
| "anime", "TSX", "edite" | `diazverso-criacao-video` | Plano de cena, código e render quando runtime real | Não depender de Content Lab antigo |
| "efeitos sonoros" / "música" | `diazverso-criacao-video` | Seleção contextual e direitos | Sem áudio real, apenas proposta, não QA |
| "Short", "vídeo vertical" | `diazverso-criacao-video` + `diazverso-core` | 9:16, legendas e CTA | Preferência ≥60s, não regra YouTube |
| "prepare o kit para postar manualmente" / "faça a descrição" | `diazverso-criacao-video` | Entregar título, descrição, tags, fontes, afiliados pertinentes e materiais finais | **O criador publica manualmente; não oferecer envio, agendamento ou tutorial de postagem** |
| "configurar Drive", "planilha" | `diazverso-setup` | Diagnóstico e estrutura existente | Sem ferramentas não criar |
| "economizar tokens", "contexto" | `diazverso-contexto-eficiente` | Contexto enxuto e decisão sobre refs | Usar `context-optimization` externa só no caso avançado |

**Limite atual:** skills técnicas ainda podem estar pendentes. **Publicação de vídeos não é função planejada nem ausente: foi explicitamente excluída.** O plugin produz o kit e encerra; só registra posteriormente URL/data informadas e verificadas. Não criar ou importar skill de postagem.

## Seleção determinística

1. Priorizar verbo e resultado do pedido (escrever, revisar, editar, publicar, configurar); formato longo/Short é contexto secundário.
2. Uma skill principal por microtarefa. `diazverso-core` fornece referência editorial; não deve tentar executar permissões de Drive ou render.
3. Se o pedido combina ações, partir em fases pequenas na ordem do pipeline e revisar cada uma.
4. Carregar metadados antes do corpo da skill. Carregar refs, TSX e arquivos de mídia somente quando necessários.
5. Quando tool/host estiver ausente, registrar como **não executado** e fornecer entrega parcial correta.
