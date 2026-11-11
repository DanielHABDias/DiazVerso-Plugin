# Diazverso

Plugin para pesquisar pautas, criar e revisar roteiros, organizar Google Docs/Sheets, preparar thumbnails e Nox, planejar edição Remotion e entregar um kit para publicação manual.

## Uso

Acione uma skill Diazverso ou peça “vamos criar um vídeo para o Diazverso”. Todas as skills exigem o [protocolo de contexto eficiente](skills/diazverso-contexto-eficiente/SKILL.md): uma responsável principal, referências sob demanda, reutilização do que já foi conferido e retomada por checkpoint.

O [mapa de skills](skills/diazverso-contexto-eficiente/references/skill-map.json) permite navegar sem abrir todos os arquivos. Com Python disponível, a busca incremental retorna até três resultados por padrão:

```bash
python skills/diazverso-contexto-eficiente/scripts/context_map.py --root . --query "roteiro"
```

O índice descartável fica fora do plugin e reutiliza arquivos inalterados. Mudanças invalidam seus metadados. O grafo orienta a busca; Docs, Sheets e arquivos atuais continuam sendo as fontes de verdade.

## Requisitos

- Google Drive, Docs e Sheets conectados para operações nesses serviços.
- Executor com Python para os utilitários locais; Node, React e Remotion no projeto de edição para TSX/render; FFmpeg para inspeção audiovisual.
- Ferramenta de imagem para gerar artes e acesso às mídias com direitos conferidos.

As skills não fornecem essas conexões nem instalam dependências automaticamente. Componentes de motion estão em `skills/diazverso-decupagem/references/motion/`; a composição usa o executor do projeto de edição.

Nox canônico está em `assets/brand/nox/Nox.png`. Os WAVs originais em `assets/sfx/` têm integridade e sinal medidos, mas precisam de escuta/aprovação antes do uso editorial. Fundos procedurais HQ dispensam imagens adicionais.

## Instalação e manutenção

O manifesto portátil é `plugin.json`; a instalação é feita manualmente pelo criador no cliente compatível. O onboarding confere as capacidades presentes. As instruções são obrigatórias quando o Diazverso é acionado; a instalação não cria uma política global para conversas que não utilizem o plugin.

Para uso obrigatório no repositório aberto no Codex, `AGENTS.md` contém o ponto de entrada. Em outro workspace, a política desse workspace precisa acionar o Diazverso. O plugin não controla cache interno, raciocínio oculto ou métricas que o host não exponha.

`scripts/validate_plugin.py` confere estrutura, referências, assets, sintaxe e mapa. `scripts/build_plugin.py --output /caminho/fora/do/repositorio/diazverso.zip` gera o pacote. Essas ferramentas de manutenção não integram o ZIP instalado.

[Manutenção de skills](skills/diazverso-manutencao/SKILL.md) · [Licenças e atribuições](THIRD_PARTY_NOTICES.md)
