# Diazverso — desenvolvimento do plugin

Este arquivo orienta a construção e será removido somente no fechamento da V1.
O estado atual e as evidências estão em `docs/REGISTRO_EXECUCAO_E_PENDENCIAS.md`;
os critérios e pendências estão em `docs/ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md`.
Contagens e bloqueios dos handoffs antigos são históricos, não o estado atual.

## Antes de agir

- Conferir branch, HEAD, alterações locais e CI; preservar trabalho mais novo.
- Ler o estado consolidado e somente o item/skill necessário. Aplicar
  `skills/diazverso-contexto-eficiente/SKILL.md`; técnicas avançadas e M01 sob demanda.
- Priorizar uma entrega funcional vertical; reutilizar implementações e testar
  conforme risco. Não criar relatórios por subpasso nem repetir verificações sem motivo.
- Prosseguir autonomamente nas tarefas elegíveis; registrar bloqueios reais sem
  falsificar integração, telemetria, render, permissões ou aprovação humana.

## Decisões que prevalecem

- Publicação exclusivamente manual pelo criador. O plugin termina no kit revisado;
  não implementar/importar envio, postagem, agendamento ou instruções de como postar.
  Registro posterior em Sheets somente com URL/data/publicação reais verificadas.
- Não instalar o plugin no ChatGPT/Codex durante desenvolvimento. Gerar/testar o
  pacote; o criador instalará pessoalmente após conclusão e limpeza da V1.
- Plugin antigo e Content Lab antigo são obsoletos. Content Lab não é dependência;
  sua refatoração é posterior. TSX antigos somente como referências seletivas.
- Nox canônico: `assets/brand/nox/Nox.png`. Preservar bytes/identidade; nunca
  apresentar imagem genérica como asset oficial. Poses novas exigem comparação visual.
- Preservar fatos versus opinião, voz PT-BR natural e identidade HQ madura.
  Especificação: `docs/ESPECIFICACAO_CANONICA_DIAZVERSO_V1.md`.
- Integrações Google usam IDs descobertos da instalação e ferramentas autorizadas,
  sem credenciais embutidas. Testes só em estrutura isolada; readback e idempotência
  obrigatórios. Escritas com reserva de IDs exigem escritor único coordenado;
  `sheets_batch.py` não oferece lock distribuído. Não seguir Config herdada de cópia.
- Avaliar especialistas pelo mérito; consultar
  `docs/CATALOGO_SKILLS_PRIORITARIAS_E_IRIS.md` ao selecionar motion/QA/thumbnail.
  Copiar/modificar/redistribuir terceiros só com autorização verificável e avisos
  preservados. Ausência de licença não impede avaliação, nem autoriza redistribuição.
- Não enviar áudio a serviços externos sem consentimento específico.
- Exclusões de dados reais ou outras ações destrutivas precisam de autorização
  pertinente. Não excluir documentos temporários até toda V1 passar nos critérios;
  migrar regras úteis e testar referências/pacote antes da limpeza final.
- Atualizar a fonte de estado e o roadmap por entrega; não propagar o mesmo texto
  em vários handoffs. Não anunciar V1.0 enquanto restarem gates sem comprovação.
