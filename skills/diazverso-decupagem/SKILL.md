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

## Contrato de composição independente — H01

A decupagem aprovada pode ser exportada como **props JSON** portáteis para um executor Remotion/TSX separado. O contrato versionado está em `../../schemas/remotion-composition-v1.schema.json`; o validador stdlib está em `scripts/validate_composition.py`; há um **exemplo sintético, sem arquivos de narração reais**, em `examples/short-remotion-props.example.json`.

Campos do contrato: `production_id`, `script_version`, formato `LONGO` (1920×1080) ou `SHORT` (1080×1920), FPS, duração total em frames; catálogo de assets com caminhos **relativos ao projeto do editor**, tipos e direitos; cenas com início/duração em frames, objetivo, descrição visual, camadas/motion, cues de legenda e áudio (cues têm início **relativo à cena**); configuração de saída MP4/H.264. Cenas precisam ser contíguas e usar assets declarados e com direitos `APPROVED` — **não basta registrar o nome do arquivo para comprovar existência ou licença**.

Executar `python scripts/validate_composition.py examples/short-remotion-props.example.json` a partir da pasta desta skill (ou indicar caminho absoluto ao script). O retorno `VALID_CONTRACT` significa apenas props estruturados, nunca render confirmado. O executor independente traduz props em `<Composition>`, `<Sequence>`, `<Audio>` e componentes de motion, localiza os assets em seu próprio projeto, inspeciona visual e áudio, e só então produz vídeo. **Não existe dependência nem integração com o Content Lab antigo.** H03–H09 e L02/L03 abrangem componentes e render/QA reais.

## Componentes de motion — H03 e H04

Os componentes autorais estão em `references/motion/`, independentes do Content Lab antigo:

- `camera.tsx` — `DiazCamera` (Remotion): imagem estática com crop **cover**, zoom, pan/reframe e blur interpolado ao longo da cena. Informar dimensões **reais** do arquivo e duração da cena em frames. O deslocamento é limitado matematicamente ao crop disponível para **não expor bordas vazias**. Não substitui a inspeção do rosto/objeto importante no recorte.
- `parallax.tsx` — `DiazParallax`: fundo cobrindo o canvas e camadas PNG recortadas em posição e escala conservadoras, com movimento de profundidade. A primeira camada deve ser um **fundo opaco**, e os recortes precisam de transparência realmente verificada. Usar profundidade 0–1, sem garantir segurança se uma UI de plataforma encobrir elementos.
- `motion-math.mjs` — funções puras `coverGeometry`, `cropAndPan`, `parallaxGeometry`, sem React, testáveis com Node integrado. Cenários de borda em `tests/test_motion_math.mjs`; executar `node --test skills/diazverso-decupagem/tests/test_motion_math.mjs` a partir da raiz do plugin. O workflow executa o mesmo comando.

## Texto cinético — H05

Em `references/motion/kinetic-text.tsx`, `DiazKineticText` recebe palavras com `text`, `startFrame` e `durationFrames` **relativos ao início da cena**; faz entrada curta com posição/escala/opacidade, sem precisar de medições online. O módulo `kinetic-text-math.mjs` valida ordem, duração e não sobreposição; seleciona a palavra do frame atual e calcula contraste de cores sólidas `#RRGGBB` pelo método de luminância relativa WCAG. O componente exige no mínimo **4,5:1**, usa fundo **opaco** na caixa do texto e largura conservadora; a referência tipográfica é `Anton` **somente se fornecida legalmente pelo host**, com fallback sem redistribuir fontes.

Para testar: `node --test skills/diazverso-decupagem/tests/test_kinetic_text.mjs` na raiz do repositório. **7 testes Node passaram localmente em 11/11/2026 contra os bytes idênticos ao helper versionado** (Git blob `5937c5d50151ad517469200c8c703b8a42393c3d`); CI e compilação/render TSX ainda dependem do executor. A cor calculada não garante contraste de cada pixel de um frame renderizado; a inspeção real, legibilidade e sincronização ao áudio continuam em H09/L02/L03. Não inventar timestamps de palavras quando não houver áudio/timing conferido.

**Fronteira de validação:** os cálculos de cobertura podem ser testados offline, mas o componente TSX só será considerado visualmente revisado após executor Remotion independente (H09/L02) renderizar frames e confirmar crop, segurança, nitidez e Nox. Não afirmar que um componente foi renderizado quando houve apenas validação estática/numérica.

## Painéis de filme/TV com CRT — H06

O componente autoral `references/motion/crt-panel.tsx` (`DiazCrtPanel`) enquadra **um trecho já disponibilizado legalmente ao editor** numa moldura contextual de monitor, com scanlines perceptíveis, vinheta e reflexo discretos. Os parâmetros são conferidos por `references/motion/crt-panel-math.mjs`: arquivo relativo ao projeto, início/duração dentro do vídeo de origem aferido, dimensão de quadro, intensidade de scanlines, evidência textual da revisão de direitos e autorização **separada** para o áudio original, com volume controlado. Sem autorização para áudio, o trecho fica mudo; a narração/trilha principal são tratadas em outra camada.

**Obrigatório:** os campos `rightsStatus='APPROVED'` e `rightsEvidence` são informações inseridas **após decisão humana real**; o código não comprova licença nem garante enquadramento jurídico. Um clipe de terceiros marcado sem evidência ou com direitos pendentes não pode ser usado. Não importar filmes/séries de plataformas nem presumir permissão por serem referências editoriais. Ao executar Remotion, conferir se o vídeo realmente decodificou, se há áudio permitido, ausência de distorção e CRT perceptível nos frames finais. `tests/test_crt_panel.mjs` contém testes de parâmetros (não testes de render); CI os executará.

