---
name: diazverso-aprovacao-roteiro
description: "Use para validar o gate final de roteiro e packaging do Diazverso antes de autorizar decupagem, motion, edição ou render, exigindo revisão factual, estrutural, de voz e decisão explícita do criador."
---

# Diazverso — Gate editorial de roteiro e packaging (F10)

**Objetivo:** impedir que uma produção entre em edição como se roteiro, fatos e promessa estivessem aprovados quando ainda há pendências. Esta skill organiza decisões e evidências; **não concede permissão para publicar, renderizar ou alterar Google Sheets**.

## Entradas

- Identificação estável `VD_####` ou `SH_####`, tipo e versão/data do roteiro, com URL do Google Doc nativo se existir e puder ser lido.
- Tese e promessa, títulos A/B, conceito de thumbnail, gancho, payoff e revisão da embalagem.
- Relatórios aplicados **ao mesmo roteiro/versão** das revisões F07 (fatos/fontes), F08 (estrutura/ritmo) e F09 (voz). Uma skill existente sem relatório **não conta como revisão executada**.
- Decisão explícita do criador sobre versão final do roteiro e escolha do packaging. Não inferir consentimento pelo silêncio, por links existentes ou por resultado positivo de ferramenta.

## Checklist de aprovação

1. **Identidade e versão:** confirmar que roteiro, ID da produção, tipo LONGO/SHORT e revisões se referem à mesma versão. Se o texto mudou depois de uma revisão material, reabrir a revisão correspondente.
2. **Fatos e fontes:** nenhuma alegação material pendente ou contestada sem correção/qualificação. F07 registrada com referências rastreáveis ou bloqueios explicitamente resolvidos.
3. **Estrutura:** gancho conecta-se à tese, progressão permite compreender a história, redundância controlada e payoff responde à promessa. F08 registrada; não confundir estimativa editorial com retenção real.
4. **Voz:** F09 registra texto conversado PT-BR, opiniões preservadas e humor natural sem copiar a fala de outro criador. Ausência de áudio não implica revisão vocal executada.
5. **Packaging:** título escolhido e thumbnail proposta combinam com o roteiro e a abertura. Divergências de promessa ou fatos abrem nova revisão. Aprovação de **conceito** não significa que a arte final já foi produzida.
6. **Documentos e links:** quando a F06 estiver operacional, confirmar Doc nativo formatado, pasta correta e vínculo idempotente na linha da produção. Se F06 estiver pendente, **não afirmar fluxo integrado concluído**; registrar limitação e impedir transição operacional que dependa desse vínculo.
7. **Decisão humana:** apresentar resumo objetivo com versão, itens revisados, pendências e pergunta de aprovação. Somente confirmação inequívoca do criador para esta versão permite status `APROVADO PELO CRIADOR`. Uma revisão feita pela IA pode apenas recomendar aprovação.

## Estados e saída obrigatória

- `PENDENTE DE REVISÃO`: relatório F07/F08/F09 ou packaging ausente, desatualizado ou bloqueado.
- `PRONTO PARA APROVAÇÃO HUMANA`: todos os critérios editoriais verificados sem pendências materiais, mas falta decisão explícita do criador.
- `APROVADO PELO CRIADOR`: há decisão inequívoca registrada com ID e versão; somente então liberar **planejamento** de decupagem/edição, condicionando execução real aos recursos e permissões.
- `REPROVADO/DEVOLVIDO`: ajustes solicitados; reabrir as revisões afetadas e não avançar como se aprovado.

Entregar um registro conciso:

| Campo | Valor obrigatório |
| --- | --- |
| Produção/versão | ID, tipo, data/identificador do roteiro |
| Revisão factual F07 | estado + evidência |
| Estrutura F08 | estado + evidência |
| Voz F09 | estado + evidência |
| Packaging | título/thumbnail/gancho/payoff e estado |
| Pendências | bloqueios e o que falta verificar |
| Decisão humana | texto/data da aprovação específica ou `AINDA NÃO APROVADO` |
| Próximo passo | correção, pedido de aprovação ou planejamento técnico |

## Segurança e transições

- Jamais escrever `REVISÃO=APROVADO`, alterar status de etapa, criar/vincular documentos ou iniciar serviços sem ferramenta real, permissões adequadas e leitura de retorno. Não declarar que o criador aprovou se não aprovou.
- Se a planilha estiver desconectada, manter o registro em resposta ou artefato local aprovado e sinalizar `SINCRONIZAÇÃO PENDENTE`; não simular gravação.
- A aprovação do roteiro **não autoriza publicação** nem o uso de mídia sem direitos; render e QA audiovisual têm gates próprios. O criador pode revogar ou pedir mudanças, reiniciando as revisões afetadas.
- F10 é um **contrato de decisão**, não um teste integrado real do fluxo Drive/Sheets/Remotion; estes permanecem nos itens de integração/QA do roadmap.
