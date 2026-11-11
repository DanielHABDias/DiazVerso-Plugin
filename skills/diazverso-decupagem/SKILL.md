---
name: diazverso-decupagem
description: "Use para transformar roteiro aprovado em cenas, componentes TSX/Remotion, planejamento de áudio, previews e revisão audiovisual de vídeo longo ou Short Diazverso."
---

**Protocolo obrigatório Diazverso:** antes de agir, aplicar `../diazverso-contexto-eficiente/SKILL.md`. Ler uma vez por sessão/versão e reutilizar o contexto válido; abrir somente a skill principal e as dependências necessárias.

# Edição por cenas

1. Receber ID, formato e revisão aprovada do roteiro. Confirmar narração, intenção visual, mídia e direitos.
2. Dividir por mudanças de informação: objetivo, fala, visual, duração, camadas, música/SFX, legenda e fonte. Evitar cortes ou efeitos sem função.
3. Selecionar apenas os recursos necessários da [biblioteca motion](references/motion.md). Para áudio, usar catálogo revisado e duração aferida.
4. Exportar o contrato `../../schemas/remotion-composition-v1.schema.json` e validar com `scripts/validate_composition.py <props.json>`. A validação estrutural não comprova mídia nem render.
5. Gerar a composição no projeto Remotion disponível. Cenas usam `Sequence`, áudio e componentes com tempos relativos coerentes e dimensões do formato.
6. Executar `scripts/render_previews.py` com props, entrypoint, composição e saída. Sem `--execute`, retorna plano; com execução autorizada, usa Remotion já instalado e recusa sobrescrever arquivos.
7. Inspecionar os arquivos reais. Usar [QA e correções](references/qa.md) para escolher o revisor do problema. Renderizar novamente o trecho alterado antes de aprovar.
8. Para vertical, aplicar `../diazverso-shorts/SKILL.md`: preset, margens, captions e CTA. Gerar legendas de timestamps reais, sem inferir sincronia por presença de SRT.

## Contrato audiovisual

- ID de produção e revisão de roteiro identificáveis.
- `fps`, `width`, `height`, `duration_frames`, assets com caminhos e direitos, cenas ordenadas e saída declarada.
- Cada cena informa início/duração, objetivo, visual, layers, captions e áudio. Respeitar intervalos e duração conhecida dos arquivos.
- Localizar assets no projeto de edição. Gerar props ou preencher o contrato não executa a composição nem verifica direitos.
- Arquivos existentes e fontes originais não são sobrescritos automaticamente.

## SFX originais

`assets/sfx/catalog.json` descreve cinco WAVs procedurais sem samples externos: whoosh curto/longo, ding, boom e riser. `scripts/build_original_sfx.py <pasta-nova>` os reproduz sem sobrescrita.

Integridade e sinal são medidos; escuta/aprovação editorial continuam obrigatórias. Candidatos não entram como APPROVED no planejador de áudio por terem sido gerados.

## Limites

Confirmar executor, mídia, fontes e permissões. Não simular análise visual, escuta, transcrição, render ou aprovação. Não publicar conteúdo. O kit final depende de revisão real dos arquivos e decisão do criador.
