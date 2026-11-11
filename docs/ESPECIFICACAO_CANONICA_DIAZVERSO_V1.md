# Diazverso 1.0 — Especificação canônica mínima

> **10/11/2026 — A02.** Fonte curta para implementar o novo plugin. Distingue **decisões aprovadas** de **direção criativa ainda refinável**. Não constitui confirmação de instalação, render ou publicação.

## 1. Precedência das fontes

1. **Instruções e decisões mais recentes do criador** nesta fase do projeto.
2. Este documento e o **contrato operacional aprovado** de Drive/Sheets.
3. Skills e artefatos já implementados e verificados no novo repositório.
4. Material histórico: plugin antigo e Content Lab antigo, **obsoletos**. Servem apenas para recuperar exemplos seletivos, nunca para reimpor práticas.
5. Ideias, pesquisas e análises de terceiros são **hipóteses ou referência**, não requisitos automáticos.

A identidade criativa ainda pode mudar por decisão do criador. Não transformar observações sobre vídeos externos em regras fixas de câmera/cortes sem inspeção dos arquivos originais.

## 2. Conteúdo e estilo — direção declarada pelo criador, ainda ajustável

- Canal **Diazverso**, em português brasileiro, sobre **heróis e universos associados** (Marvel, DC, Ben 10, quadrinhos, séries, cinema, animações e jogos).
- Buscar **tese, história, tensão, pergunta ou contradição** que dê motivo para acompanhar o vídeo. Argumentação e aprendizagem integrada à narrativa, sem virar aula ou lista sem propósito. Aplicação no mundo real **quando fizer sentido**.
- **Voz conversada**, informal, opinativa, natural, capaz de reclamar, ironizar e fazer humor contextual; nunca forçar piadas, bordões, gritos ou artificialidade de narrador épico.
- As referências **FALL (humor/conversa)**, **Um Nerd (tese/estrutura)** e **RunnyIA (fluidez/motion)** servem para estudar funções distintas; **não copiar a identidade ou concluir técnicas quadro a quadro não verificadas**.
- Embalagem: título A/B **realmente diferentes**, thumbnail legível e coerente com a promessa, gancho que cumpra o título. Não alegar taxas de CTR/retenção sem dados.

## 3. Direção visual e papel do Nox — ainda refinável

- **HQ contemporânea/madura**, painéis, textura/halftone, profundidade, câmera virtual, parallax e tipografia cinética com finalidade narrativa; evitar visual infantilizado ou balões de fala como padrão.
- **Nox** é mascote/personagem recorrente quando a cena justifica. **Referência canônica real**: `assets/brand/nox/Nox.png` no GitHub, PNG RGBA 1408×768, 415.179 bytes, presente no `assets/manifest.json`. Não redesenhar o personagem arbitrariamente; validar novas poses contra a imagem.
- **Anton** é referência tipográfica principal para impacto; fontes e versões precisam ser licenciadas/compatíveis antes de incluir um binário.
- A edição desejada é motion **Remotion/TSX**, combinando imagens com movimento/zoom/reframe, depth, clips autorizados, SFX/áudio e QA. Não afirmar que já há um renderizador executável só porque existe uma skill.
- Shorts: **9:16**, legendas sincronizadas por padrão exceto trechos exclusivamente textuais, CTA contextual no final, preferência editorial por **pelo menos 60 segundos** (não limite do YouTube).

## 4. Organização operacional aprovada — Google Drive e Sheets

```text
Diazverso/
├── Canal do YT — V1.0 (Diazverso) [Google Sheets]
├── Roteiros/{Longos, Shorts}/      [Google Docs diretos, sem pastas por vídeo]
├── Thumbnails/{Longos, Shorts}/   [arquivos diretos VD_#### / SH_####]
├── Assets/
├── Backgrounds/
├── Memes/
├── Músicas/
└── Sounds/
```

**Abas da planilha:** `Produções` (LONGO e SHORT), `Ideias`, `Afiliados`, `Config` (técnica, oculta).

