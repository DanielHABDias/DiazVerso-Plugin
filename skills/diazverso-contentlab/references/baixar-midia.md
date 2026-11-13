# Baixar mídia para o projeto

Consultar na etapa Mídia, antes de importar vídeo ou imagem. A pesquisa e a leitura de fontes ficam em [acesso à internet](../../diazverso-pesquisa/references/acesso-web.md).

## Vídeo: pelo Content Lab

O Content Lab baixa com o yt-dlp: um vídeo por link, sem playlist, até 4 GB, mesclado em MP4. Funciona com YouTube, TikTok, Instagram, X, Vimeo e os outros sites que o yt-dlp suporta.

- **Agente:** `media_import_url` com o link exato, `rights` e `rightsConfirmedByUser: true`, depois `job_wait`.
- **Criador:** a aba **Importar por URL**, na etapa Mídia do app. É o caminho quando o link exige a conta dele.
- **Escolher antes de baixar:**
  - o link direto do vídeo (`watch?v=`, `/video/`, `/status/`), nunca o de playlist ou perfil;
  - o canal oficial (estúdio, distribuidora, editora), pelo título e pelo canal que aparecem na busca;
  - nada de vídeo de outro criador de conteúdo, reupload, "concept trailer" ou fan-made.
- **Direitos:** o criador confirma uma vez por produção (o canal usa fair use de comentário). Sem essa confirmação, não importar.
- **Não precisa cortar.** O plano de motion usa o trecho exato do clipe (entrada e saída), e o áudio do clipe fica mudo, salvo trecho de cena previsto no roteiro.
- **Nomes:** o arquivo importado leva o nome do link. Registrar no manifesto de mídia o `mediaId`, o nome descritivo (`filme-venom3-trailer-final`), a URL, o canal e o trecho que interessa. Usar esse nome no plano e nas falas com o criador.
- **Falhas:**
  - `DEPENDENCY_MISSING`: o yt-dlp falta em Dependências; o criador instala no app.
  - Link privado, com restrição de idade ou de região: pedir ao criador para importar pela aba com a conta dele.
  - Playlist recusada: pegar o link de um vídeo só.
  - Não tentar o mesmo link em loop.

## Imagem: capas, painéis e pôsteres

1. **Fonte com proveniência:** wikis da obra (pela API `prop=pageimages|imageinfo`), Wikipedia ou o site oficial. Conferir edição, número e se é a capa principal ou uma variante.
2. **Download direto** quando o servidor permite, identificando o cliente com honestidade.
3. **Se o servidor recusa download automático:** baixar pelo navegador do app ou do criador, que carregam a página como um usuário comum.
   - Para gravar em disco, abrir uma página local de recebimento no navegador do app (`preview_start` com a URL local). Dela, buscar a imagem e enviá-la por POST para essa mesma origem.
   - Nunca disfarçar o cliente (user-agent ou referer falsos), resolver captcha ou contornar bloqueio de robô.
4. **Nomes descritivos:** `hq-<obra>-<número>-<o que mostra>.jpg`, `filme-<obra>-<o que mostra>.jpg`. Converter WebP para JPG quando preciso.
5. **Abrir as imagens** (uma faixa de miniaturas basta) antes de `media_import_files`. Descartar variante errada, marca d'água ou imagem que não mostra o que a fala cita.

## Áudio

- **Trilha:** biblioteca de áudio do YouTube ou outra licença clara, como CC BY (com o crédito no kit de publicação), importada com `role: "music"`.
- **SFX:** `audio_library` ou o Openverse com licença comercial ([som](../../diazverso-motion/references/som.md)).
