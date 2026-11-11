---
name: diazverso-manutencao
description: "Use ao criar ou alterar skills, scripts, assets, estrutura e documentação do plugin Diazverso, mantendo conteúdo atual, contexto eficiente e referências íntegras."
---

**Protocolo obrigatório Diazverso:** antes de agir, aplicar `../diazverso-contexto-eficiente/SKILL.md`. Ler uma vez por sessão/versão e reutilizar o contexto válido; abrir somente a skill principal e as dependências necessárias.

# Manutenção do plugin e das skills

Aplicar `../diazverso-contexto-eficiente/SKILL.md` antes de agir. Trabalhar na fonte autorizada, verificar a versão corrente e preservar alterações do usuário.

## Escrever o estado atual

- Substituir diretamente a instrução ou implementação pelo comportamento vigente. O conteúdo distribuído deve ensinar apenas como o produto funciona.
- Não adicionar datas de alteração, cronologia, changelog, números de tarefas, relatórios de construção, comparações de versões ou cópias paralelas. Registrar a versão em `plugin.json`.
- Preservar dados de negócio necessários, como data real de publicação, timestamps de mídia, revisões de fonte e copyright/licenças. Eles não são histórico de implementação.
- Remover arquivos e referências sem uso. Renomear componentes pelo propósito atual; não manter aliases ou adaptadores de compatibilidade sem requisito do produto.

## Criar uma skill útil

1. Reutilizar uma skill existente quando atender ao mesmo resultado. Criar outra somente se houver responsabilidade distinta.
2. Usar pasta e frontmatter `name` coincidentes, em kebab-case, e `description` com resultado e gatilhos concretos.
3. Incluir, logo após o frontmatter, o protocolo obrigatório de contexto usado pelas demais skills. Não duplicar toda a política.
4. Manter o corpo curto: entrada, ação, saída e limites. Separar detalhe condicional em referências indicadas por quando consultá-las.
5. Scripts devem executar uma função necessária, sem instalação, publicação, acesso ou sucesso presumidos. Preservar direitos e consentimento para serviços externos.
6. Manter uma fonte por decisão e registrar dependências por caminhos reais. Regenerar o mapa de skills e verificar que a nova skill pode ser encontrada.
7. Executar validação proporcional em ambiente isolado; entregar somente recursos operacionais e ferramentas de manutenção necessárias, sem fixtures, renders de demonstração ou relatórios de execução.
8. Atualizar a versão e salvar pela fonte GitHub do plugin. Não instalar automaticamente.

Com a fonte local disponível, `scripts/validate_plugin.py` valida o pacote e `scripts/build_plugin.py` o constrói. Esses utilitários ficam na raiz do repositório. Respeitar as instruções do host e do criador acima desta política.
