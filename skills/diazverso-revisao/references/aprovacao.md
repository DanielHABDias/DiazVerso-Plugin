# Diazverso — Gate editorial de roteiro e packaging (script-approval)

**Objetivo:** impedir que uma produção entre em edição como se roteiro, fatos e promessa estivessem aprovados quando ainda há pendências. Esta skill organiza decisões e evidências; **não concede permissão para publicar, renderizar ou alterar Google Sheets**.

## Entradas

- Identificação estável `VD_####` ou `SH_####`, tipo e versão/data do roteiro, com URL do Google Doc nativo se existir e puder ser lido.
- Tese e promessa, títulos A/B, conceito de thumbnail, gancho, payoff e revisão da embalagem.
- Relatórios aplicados **ao mesmo roteiro/versão** das revisões facts (fatos/fontes), structure (estrutura/ritmo) e voice (voz). Uma skill existente sem relatório **não conta como revisão executada**.
- Decisão explícita do criador sobre versão final do roteiro e escolha do packaging. Não inferir consentimento pelo silêncio, por links existentes ou por resultado positivo de ferramenta.

## Checklist de aprovação

1. **Identidade e versão:** confirmar que roteiro, ID da produção, tipo LONGO/SHORT e revisões se referem à mesma versão. Se o texto mudou depois de uma revisão material, reabrir a revisão correspondente.
2. **Fatos e fontes:** nenhuma alegação material pendente ou contestada sem correção/qualificação. facts registrada com referências rastreáveis ou bloqueios explicitamente resolvidos.
3. **Estrutura:** gancho conecta-se à tese, progressão permite compreender a história, redundância controlada e payoff responde à promessa. structure registrada; não confundir estimativa editorial com retenção real.
4. **Voz:** voice registra texto conversado PT-BR, opiniões preservadas e humor natural sem copiar a fala de outro criador. Ausência de áudio não implica revisão vocal executada.
5. **Packaging:** título escolhido e thumbnail proposta combinam com o roteiro e a abertura. Divergências de promessa ou fatos abrem nova revisão. Aprovação de **conceito** não significa que a arte final já foi produzida.
6. **Documentos e links:** confirmar Doc nativo formatado, pasta correta e vínculo idempotente na linha da produção. Sem conexão ou leitura de retorno, registrar o limite e não declarar integração verificada.
7. **Decisão humana:** apresentar resumo objetivo com versão, itens revisados, pendências e pergunta de aprovação. Somente confirmação inequívoca do criador para esta versão permite status `APROVADO PELO CRIADOR`. Uma revisão feita pela IA pode apenas recomendar aprovação.

## Estados e saída obrigatória

- `PENDENTE DE REVISÃO`: relatório facts/structure/voice ou packaging ausente, desatualizado ou bloqueado.
- `PRONTO PARA APROVAÇÃO HUMANA`: todos os critérios editoriais verificados sem pendências materiais, mas falta decisão explícita do criador.
- `APROVADO PELO CRIADOR`: há decisão inequívoca registrada com ID e versão; somente então liberar **planejamento** de decupagem/edição, condicionando execução real aos recursos e permissões.
- `REPROVADO/DEVOLVIDO`: ajustes solicitados; reabrir as revisões afetadas e não avançar como se aprovado.

Entregar um registro conciso:

| Campo | Valor obrigatório |
| --- | --- |
| Produção/versão | ID, tipo, data/identificador do roteiro |
| Revisão factual facts | estado + evidência |
| Estrutura structure | estado + evidência |
| Voz voice | estado + evidência |
| Packaging | título/thumbnail/gancho/payoff e estado |
| Pendências | bloqueios e o que falta verificar |
| Decisão humana | texto/data da aprovação específica ou `AINDA NÃO APROVADO` |
| Próximo passo | correção, pedido de aprovação ou planejamento técnico |

## Segurança e transições

- Jamais escrever `REVISÃO=APROVADO`, alterar status de etapa, criar/vincular documentos ou iniciar serviços sem ferramenta real, permissões adequadas e leitura de retorno. Não declarar que o criador aprovou se não aprovou.
- Se a planilha estiver desconectada, manter o registro em resposta ou artefato local aprovado e sinalizar `SINCRONIZAÇÃO PENDENTE`; não simular gravação.
- A aprovação do roteiro **não autoriza publicação** nem o uso de mídia sem direitos; render e QA audiovisual têm gates próprios. O criador pode revogar ou pedir mudanças, reiniciando as revisões afetadas.
- script-approval é um **contrato de decisão**, não um teste integrado real do fluxo Drive/Sheets/Remotion; estes permanecem nos itens de integração/QA do roadmap.
