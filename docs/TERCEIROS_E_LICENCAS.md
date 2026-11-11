# Diazverso 1.0 — Skills externas, licenças e segurança

> Inventário de origem e direitos. A inclusão de uma skill no GitHub **não comprova** execução, segurança total ou compatibilidade no host. Atualizar a cada importação/patch.

## Incorporadas fisicamente (vendorizadas)

| Skill | Origem | Licença preservada | Arquivos incluídos | Situação |
| --- | --- | --- | --- | --- |
| `context-optimization` | [muratcankoylan/Agent-Skills-for-Context-Engineering](https://github.com/muratcankoylan/Agent-Skills-for-Context-Engineering/tree/main/skills/context-optimization) | [MIT](../skills/context-optimization/LICENSE) | `SKILL.md`, `references/optimization_techniques.md`, LICENSE | Fonte comparada e relida; execução no host ainda não verificada |
| `video-editing` | [gitethanwoo/video-editing](https://github.com/gitethanwoo/video-editing/tree/main/skills/video-editing) | [MIT](../skills/video-editing/LICENSE) | `SKILL.md`, scripts, templates TSX/Remotion, refs, testes, metadata e LICENSE | Copiado com conteúdo necessário; ferramentas FFmpeg/Node/Remotion exigem runtime, sem teste nesta sessão |
| `analyze-video-editing` | [gitethanwoo/video-editing](https://github.com/gitethanwoo/video-editing/tree/main/skills/analyze-video-editing) | [MIT](../skills/analyze-video-editing/LICENSE) | SKILL.md, scripts, refs, testes, metadata e LICENSE | **Modificação de segurança Diazverso**: áudio externo somente com `--allow-external-upload` e autorização específica; sem execução testada |
| `find-broll` | [gitethanwoo/video-editing](https://github.com/gitethanwoo/video-editing/tree/main/skills/find-broll) | [MIT](../skills/find-broll/LICENSE) | SKILL.md, refs, metadata e LICENSE | Requer verificação de licença, procedência e atribuição de cada mídia encontrada |

A licença MIT permite cópia e modificação com a manutenção do aviso; preservamos o arquivo `LICENSE` nas quatro skills. **Os materiais de vídeo de terceiros encontrados pelas skills NÃO são licenciados apenas por estarem em uma biblioteca**.

## Modificações no código importado

- `skills/analyze-video-editing/scripts/audio_listener.py`: adicionado **bloqueio de upload externo por padrão**. Sem `--prepare-only` ou `--allow-external-upload`, falha com instrução de obter consentimento. O flag não substitui autorização do usuário; o agente deve verificar a autorização antes de executá-lo.
- `skills/analyze-video-editing/SKILL.md`: exemplo mudou para `--prepare-only` e passou a exigir consentimento explícito para invocar serviço externo. O upstream por padrão podia enviar áudio com `GEMINI_API_KEY` disponível.
- Nenhuma execução Python/FFmpeg, requisição Gemini, `npm install` ou upload de áudio foi efetuada durante a importação. A verificação de segurança é **estática**, não teste de execução.

## Candidatas ainda não incorporadas

| Candidata | Situação | Decisão |
| --- | --- | --- |
| **Remotion skills oficiais** `remotion-dev/skills` | Em 10/11/2026, o repositório consultado não apresentou LICENSE raiz; questão pública de licença/redistribuição foi levantada. | **Não copiar o código original sem autorização clara.** Criar skills Diazverso autorais baseadas em documentação pública/fatos de API e pedir licença para vendorização, se necessário. São desejadas no pacote, mas redistribuição não deve ser presumida. |
| **OpenAI Skill Creator** | Instruções oficiais disponíveis no host; a skill de referência possui licença Apache-2.0 por arquivo. | Usar para desenvolvimento; só incorporar fisicamente se realmente necessária aos usuários finais, com LICENSE e dependências correspondentes. |
| **Superpowers** | MIT na raiz de `obra/superpowers`, mas contém muitas skills e fluxos próprios. | Selecionar apenas skills com ganho comprovado após revisão de compatibilidade e custos; não importar em massa. |

## Política de seleção e distribuição (decisão do criador em 11/11/2026)

- **Qualidade técnica primeiro:** não rejeitar uma skill/script na pesquisa, comparação ou avaliação apenas pela falta de `LICENSE` ou de declaração explícita de uso livre. Ausência de licença não é proibição; priorizar testes reais de qualidade, custo de tokens/contexto, integração, segurança, manutenção e dependências.
- **Não confundir pesquisa com cópia:** a falta de proibição também não é autorização automática de redistribuição. Procurar permissões aplicáveis em licença, documentação, termos ou autorização do titular. Respeitar proibições expressas. Quando a redistribuição não estiver autorizada ou confirmada, manter a candidata no registro e avaliar permissão, integração sem copiar arquivos ou implementação original equivalente. Não rebaixar sua avaliação técnica exclusivamente por documentação de licença incompleta.
- **Registrar separadamente:** `QUALIDADE/TESTES`, `PERMISSÃO PARA REDISTRIBUIÇÃO` e `ESTADO DE INTEGRAÇÃO`, evitando chamar de inferior uma candidata apenas por restrição documental.

1. **As skills externas selecionadas e autorizadas para redistribuição devem estar de fato no pacote**, não apenas como URLs — conforme decisão do criador. Cada uma deve incluir referências, scripts e avisos de licença/autoria necessários.
2. A skill nunca deve acionar comandos ou serviços de terceiros sem ferramentas e autorizações reais. Tratar comandos mostrados em SKILL.md como instruções de execução condicionais, não execução automática.
3. Antes da release, gerar pacote completo e **validar que todos os arquivos declarados existem, estão íntegros e são descobertos**; o smoke test mínimo B06 não valida todas essas skills.
4. Não incluir fontes proprietárias, filmes, trilhas, memes, assets de terceiros ou binários sem direitos de redistribuição.
5. O Nox.png fornecido pelo criador é tratado separadamente como asset canônico do Diazverso, não como skill externa.

**Pendências:** testes locais/host das bibliotecas, versões/dependências de FFmpeg, Node e Remotion, direitos de recursos adicionais e revisão de segurança dinâmica antes da publicação.
