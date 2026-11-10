# Diazverso 1.0 — Skills de referência prioritárias e integração Iris

> **Briefing explícito do criador em 10/11/2026.** Documento **temporário** para o Codex; migrar suas decisões para skills autorais, referências e configuração do pacote antes da limpeza final. Objetivo: **um plugin realmente excelente**, não uma coleção grande de skills sem função.

## Regras obrigatórias

1. **O plugin será criado e testado no repositório GitHub. NÃO INSTALAR no ChatGPT ou Codex durante o desenvolvimento.** O criador fará a instalação manual do ZIP **após** a V1.0 completa, revisada, limpa e validada.
2. **Selecionar skills excepcionais por função real, não por hype**: pesquisa/fatos, títulos, thumbnail, roteiro, Nox, motion/Remotion, tratamento de vídeo, música e SFX, legendas, QA visual/sonoro, publicação e contexto/tokens. Avaliar qualidade, precisão, manutenção, dependências, segurança, idioma, integração e desempenho de um exemplo reproduzível.
3. **Quando a licença autorizar redistribuição**, incluir **dentro de `skills/`** as skills externas aprovadas, com `SKILL.md`, referências/scripts/arquivos necessários, licença, autoria e registro de versão; não basta apontar para links externos. Checar scripts por chamadas externas/destrutivas antes de executar.
4. **GitHub público NÃO equivale a licença livre.** Se não houver autorização clara de cópia/redistribuição, **não copiar os arquivos** para o plugin. O Codex deve estudar a documentação pública e o funcionamento divulgado, extrair princípios e requisitos funcionais, comparar alternativas, e criar **uma skill Diazverso original, escrita do zero** para a mesma finalidade, sem reprodução de trechos protegidos, scripts/códigos ou estrutura criativa distintiva. Documentar fontes/decisões e validar exemplos.
5. **Carregamento progressivo:** skill principal por microtarefa; bibliotecas avançadas só quando a tarefa exige. Uma skill muito grande piora o consumo de tokens.
6. **Toda implementação exige revisão:** qualidade, licença, segurança, funcionalidade real, links e testes. Uma skill importada mas não executada ainda não é uma funcionalidade validada.
7. **Não usar Content Lab antigo como dependência.** Refatorar Content Lab somente depois do novo plugin 1.0; TSX antigos são referências seletivas.

## Catálogo para auditoria ativa (não é lista de skills já instaladas)