- IDs permanentes: **TF_####** = ideia ainda não promovida; **VD_####/SH_####** = produção.
- Uma ideia que vira vídeo **sai de Ideias**, mas **só depois** de criar/confirmar o novo registro em Produções e seus vínculos. Falhas não podem perder a ideia; repetição não pode duplicar a produção.
- Roteiros são **Docs nativos formatados**, com hierarquia, narração e orientação audiovisual distinguíveis, fontes e seção final **Kit de publicação — NÃO NARRAR**.
- Em `Produções`, status publicados só com link/dado real. **Revisão aprovada não é sinônimo de publicado.** Afiliados só se forem relevantes, com divulgação apropriada.
- Não incluir IDs pessoais de Drive/Sheets em skills distribuídas. Cada instalação deve **descobrir, verificar e reparar idempotentemente**, com conexão e autorização; bibliotecas auxiliares opcionais.
- Contrato detalhado e estado real: [CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md](CONTRATO_OPERACIONAL_GOOGLE_DRIVE_E_PRODUCAO_V1.md). Bibliotecas: [ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md](ORGANIZACAO_BIBLIOTECAS_DRIVE_2026-11-10.md).

**Decisão posterior do criador — 11/11/2026: publicação estritamente manual.** A execução do plugin encerra com o **kit de publicação revisado**, entregue para o criador postar pessoalmente. Excluir skill antiga de postagem e **não desenvolver skill/API/browser/automação nem instruções de como postar**. O registro posterior de `PUBLICADO`, data e URL é apenas documentação factual após confirmação real da postagem manual; não faz parte de enviar o vídeo.

## 5. Plugin, revisão e execução — decisões aprovadas

- **Uma microtarefa por vez.** Definir entrada, entrega, testes/revisão e evidência; corrigir antes de marcar `[x]` no [roadmap](ROADMAP_CONSTRUCAO_PLUGIN_DIAZVERSO_1.0.md).
- O criador autorizou **continuidade automática** entre microtarefas elegíveis, sem solicitar a palavra “próximo”; **sem alegar trabalho em segundo plano** e sem avançar por gate bloqueado como se tivesse passado.
- **Carregamento progressivo de contexto:** metadados → skill principal → referências/arquivos estritamente necessários. Resumir resultados, não perder decisões, medições de tokens só se houver dados.
- **Skills externas selecionadas** serão incluídas fisicamente no plugin com dependências, atribuição e **licença válida de redistribuição**. Não redistribuir terceiros sem permissão. Registro: [TERCEIROS_E_LICENCAS.md](TERCEIROS_E_LICENCAS.md).
- **Nox.png físico** é necessário no pacote; conferir hash/ZIP e identidade visual. Música, SFX, memes, vídeos e backgrounds de terceiros requerem avaliação individual de direitos.
- **Plugin antigo e Content Lab antigo são obsoletos.** O novo plugin não depende da refatoração do Content Lab; **refatorar Content Lab somente após concluir e validar a V1.0**. Exemplo TSX antigo só após auditoria individual. Se uma futura integração exigir adaptador Content Lab, ele será **opcional, com contrato novo e testes próprios**, e não reintroduzirá dependências do projeto anterior na instalação do plugin.
- Ferramentas diferentes oferecem capacidades diferentes; **sem acesso a Drive, editor, render ou YouTube não alegar execução**. Registro de bloqueios: [REGISTRO_EXECUCAO_E_PENDENCIAS.md](REGISTRO_EXECUCAO_E_PENDENCIAS.md).

**Skills prioritárias e Iris:** avaliar especialistas externos (Remotion, GSAP, HyperFrames, Humanizer, Last30Days, Baoyu, QA e contexto) pelo seu valor comprovável. **Iris deve fornecer visão/inspeção de vídeos**; a identificação do aplicativo/interface exatos ainda precisa ser feita, não inventar API. Skills selecionadas vão dentro do plugin quando licenciadas; se não houver autorização, criar **skill Diazverso original** sem copiar material protegido. Ver [catálogo](CATALOGO_SKILLS_PRIORITARIAS_E_IRIS.md).

## 6. Estados e descarte controlado

**Produto ainda em construção.** B06 (ZIP validado no CI) foi concluída sem instalação, conforme decisão corretiva do criador; F06 e outras integrações seguem pendentes. **NÃO instalar no ChatGPT/Codex agora**; o criador instalará o ZIP manualmente após V1.0 completa, revisada e limpa.

O criador determinou que os **arquivos temporários de orientação** serão excluídos **somente após** V1.0 implementada, testada no desenvolvimento e revisada, **antes de o criador instalar manualmente** e com suas regras transferidas para documentos/skills canônicos. Não eliminar referências ainda ativas e preservar histórico Git.

**Princípio de mudança:** decisão posterior do criador atualiza este documento e as skills afetadas; histórico antigo não prevalece por padrão.
