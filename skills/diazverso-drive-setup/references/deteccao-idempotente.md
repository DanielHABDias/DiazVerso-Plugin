# discovery — Descoberta idempotente de Drive (somente leitura)

**Executor portátil:** `../scripts/discover_structure.py` consome JSON de metadados já lidos por um conector Drive autorizado. Ele **não conecta**, **não cria** e **não modifica** pastas. Não colocar IDs da conta do criador no código ou nos exemplos distribuídos.

## Procedimento da skill

1. Confirmar que há ferramenta de leitura Drive conectada e saber em qual conta/Drive está trabalhando. Se já existe um `root_id` de configuração, verificar nome **exato** `Diazverso`, MIME de pasta, pais e acesso; não usar configuração de outra conta.
2. Pesquisar pastas de nome exato `Diazverso` (não variantes como `diazverso-plugin`) e coletar **todas as páginas**. Resultado incompleto ou ambíguo = bloqueio, não criação. Se houver mais de uma raiz exata, selecionar apenas com ID da instalação já verificado ou decisão do usuário.
3. Listar diretamente os filhos da raiz com filtro de parent exato e `trashed=false`; paginar até o fim. Repetir nos filhos `Roteiros` e `Thumbnails`. Conferir nome, MIME e **pai real** de cada objeto; não aceitar `Longos` de outra pasta.
4. Exigir `Roteiros/{Longos,Shorts}`, `Thumbnails/{Longos,Shorts}` e a planilha nativa `Canal do YT — V1.0 (Diazverso)`. Descobrir também `Assets`, `Backgrounds`, `Memes`, `Músicas` e `Sounds` como bibliotecas **opcionais**: ausência de uma opcional não exige reparo para operação básica.
5. Alimentar o script com o snapshot em memória ou JSON local. As chaves aceitas são `root_pages`, `children` (por ID pai), `complete` (por ID e `roots`), e opcionalmente `preferred_root_id` e `preferred_ids` da instalação. Cada página segue o formato `results` (conector) ou `files` (Drive API), contendo `id`, `title/name`, `mime_type/mimeType` e `parent_ids/parents`. `complete` só deve ser true depois de **esgotar** `next_page_token`/`nextPageToken`.
6. Interpretar `COMPLETE`, `INCOMPLETE`, `ROOT_MISSING` ou `BLOCKED`. `MISSING` não autoriza criar; `AMBIGUOUS` ou `CONFIG_ID_INVALID` impede seleção automática. Registrar IDs encontrados **somente** na configuração autorizada daquela instalação, nunca no pacote público.
7. **Repetir a leitura** se o usuário solicitar configurar/reparar ou se houver alteração concorrente. Criação/reparo autorizado exige nova inspeção e confirmação; a descoberta não escreve dados.

## Cuidados

- Consultas `'<ID_PAI>' in parents and trashed = false` devem usar o ID **descoberto na conta atual**, não ID deste projeto; ferramentas que não suportam filtro deverão retornar pais verificáveis.
- Nem `search` textual genérico nem título aproximado identificam uma pasta de forma unívoca. Resultado paginado parcial não equivale a pasta ausente.
- Não criar, renomear, mover, excluir ou compartilhar arquivos durante detecção; não pressupor Drive conectado no plugin.

## Contrato de resultado

`writes_performed=false` sempre. Cada caminho contém `EXISTS` + ID da instalação, `MISSING`, `AMBIGUOUS` ou `CONFIG_ID_INVALID`. Se faltarem bibliotecas opcionais, reportar `INCOMPLETE` com lista explícita, mas só os caminhos essenciais devem bloquear a operação básica. A validação de abas/colunas fica para sheet-schema.