| Ferramenta/skill | Finalidade prioritária no Diazverso | Ação do Codex |
| --- | --- | --- |
| **Remotion Agent Skills oficiais** (`remotion-best-practices`, `remotion-create`, `remotion-markup`, `remotion-render`, `remotion-captions`, `remotion-multimedia`, `remotion-docs`) | Produção e QA de cenas TSX/React, composição horizontal/vertical, legendas, render e API correta | **Prioridade máxima para motion.** Ver [Remotion Agent Skills](https://www.remotion.dev/docs/ai/skills) e [repositório oficial](https://github.com/remotion-dev/skills). Verificar licença/condições de redistribuição e do próprio Remotion. Se incertas, criar skills **autorais equivalentes** a partir da documentação pública e testes; não copiar fonte sem permissão. |
| **Iris — inspeção visual de vídeos** | Permitir à IA **ver/analisar vídeo**, identificar falhas de frame, transições, Nox, legendas, ritmo e diferenças antes/depois de correções | **Requisito funcional prioritário do criador.** Ele já utilizou algo chamado Iris e suspeita ser **aplicativo, não skill**. O produto exato, repo e API/CLI **não foram identificados com segurança**; **não confundir com projetos homônimos achados por busca**. Investigar e confirmar o Iris correto, requisitos, conexão de host e se deve ser exposto por `plugin.json`/configuração. Se não integrável, criar **pipeline autoral de análise visual de vídeo** (extração de quadros/metadata/timestamps + IA multimodal disponível + relatório de achados + rechecagem), com capacidade verificada, sem fingir visão real. |
| **HyperFrames** | Animações, motion, render e verificação visual de composições | Localizar repo/ferramenta correta, versão, licença, exemplos e limitações; testar candidato versus Remotion antes de selecionar/incorporar ou escrever adaptador autoral. |
| **GSAP** | Timing de movimento, easings, transições expressivas, cinematografia HQ | Revisar APIs/licença/compatibilidade Remotion. Usar como referência técnica e criar cenas autorais quando apropriado; não embutir dependência sem condições claras. |
| **Humanizer** | Revisão de voz natural, reduzir tom robótico e preservar ironia/comentário do canal | Avaliar skill/repo e licenças; adaptar método ao PT-BR e ao Diazverso, sem copiar texto protegido. Revisor próprio com testes de antes/depois. |
| **Last30Days** | Pesquisa atual e sinais culturais de temas Marvel/DC/Ben 10 etc. | Investigar versão/cobertura/licença; criar protocolo de fontes e datas com ferramentas reais, sem simular acesso a tendências. |
| **Baoyu Cover Image** | Construção de thumbnail/capa legível, com promessa visual e variações A/B | Estudar técnicas e validação de contraste, enquadramento e Nox; produzir skill de thumbnail **autoral** quando necessário. |
| **Superpowers / Skill Creator / Plugin Creator** | Qualidade do desenvolvimento, planejamento pequeno, teste/revisão e skills de alta qualidade | Usar ferramentas oficiais disponíveis para **desenvolver** o pacote; incorporar só rotinas realmente necessárias **para usuário final** e que permitam redistribuição. |
| **Context Engineering / economia de tokens** | Carregamento progressivo, manutenção de decisões e custo de contexto | Já há `context-optimization` MIT dentro do pacote e `diazverso-contexto-eficiente` autoral. Medir efeito e testar antes de declarar melhoria. |
| **EarShot** | QA de áudio, clipping, música/voz/SFX, transições, sincronização | Investigar produto/licença/integração; não presumir que está conectado. Se ausente, criar QA próprio com análise de áudio e revisão auditiva. |
| **WATCH** | Inspeção visual ou acompanhamento multimodal conforme produto real | Identificar repo/produto com precisão antes de incorporar; comparar com Iris e evitar duplicação de funções. |
| **Browser Use** | Pesquisa com navegador, recursos e operações de interface onde permitido | Identificar integração/skill segura, permissões e registro; não criar automações destrutivas sem autorização. |
| **vidIQ** | Pesquisa de pautas, títulos e sinais de SEO YouTube | É integração opcional; usar dados acessíveis e não converter scores em garantias de CTR ou alcance. |
| **Openverse / Real SFX** | Busca de mídia/SFX apropriados, origem e permissões | Verificar licença **de cada arquivo** antes de importar e usar; não redistribuir assets automaticamente. |

**Não presumir que esses nomes tenham todos um único repositório ou sejam de fato 'skills'.** Registrar identificação, URL, licença, riscos, compatibilidade e resultado de teste de cada candidato. Se a fonte for desconhecida, marcar `IDENTIFICAÇÃO PENDENTE` — especialmente **Iris**.

## Skills externas JÁ presentes no repositório (não repetir importação)

- `skills/context-optimization` — licença MIT, referência.
- `skills/video-editing` — licença MIT, templates/scripts de edição.
- `skills/analyze-video-editing` — licença MIT; fork Diazverso exige autorização específica antes de upload externo de áudio.
- `skills/find-broll` — licença MIT; não garante licença das mídias encontradas.

Ver [TERCEIROS_E_LICENCAS.md](TERCEIROS_E_LICENCAS.md) para a auditoria de origem. **A presença do código não garante execução de FFmpeg/Node/Remotion nem instalação no host.**

## Passo a passo que o Codex deve usar para cada candidata

1. **Identificar precisamente** nome, fonte primária (repo + commit/tag), produto e função (skill, biblioteca, app ou serviço). **Iris primeiro como recurso de QA de vídeo.**
2. Ler README, `SKILL.md`, refs, exemplos e documentação externa; verificar licença de **cada componente relevante**, segurança e atribuição. GitHub público sem licença explícita = **não copiar código/texto** para distribuir.
3. Criar uma pequena matriz comparativa: valor real no Diazverso, possibilidade de integração, custo de contexto, dependências, licença, qualidade e manutenção.
4. **Se permitida:** incorporar somente skills realmente selecionadas e todos os arquivos necessários, preservar licença e autoria, remover redundâncias com cuidado, passar em auditoria de segurança.
5. **Se não permitida:** implementar skill **nova, original, funcional** a partir de requisitos e conhecimento geral/documentação pública; citar inspirações como bibliografia, mas não reaproveitar material proprietário.
6. Produzir **teste mínimo reproduzível** da finalidade: por exemplo, Remotion → compilar/render de uma cena; Humanizer → revisar texto; Iris → analisar frames reais/timestamps de um vídeo de teste; thumbnail → imagem e QA de legibilidade.
7. Registrar evidências, corrigir/revisar, marcar a microtarefa existente correspondente (G/H/I/J etc.) somente quando **todos** os seus critérios tiverem sido atendidos.

## Limites de implementação

- **Não empacotar as ferramentas externas inteiras** se só uma skill selecionada é relevante; manter plugin modular e enxuto.
- **Iris como requisito de capacidade e integração futura**, não como diretiva para adivinhar qual software instalar. Não criar campos inválidos em `plugin.json` ou secrets fictícios. Se houver integração real, adicionar a configuração válida e testada.
- **Não criar uma skill musical de composição própria**. O foco é **pesquisar/selecionar músicas prontas, conferir direitos, combinar à cena, mixar e revisar**; respeitar a direção atual do criador.
- **Release 1.0:** ZIP final com conteúdos reais e testados no GitHub. Só após finalização, o criador instala manualmente no ChatGPT.

**Limpeza:** este documento é transitório. Migrar critérios e resultados para skills, `references/`, `plugin.json`, templates e arquivos de licença/avisos antes de apagar os documentos de planejamento ao concluir V1.0.
