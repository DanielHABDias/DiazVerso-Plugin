---
name: diazverso-decupagem
description: "Use para dividir roteiro aprovado de vídeo longo ou Short Diazverso em cenas executáveis, com narração, visual, música/SFX, duração, fontes e objetivo de cada bloco."
---

# Diazverso — Decupagem audiovisual

**Entrega:** tabela de cenas sequenciais derivada de **uma versão identificada do roteiro**, pronta para guiar edição TSX/Remotion independente. Não criar fatos novos nem presumir direitos de mídia. Se o roteiro ainda estiver pendente de aprovação, gerar apenas uma **decupagem preliminar** e indicar o gate.

## Um fluxo, sem burocracia

1. Obter ID `VD_####` ou `SH_####`, versão do roteiro, formato (16:9 ou 9:16), texto/narração, fontes e mídia disponível. Se não houver informação suficiente, trabalhar com referências visuais propostas claramente marcadas, sem afirmar arquivos encontrados.
2. **Separar por mudança de ideia/ação/ênfase**, não por frase ou por número fixo de segundos. Para cada cena, indicar a função narrativa: apresentar, demonstrar, comparar, criar tensão, revelar, respirar ou concluir. Dividir cenas estáticas longas somente se houver ganho de clareza.
3. Para cada cena, preencher: `cena_id`, `texto_narrado` (ou `SEM NARRAÇÃO`), `inicio_estimado_s`, `duracao_estimada_s`, `objetivo`, `quadro_alvo`, `camadas_movimento`, `fonte_asset`, `musica`, `sfx`, `texto_tela`, `legenda`, `direitos_status`, `risco_qa`.
4. **Imagem nunca meramente parada:** propor enquadramento/movimento útil (pan, zoom/reframe, parallax ou transição) quando fizer sentido, sem excesso. Evitar Nox repetitivo; usar seu arquivo canônico e variantes somente após verificação da identidade. HQ moderna, contraste e tipografia legível.
5. Usar música e SFX **por função e timing**; informar onde entram, saem ou têm ducking na narração. Não indicar arquivo como liberado sem licença verificada; marcar `PENDENTE DE DIREITOS` quando necessário. Não inserir trechos de terceiros só por aparência de CRT/moldura.
6. Para Short, encaminhar para `diazverso-shorts` e o preset `diazverso-shorts/references/preset-vertical-v1.json`: 1080×1920, zonas seguras e legenda sincronizada por padrão, exceto cena **exclusivamente de texto na tela**.
7. **Checar continuidade:** toda parte relevante do roteiro deve aparecer em uma cena; começo e fim de cada cena devem avançar sem tempos negativos/sobreposição acidental. Estimativas não são timestamps medidos do render. Conferir a duração real após narração/render; ajustar a decupagem no editor.
8. **Saída mínima:** tabela sequencial + breve lista de assets/direitos pendentes e cenas com maior risco de legibilidade/áudio. Não abrir um documento para cada cena. Gerar um JSON/TSX apenas quando houver executor ou implementação solicitada.

## Modelo enxuto de tabela

| Cena | Tempo estimado | Objetivo | Narração | Quadro/motion | Texto/legenda | Música/SFX | Asset/fonte e direitos |
| --- | --- | --- | --- | --- | --- | --- | --- |
| S01 | 0–4 s | Gancho | Trecho exato aprovado | Close/recorte com contraste | Legenda da fala | Impacto breve se aprovado | Fonte indicada ou PENDENTE |
| S02 | 4–10 s | Contexto | Próximo trecho aprovado | Painel HQ / reframe | Palavra-chave sem duplicar legenda | Ducking da trilha | Asset aprovado ou proposta |

Os tempos acima **são exemplos**, não um roteiro pronto nem um preset universal. Em uso real, montar cenas somente a partir da narração existente.

## Limites

- Não afirmar escuta de voz, renderização, sincronização medida, QA visual ou disponibilidade/licença de mídia sem execução/consulta efetiva.
- Não depender do Content Lab antigo; TSX/Remotion é trabalho de etapa posterior em runtime independente.
- O plugin **não posta vídeos nem explica como postar**. O criador publica manualmente; esta skill só prepara a edição.