## Trilha e SFX por contexto — H07

`references/audio/audio-plan.mjs` contém `planAudio(catalog,scene,options)` para montar cues de trilha e efeitos sonoros por intenção da cena (ex.: tensão, descoberta, impacto), **a partir de um catálogo local previamente revisado**. Cada item precisa de ID, caminho seguro e relativo, tipo `music`/`sfx`, duração conhecida em frames, tags, `rights='APPROVED'` e evidência real de aprovação. Um campo preenchido não constitui verificação de licença; consultar a origem e autorização de uso antes de alimentar o catálogo. Itens pendentes não entram na composição.

Para música compatível com a duração da cena, o planejador separa intervalos de trilha e reduz o volume automaticamente nos trechos em que a narração está marcada (ducking); SFX podem ter início configurado dentro da cena. Todos os tempos são **relativos à cena e estimados a partir de entradas verificadas**. Se faltar música ou SFX válido, retorna `NEEDS_APPROVED_AUDIO` com as pendências e **não inventa mídia**. Testes de filtro, limites, ganho e cues estão em `tests/test_audio_plan.mjs`, incluídos no CI. O arquivo não escuta nem normaliza áudio e **não confirma mixagem ou sincronização real**; esses aspectos precisam de preview/render independente em H09/L02/L03.

## Trechos de render e previews — H08

O executor `scripts/render_previews.py` recebe um **JSON validado do contrato H01**, o caminho do entrypoint TSX de um **projeto Remotion independente**, o ID registrado da composição e um diretório de saída fora dos assets originais. Sem `--execute`, produz somente um **plano JSON e não grava arquivos**. Com `--execute`, exige `npx` e o Remotion **já instalado localmente no projeto do editor**, e executa, em ordem, um MP4 por cena pelo intervalo inclusivo `--frames=início-fim` e **até três PNGs de conferência** (primeiro, meio e último frame da cena) com `remotion still --frame`. Os comandos usam argumentos diretos, sem shell. Arquivos existentes não são sobrescritos e a primeira falha interrompe o lote.

Exemplo de uso a partir da raiz do plugin, **substituindo pelo projeto Remotion independente realmente existente**:

```bash
python skills/diazverso-decupagem/scripts/render_previews.py --props skills/diazverso-decupagem/examples/short-remotion-props.example.json --entrypoint /caminho/projeto-remotion/src/index.tsx --composition-id DiazversoShort --out /caminho/outputs
```

Acrescentar `--execute --project-root /caminho/projeto-remotion` **somente depois** de validar entrada, composição, licença dos arquivos e diretório, e ter o editor instalado. A CLI roda com esse projeto como diretório atual para resolver sua instalação local do Remotion; não instala pacotes automaticamente. A indicação `--project-root` é obrigatória na execução real. Os exemplos de assets/voz são ilustrativos e **não são garantia de arquivos presentes**. Um trecho de vídeo criado pelo CLI recebe estado `PREVIEWS_RENDERED_AWAITING_HUMAN_REVIEW`, não `APROVADO`; inspecionar quadros, legendas, câmera/Nox, música, SFX e cortes, corrigir e refazer quando necessário. Nenhum render final é iniciado pelo executor H08, e **nenhuma postagem é realizada**. `tests/test_render_previews.py` cobre fluxo de comandos usando um **CLI simulado**; sem executor Remotion real, não declarar que frames verdadeiros foram renderizados. H09/L02/L03 cobrem a validação audiovisual ponta a ponta.

## Revisão de ritmo e direitos — J05/J06

O revisor `scripts/review_pacing.py <cenas.json>` recebe `format` (`SHORT`/`LONGO`), `fps`, `total_frames` e cenas contíguas com `id`, `start_frame`, `duration_frames`, `role` (`HOOK`, `CONTEXT`, `EVIDENCE`, `TWIST`, `PAYOFF`, `CTA`, `BREATHER`), `narration` e `visual_change`. Sinaliza quadros longos sem mudança visual, ausência de payoff, CTA antes da conclusão, repetição **literal** de fala e preferência editorial de Short ≥60 s. O resultado fornece **achados verificáveis**, nunca previsão de retenção, causalidade, redundância semântica ou métricas de YouTube. **A pessoa responsável decide cada correção.**

O revisor `scripts/review_rights.py <direitos.json>` exige por asset ID, tipo, origem, status de direitos, base e **evidência real**, informação de crédito obrigatório, estado de revisão de Content ID e transformações. Para links afiliados, exige URL HTTPS, verificação **na produção atual** e divulgação clara. Direitos pendentes, origem sem comprovação e créditos obrigatórios faltando bloqueiam aprovação. `CRT`, espelhamento, cortes ou molduras **não concedem direitos autorais**. `Content ID: REVIEWED` é um registro de análise humana, **não prova ausência de reivindicações**; o código nunca consulta YouTube ou certifica licença.

Estes scripts são **pré-revisores de metadados**. A saída de J06 pode embasar o gate `direitos_midias` da J08, mas esse gate só pode ser marcado `APROVADO` após **conferência humana da procedência, direitos e evidências**. O retorno do programa nunca substitui essa decisão. Testes estão em `tests/test_review_pacing.py` e `tests/test_review_rights.py`; o workflow de pacote já descobre todos os testes Python desta pasta. Nenhum vídeo é postado ou ensinado a postar.

## Limites

- Não afirmar escuta de voz, renderização, sincronização medida, QA visual ou disponibilidade/licença de mídia sem execução/consulta efetiva.
- Não depender do Content Lab antigo; TSX/Remotion é trabalho de etapa posterior em runtime independente.
- O plugin **não posta vídeos nem explica como postar**. O criador publica manualmente; esta skill só prepara a edição.
