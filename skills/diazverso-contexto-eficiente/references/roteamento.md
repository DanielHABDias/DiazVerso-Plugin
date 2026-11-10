# Roteamento de skills por microtarefa — Diazverso 1.0

**Uso:** consultar somente se o agente precisar escolher entre skills semelhantes. Não carregar em toda interação.

## Regra de despacho

1. Classificar o pedido por **resultado esperado**, não só pelas palavras usadas.
2. Selecionar **uma skill principal** (responsável pelo resultado) e no máximo as auxiliares realmente indispensáveis.
3. Carregar metadados `name/description` primeiro. Ler o corpo da skill selecionada, depois referências somente quando a etapa exigir.
4. Se não existir skill específica ou ferramenta necessária, **não alegar execução**: realizar a parte informativa possível ou registrar um bloqueio.
5. Antes de trocar de etapa, revisar a entrega e salvar estado; não acionar outras skills sem objetivo.

## Responsabilidade primária atual

| Intenção concreta | Principal | Auxiliar somente se necessária |
| --- | --- | --- |
| Instalação, conexão ou diagnóstico | `diazverso-setup` | `diazverso-contexto-eficiente` se houver contexto excessivo |
| Identidade editorial, voz, posicionamento, tese | `diazverso-core` | Pesquisa externa com ferramenta disponível, se necessário |
| Orquestrar várias etapas de vídeo | `diazverso-criacao-video` **quando implementada e reconhecida** | A skill da etapa seguinte |
| Economia de contexto/planejamento de tarefas | `diazverso-contexto-eficiente` | `context-optimization` vendorizada para técnicas avançadas |
| Criação técnica, render, captions e som | Skill especializada **quando criada e validada** | Runtime Remotion real; não depender do Content Lab antigo |
| Google Drive/Sheets | Skill especializada **quando criada e validada** | Conector autorizado; não presumir acesso |
| Thumbnail e Nox | Skill especializada **quando criada** | Asset `Nox.png` físico verificado no pacote |

**Importante:** exemplos de skills ainda não implementadas são caminhos previstos, **não funções existentes**. Nunca listar skill ausente como disponível.

## Critério de revisão

- O pedido foi atendido pela habilidade mais específica disponível?
- Arquivos/referências realmente carregados foram estritamente necessários?
- Houve confirmação de capacidade, persistência e teste, quando aplicável?
- O resultado foi revisado antes da próxima microtarefa?
