# Estrutura Google

Raiz Diazverso, planilha nativa Canal do YT — V1.0 (Diazverso), Roteiros/Longos e Roteiros/Shorts, Thumbnails/Longos e Thumbnails/Shorts. Docs e imagens ficam diretamente nessas pastas, com ID no nome; não criar pasta por vídeo por padrão.

Bibliotecas opcionais: Assets, Backgrounds, Memes, Músicas e Sounds. Localizar por identidade, MIME e pai; ter um arquivo na biblioteca não comprova direitos.

## Planilha

Abas Produções, Ideias, Afiliados e Config (oculta). Cabeçalhos exatos são definidos em `../scripts/validate_sheet_schema.py`; validar a linha 1 antes de editar. Preservar abas desconhecidas e conteúdo fora da alteração autorizada.

- Ideias usa TF_####; produção longa VD_####; Short SH_####. Não reutilizar IDs emitidos.
- A ideia só sai de Ideias depois de conferir a produção, a origem, o vínculo e o Doc. Remoção exige autorização pertinente.
- Produções guarda tipo, tema, status, prioridade, títulos A/B, thumbnails A/B, roteiro, vínculos, planejamento, data/URL reais de publicação, revisão, observações e kit.
- A planilha não guarda o roteiro inteiro: usar Doc nativo formatado e link na coluna ROTEIRO.
- Dados operacionais, inclusive data de publicação e revisão da fonte, permanecem necessários; não equivalem a cronologia do plugin.

## Escritas

Usar operações nativas por campo com máscara restrita, valores literais e validações preservadas. Não copiar valores, fórmulas ou chips específicos de outra produção. Antes de alterar, reler identidade, tipo e valores esperados; depois conferir retorno.

`sheets_batch.py` reserva linha, contador e operation_id no mesmo batch. Exige escritor único coordenado pelo host e histórico completo para inicializar contadores. Não cria lock distribuído. Em resposta perdida, reler e recalcular; não reenviar batch em cache.

Conferir CURRENT_SPREADSHEET_ID e IDs de pastas da própria instalação. Uma cópia de planilha pode conter vínculos de outra instalação; reparar os vínculos da cópia antes de utilizá-los. Config é configuração, não fonte de credenciais.

## Docs e mídia

Roteiro nativo: título, briefing, títulos/thumbnails, blocos de narração e audiovisual distinguíveis, fontes, revisões e kit não narrado. Usar named styles e índices UTF-16, e conferir conteúdo/estilos/pai após escrita.

Thumbnails exigem arquivo de imagem identificável e link direto, com conferência de identidade e pasta. Assets e Nox precisam de direitos e integridade. Itens em triagem não são aprovados automaticamente.

PUBLICADO exige postagem manual realmente confirmada, data e URL verificáveis. O plugin não envia, agenda ou ensina a postar.
