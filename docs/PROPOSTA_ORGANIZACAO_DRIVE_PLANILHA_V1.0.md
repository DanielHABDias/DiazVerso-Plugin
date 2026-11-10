# Diazverso 1.0 — Auditoria do Drive e da planilha + proposta de organização

> **ESTADO: PROPOSTA PARA DISCUSSÃO (NÃO APROVADA, NÃO IMPLEMENTADA)**
>
> Auditoria realizada em **2026-11-10**, com leitura da conta Google Drive conectada, da planilha nativa **Canal do YT**, da árvore de pastas e de roteiros representativos. O usuário pediu avaliar/refatorar essa organização e depois convertê-la em procedimentos operacionais do plugin.
>
> **Nenhuma pasta, planilha ou documento do Google Drive foi criado, movido, excluído ou alterado durante a auditoria.** Este documento preserva fatos lidos e sugestões em níveis separados. O conteúdo da planilha e os arquivos originais devem ser preservados com backup/cópia antes de qualquer migração. Não incluir credenciais, emails privados nem informações de compartilhamento identificáveis em specs distribuídas.

## 1. Fontes auditadas (estado real no Drive)

- Planilha [Canal do YT](https://docs.google.com/spreadsheets/d/1s_7ybuYet0La5_cem01p_UwTNzN2uIq5vfLAgWEF_s8/edit) — aba/dados reais lidos; arquivo com acesso compartilhado e permissões de terceiros. **Não presumir propriedade exclusiva nem mover sem confirmar acesso e autorização**.
- Pasta [Roteiros](https://drive.google.com/drive/folders/12ItRg3s5324YcggyM3J8Swz7ckvnF9jd), atualmente com `Exemplos/`, `Longos/`, `Shorts/`.
- Pasta [Thumbnail](https://drive.google.com/drive/folders/1O2MuY4p-Sz-x_m9wJioMxY7GL9MzCrZ9), atualmente com `Videos Longos/`, `Shorts/`, e PNGs de fundo/moldura na raiz.
- Na pasta de roteiros longos há **8 subpastas por vídeo** `VD_0001` a `VD_0008`; na de Shorts, **25 subpastas** `SH_0001` a `SH_0025`.
- Em thumbnails longas há **8 subpastas** por vídeo, e em Shorts **14 subpastas**.
- Exemplo real de longo: [VD_0008 — Roteiro aprovado](https://docs.google.com/document/d/1HJfwgMhwi9tt-gWKhzrYfPNA5ISxVeGsbqezBRRhips/edit), com `TITLE`, `HEADING_1` e `HEADING_2`, packaging, convenções audiovisuais, blocos de NARRAÇÃO/SOM DA CENA, revisão/gates e fontes.
- Exemplo histórico de longo: [RT_0004](https://docs.google.com/document/d/1HDrvcXMamTH8ibAkffRWz2rLBPaxuyIlzM0CgkSZJDU/edit), com estrutura de capítulos e fontes, mas convenções audiovisuais/empacotamento organizados de modo diferente.
- Exemplo de short: [SH_0025 — Roteiro](https://docs.google.com/document/d/16W-upZQEtzG4WLlvqq4gH9RMQzIvCyaujKvJPs8C3IY/edit), com gancho, prova, payoff, momentos de SOM DA CENA, CTA, estimativa de duração, notas de revisão e fontes.
- Há também pastas antigas de `Assets`, `IA`, `NOX`, `Sounds`, `Backgrounds`, e materiais de skills/edição. **Não migrar automaticamente** para Drive V1.0; a visão do criador é manter assets técnicos estáveis no futuro plugin/repositório, sujeito a inventário e licenças.

## 2. Diagnóstico concreto da planilha

Abas atuais encontradas:
| Aba atual | Observação verificada | Proposta |
| --- | --- | --- |
| **Procedimentos** | 9 instruções e justificativas sobre YouTube e postagem; algumas são generalizações/hipóteses não verificadas (ex.: aguardar 30–60 min como não listado para distribuição, “RPM aumenta” ao inserir links de afiliado). | **Não manter como aba operacional.** Arquivar registro histórico; validar práticas relevantes nas fontes oficiais e transferir apenas as aprovadas para skill/checklist do plugin. |
| **Referências** | 13 canais nomeados; 10 URLs de pastas com exemplos; várias linhas residuais com conteúdo genérico repetido. O criador informa que não a utiliza. | **Não manter no novo workbook.** Guardar legado separadamente se necessário, sem apagar; pesquisas e referências ficam sob demanda e no repositório de conhecimento/briefing. |
| **Videos Longos** | 13 colunas (ID, contexto, títulos A/B, thumbnails A/B, roteiro, descrição, comentário, tags, descrição social, link final, finalizado). 29 IDs prealocados; **8 com conteúdo preenchido e TRUE**, **21 linhas-placeholder com FALSE**. Descrições extensas ocupam células. | Migrar dados relevantes para **Produções** com tipo `LONGO` e estado da produção. Remover linhas-placeholder e separar grandes blocos de publicação para documento/kit por projeto. |
| **Shorts** | 10 colunas; 49 IDs prealocados; **25 com conteúdo preenchido e TRUE**, **24 placeholders FALSE**. Descrições e tags também ocupam células; alguns têm thumbnail, outros não. | Migrar para a mesma aba **Produções** com tipo `SHORT`; campos opcionais de thumbnail A/B e `video_origem_id`. |
| **Temas futuros** | 15 ideias com IDs `TF_....`, tese, justificativa, timing e status `IDEIA`. Alguns textos já mencionam IDs de vídeos longos produzidos (ex.: `VD_0008`), gerando risco de duplicação/status desatualizado. | **Preservar como aba `Ideias` separada**, para não poluir produção com brainstorms e permitir conversão controlada para projeto real. |

**Diagnóstico:** a planilha atual contém valor real, inclusive títulos A/B, links, roteiros e temas, mas acumula colunas longas, IDs vazios pré-criados, campos de status `FINALIZADO` pouco expressivos, redundância entre ideias e produções e abas que o criador não utiliza. **Não apagar dados existentes**; criar modelo novo e fazer migração com mapeamento e conferência.

## 3. Estrutura enxuta proposta para o Drive

**Objetivo do criador:** guardar principalmente **roteiros e thumbnails**; deixar regras, SFX, backgrounds, Nox e TSX canônicos no plugin/repositório quando adequado. Uma única planilha operacional é exceção útil e fica na raiz da estrutura.

```text
Diazverso/
├── Canal do YT — V1.0               [Google Sheets]
├── Roteiros/
│   ├── Longos/
│   │   ├── VD_0008 — Carnificina — Roteiro   [Google Doc]
│   │   └── ...
│   └── Shorts/
│       ├── SH_0025 — Carnificina — Roteiro   [Google Doc]
│       └── ...
└── Thumbnails/
    ├── Longos/
    │   ├── VD_0008_A.png
    │   └── VD_0008_B.png
    └── Shorts/
        ├── SH_0025.png
        └── ...
```

- **Mudança proposital:** remover o nível de *subpasta por vídeo* da estrutura **nova**; identificadores e nomes dos arquivos já permitem localizar cada item, e a planilha armazena seus links. Não mover pastas existentes antes da migração aprovada e verificada.
- **Nomeação:** `VD_####` para longo e `SH_####` para Short; permitir `TF_####` apenas para ideias até promoção. Manter IDs históricos; não renumerar e não reciclar.
- **Thumbnails:** A/B somente quando houver alternativas; Short sem thumbnail dedicada não recebe arquivo fictício.
- **Sem pastas de guia de edição/revisores no Drive novo.** Skills, templates e padrões técnicos vão para o repositório instalável (após auditoria). Para arquivos antigos, preservar um caminho de arquivo legado acessível, sem apagar automaticamente nem misturar com nova produção.
- **Localização:** usar IDs reais de pasta e planilha na configuração **por conta/instalação**, jamais copiar IDs da conta atual como se fossem globais. Encontrar por marcador/configuração antes de buscar nome; em colisão, pedir seleção em vez de criar duplicata. 

## 4. Modelo proposto da planilha — poucas abas operacionais

**Abas recomendadas:**

1. **Produções** — tabela principal **única**, agregando longos + Shorts, com campo `TIPO` (LONGO/SHORT) e filtros/views por formato. Não duplicar o mesmo vídeo em duas abas e manter um único ciclo de status; os campos específicos do formato ficam opcionais.
2. **Ideias** — fila de pautas ainda não promovidas à produção, com tese, motivação, prioridade, origem, timing, referências e status. Quando aprovada, cria `VD_####` ou `SH_####`, grava `PRODUCAO_ID` nesta linha e altera o status para `CONVERTIDA`, sem duplicar a pauta como item ativo.
3. **Afiliados** — produtos/serviços úteis, nicho/aplicabilidade, link afiliado, plataforma, estado (ATIVO/PAUSADO/EXPIRADO), revisão de link, texto breve seguro e regras de divulgação. Usar apenas itens realmente pertinentes ao vídeo; não inserir todos em toda descrição.
4. **Config** — pequena aba técnica **oculta/protegida** com versão do esquema, identificador da estrutura Drive, IDs de pastas, IDs da planilha, opções de formato, última migração; criada pelo instalador e administrada cuidadosamente.

**Não criar automaticamente:** `Procedimentos`, `Referências` e `Painel`/dashboard. O painel pode ser adicionado depois, se houver uma necessidade concreta de acompanhamento, sem poluir a operação inicial.

### 4.1 Produções — campos essenciais para o agente

| Grupo | Campos propostos |
| --- | --- |
| Identidade | `ID`, `TIPO`, `TEMA`, `TESE_RESUMIDA`, `IDEIA_ORIGEM_ID`, `VIDEO_ORIGEM_ID` (Short derivado) |
| Fluxo | `STATUS`, `PRIORIDADE`, `DATA_PLANEJADA`, `DATA_PUBLICACAO` |
| Packaging | `TITULO_A`, `TITULO_B`, `THUMB_A_URL`, `THUMB_B_URL` |
| Artefatos | `ROTEIRO_URL` (único Google Doc estruturado), `LINK_YOUTUBE` |
| Revisão | `QA_ROTEIRO`, `QA_VISUAL`, `QA_AUDIO`, `APROVACAO_FINAL` — podem ser resumidos em `QA_STATUS` + link para relatório no documento se ficar larga |
| Publicação | `PACK_PUBLICACAO_URL` **opcional** se pacote estiver no mesmo roteiro; descrições/tags/comentário ficam como seção final **não narrada** do Doc, não textos gigantes na planilha |

**Ajuste de minimização:** se demasiadas colunas prejudicarem a leitura, reduzir a `QA_STATUS` e tratar detalhes dentro do Google Doc; manter filtros, agrupamentos e notas do Sheets. Planilha deve funcionar como **índice operacional**, não como depósito de textos longos.

**Status produção sugeridos:** `PLANEJADO` → `PESQUISA` → `ROTEIRO` → `REVISAO_ROTEIRO` → `ASSETS` → `EDICAO` → `REVISAO_FINAL` → `PRONTO` → `AGENDADO` → `PUBLICADO`; exceções `PAUSADO`/`CANCELADO`. Não presumir que publicar significa apenas bool TRUE, nem retroagir status de vídeos antigos sem evidência. **Refinar os nomes conforme processo real aprovado.**

**Status ideias sugeridos:** `IDEIA`, `PESQUISAR`, `VALIDADA`, `CONVERTIDA`, `DESCARTADA`. As 15 ideias existentes com status IDEIA precisam ser cruzadas com vídeos já produzidos antes da migração.

### 4.2 Ideias — campos propostos

`ID`, `TEMA`, `TESE`, `TITULO_PROVISORIO`, `THUMB_CONCEITO`, `MOTIVO/DEMANDA`, `PRIORIDADE`, `TIMING`, `ORIGEM`, `STATUS`, `PRODUCAO_ID`, `OBSERVACOES`.

**Separar ideias é intencional:** hipótese sem compromisso editorial não deve virar automaticamente uma linha de produção com dez colunas vazias. Ao promover, o identificador de ideia continua rastreável no registro de produção.

### 4.3 Afiliados — campos propostos

`AFILIADO_ID`, `PRODUTO`, `CATEGORIA`, `PLATAFORMA`, `LINK`, `APLICAVEL_A`, `STATUS`, `ULTIMA_VERIFICACAO`, `OBSERVACAO`, `DIVULGACAO_NECESSARIA`.

**Cuidados:** não guardar senhas, cookies, tokens ou credenciais na planilha; verificar validade e pertinência de links; texto publicitário e aviso de afiliado de acordo com plataforma e regras locais. A mera presença do link não prova efeito em RPM ou recomendação.

### 4.4 Formatação nativa esperada (não é opcional na futura implantação)

- Cabeçalho congelado, filtros, formato de tabela legível, colunas com largura apropriada, células longas com quebra controlada, cores de estado discretas e legendas.
- Validação de `TIPO`, `STATUS`, `PRIORIDADE`, `QA_STATUS` e `AFILIADOS.STATUS` com dropdowns; datas como datas e links como links.
- Inserção **sob demanda**, com geração incremental de IDs livres; **não criar 20–50 placeholders** `VD_XXXX`/`SH_XXXX` com `FALSE`.
- Uma linha = um vídeo real / ideia real; `upsert` por ID e checagem de URL/duplicata antes de inserir; não sobrescrever dados do usuário.
- Preservar fórmulas/validações, limites, filtros e linkagem com Docs/Drive. Configuração da aba oculta nunca deve ser usada para armazenar credenciais.

## 5. Modelo de roteiro Google Docs — template com formatação real

**Referências reais:** o `VD_0008` e `SH_0025` apresentam boa estrutura audiovisual, com estilos nativos de título e subtítulos; o `RT_0004` mostra variação de convenções. O novo template deve padronizar os melhores elementos sem impor detalhes editoriais da antiga versão ao Diazverso 1.0.

Estrutura proposta de um documento único por vídeo:
1. **Cabeçalho** (`TITLE`): `[ID] — [tema/título de trabalho] — roteiro`, formato, status e links para planilha.
2. **Briefing e packaging** (`HEADING_1`): tese/pergunta, promessa, público, título A/B, ideia de thumb A/B, referências essenciais.
3. **Roteiro audiovisual** (`HEADING_1`): capítulos em `HEADING_2` e trechos sinalizados `NARRAÇÃO`, `SOM DA CENA`, `MOTION/TSX`, `NOX`, `MEME/SFX`, `LEGENDA` (Short); cada indicação visual é uma **função** a executar, com duração estimada quando necessário.
4. **Abertura prioritária** (primeiros ~30 s longos; hook rápido adaptado em Shorts), valor/tese + Nox e ritmo visual quando adequado.
5. **CTAs** integrados ao corpo (longos) e final (Shorts), sem interromper artificialmente raciocínio.
6. **Fontes e verificações** (`HEADING_1`): fontes com URLs, fatos confirmados, interpretações e pontos pendentes.
7. **Checklist/revisões** (`HEADING_1`): roteiro, fatos, visual/áudio/legendas, conflitos, questões, aprovações e última versão.
8. **Kit de publicação — NÃO NARRAR** (`HEADING_1`): descrição YouTube, tags, comentário fixado, capítulos confirmados, chamadas de afiliados relevantes, descrição curta para outras redes. Não preencher timestamps de capítulos com `00:00` fictício; validar contra render.
- **Para Shorts:** foco em gancho, prova/revelação, payoff, CTA final, duração desejada ≥60s como preferência do criador, legendas 9:16 e ocultação em cartões puramente tipográficos.
- Estilos reais do Google Docs: `TITLE`, `HEADING_1`, `HEADING_2`, texto normal; espaçamento e formatação predeterminados; listas nativas, sem exigir prompt extra “formate o roteiro”.
- Novos roteiros criados **a partir de uma cópia de template aprovada** (em vez de texto cru sem estilos). Verificar documento criado, pasta destino e vínculo com a linha da planilha.

## 6. Provisionamento automático do plugin — especificação a implementar

**Com uma conta Google Drive conectada e permissão para escrita:**
1. **Discover:** procurar `Diazverso` na conta, preferindo IDs já ligados à instância; listar possíveis raízes e conferir estrutura por manifesto/versionamento. NÃO assumir que um nome igual prova ser a pasta certa.
2. **Validate:** verificar se `Roteiros/Longos`, `Roteiros/Shorts`, `Thumbnails/Longos`, `Thumbnails/Shorts` e planilha esquema esperado existem e são graváveis.
3. **Preview changes:** mostrar o que falta e **pedir autorização para criar/migrar**. Não criar estrutura silenciosamente em conta errada nem em Drive de terceiro; primeira configuração pode ser opt-in único e depois manutenção idempotente conforme permissões.
4. **Create missing only:** criar exclusivamente as pastas/planilha realmente faltantes, a partir de template de Sheets versionado; incluir dropdowns, colunas, cores, filtros e `Config`.
5. **Bind:** gravar/configurar IDs reais da pasta/planilha na configuração do plugin por usuário/instalação; em novos ambientes, localizar a instância já criada. Não armazenar segredos no repositório.
6. **Operate:** ao criar ideia, registrar `Ideias`; ao aprovar, alocar `VD_####/SH_####`, criar roteiro formatado no local certo, atualizar `Produções`, pesquisar assets externos e criar thumbnail A/B na pasta apropriada. Reutilizar o mesmo ID em todos os artefatos.
7. **Verify:** ler de volta links, pastas, Doc e linhas alteradas; em erro de permissão, conexão ou gravação, indicar falha claramente; evitar duplicação em retry.
8. **Migrate:** manter backup da planilha antiga e links; não apagar/mover/renomear originais ou materiais compartilhados até comparação e autorização explícitas.

**Capability boundary:** skill apenas descreve fluxo; leitura e criação dependem das ferramentas disponíveis ao ChatGPT comum, Work/Codex ou MCP Content Lab. Não afirmar funcionamento automático quando integração não existe. Identificar recursos reais no momento da tarefa.

## 7. Plano seguro de migração dos conteúdos reais

**Sem alterações no Drive até aprovação da proposta.** Ordem recomendada:
1. Capturar snapshot/export da planilha atual e inventário de 8 longos + 25 Shorts com conteúdo, 15 ideias e respectivos links, e das 9 instruções e 13 referências legadas.
2. Criar **pasta raiz e planilha V1.0 como cópia nova**, preservando a original compartilhada. Configurar `Produções/Ideias/Afiliados/Config`.
3. Migrar 8 longos e 25 Shorts reais, sem 21+24 placeholders. Manter IDs, links do YouTube e referências dos Docs e thumbs. Decidir se copiar/mover os 33 Docs e imagens para a nova hierarquia em operação posterior.
4. Importar 15 ideias em `Ideias` e resolver manualmente vínculos/deduplicação com vídeos já feitos; registrar `PRODUCAO_ID`.
5. Extrair produtos atuais das descrições de vídeo para **Afiliados** somente após verificar seus links e relevância; não publicar automaticamente.
6. Padronizar template para **novos** roteiros. Os Docs históricos com diferentes convenções podem permanecer como histórico; não reescrever conteúdo inteiro sem necessidade.
7. Validar contagens, IDs, links, status e diferenças; usar teste completo: criar uma ideia, promover a produção, gerar Doc formatado, registrar thumbnails, atualizar status e publicar pacote.
8. Só depois decidir arquivamento/remoção de abas antigas e pastas legadas. Não realizar operações destrutivas como limpeza automática.

## 8. Perguntas de aprovação (para quando o criador revisar)

- Confirmar **uma aba `Produções` com filtros de formato** versus manter duas abas físicas; recomendação técnica é **uma** para reduzir duplicação.
- Confirmar **`Ideias` separada**; recomendação é **sim**, pois não são projetos aprovados.
- Confirmar **`Afiliados`**; recomendação é **sim**, por ser referência operacional dinâmica de publicação.
- Confirmar roteiros com o **kit de publicação ao final do mesmo Google Doc** para manter Drive restrito a Docs e thumbs.
- Confirmar eliminar subpastas individuais por vídeo **da nova estrutura**, com IDs em nomes de arquivo e vínculos na planilha.
- Confirmar criação de **nova planilha V1.0** em vez de editar no lugar a antiga compartilhada; recomendação é **nova + migração assistida**, preservando original.

## 9. Para usar no futuro plugin

Este é um **rascunho arquitetural de operação**, não a versão aprovada. Quando o criador aprovar, extrair:
- `docs/drive-layout.md` — layout canônico e convenção de nomes
- `schemas/channel-sheet-v1.*` — abas, colunas, tipos, estados, validações
- `templates/roteiro-longo.*` e `templates/roteiro-short.*` — estrutura e estilos reais
- `skills/drive-provisioning/SKILL.md` e `skills/youtube-ops/SKILL.md` — descoberta idempotente, criação consentida, manutenção e verificações
- Testes que simulam Drive sem estrutura, Drive com estrutura parcial, cópia compartilhada, duplicatas, permissões insuficientes, importação e migração.

**Proposta sujeita a ajuste:** continuar a discussão antes de tocar no acervo antigo ou congelar schema.