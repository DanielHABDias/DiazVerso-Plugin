# Baixar mídia para o projeto

Consultar na etapa Mídia, antes de importar vídeo ou imagem. A pesquisa e a leitura de fontes ficam em [acesso à internet](../../diazverso-pesquisa/references/acesso-web.md).

## Vídeo: pelo Content Lab

O Content Lab baixa com o yt-dlp: um vídeo por link, sem playlist, até 4 GB, mesclado em MP4. Funciona com YouTube, TikTok, Instagram, X, Vimeo e os outros sites que o yt-dlp suporta.

- **Agente:** `media_import_url` com o link exato, `rights` e `rightsConfirmedByUser: true`, depois `job_wait`.
- **Criador:** a aba **Importar por URL**, na etapa Mídia do app. É o caminho quando o link exige a conta dele.
- **Cobertura:** buscar vídeo para cada personagem, objeto ou evento que a fala cita, não só para o tema central.
  - Quando a cena exata não existe em vídeo (só na HQ), usar uma cena que **represente** o personagem: o filme, a série animada (o Venom do desenho de 1994), o trailer de um jogo (*Spider-Man 2* do PS5).
  - Exemplos: o Gorr com a Necroespada em *Thor: Amor e Trovão* representa a All-Black; o Celestial de *Eternos* representa os Celestiais.
  - Uma busca por personagem (`<obra> official trailer <personagem>`), com `allowed_domains: ["youtube.com"]`.
- **Escolher antes de baixar:**
  - o link direto do vídeo (`watch?v=`, `/video/`, `/status/`), nunca o de playlist ou perfil;
  - **conferir o canal antes de importar**, sem baixar nada: `curl -s "https://www.youtube.com/oembed?format=json&url=<link>"` devolve `author_name`. Preferir Marvel Entertainment, Sony Pictures Entertainment, PlayStation e Marvel Studios. Canais de notícia ou de reupload (Nerdist, IGN, "Movie Trailers") ficam como segunda opção, e só sem logo grande;
  - nada de vídeo com outro criador aparecendo ou narrando, react, "breakdown", "concept trailer" ou fan-made;
  - séries antigas sem upload oficial: um clipe do episódio pode entrar. Uma marca pequena do canal de TV que exibia a série é aceitável; logo de outro criador do YouTube, não.
- **Direitos:** o criador confirma uma vez por produção (o canal usa fair use de comentário). Sem essa confirmação, não importar.
- **Não precisa cortar.** O plano de motion usa o trecho exato do clipe (entrada e saída), e o áudio do clipe fica mudo, salvo trecho de cena previsto no roteiro.
- **Conferir depois de importar:** o caminho do arquivo está em `project.json` (`uri` do `mediaId`). Tirar um frame no meio de cada vídeo com o ffmpeg e olhar: o assunto certo, sem marca d'água e sem ninguém por cima. Anotar a resolução.
- **Zoom em vez de descartar:** vídeo em 4:3 ou com marca pequena num canto entra com zoom de 110–120% (preenche o 16:9 e corta a marca). Anotar o zoom na direção do roteiro e no manifesto. Se ainda assim não servir, trocar pelo recorte PNG do personagem ou pela imagem inteira.
- **Nomes:** o arquivo importado leva o nome do link. Registrar o vídeo no manifesto de mídia, que fica em `manifesto-midia.md`, na pasta do projeto:
  - o `mediaId`;
  - o nome descritivo (`filme-venom3-trailer-final`, `desenho-1994-venom-contra-aranha`, `jogo-spiderman2-ps5-revelacao`);
  - a URL e o canal;
  - o trecho que interessa.

  Usar esse nome no plano e nas falas com o criador.
- **Ligar ao roteiro:** depois de importar, acrescentar ao roteiro um bloco `direction` "Vídeos de…" por capítulo, com `script_edit` (`block.add` antes da fala seguinte), dizendo qual clipe entra em qual palavra (1–3 s, sem áudio). A narração aprovada não muda. Se a revisão der conflito, a `baseRevision` é a do projeto: ler o valor `actual` no erro e repetir.
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

## Recortes PNG dos personagens

O plano de motion põe por cima da cena todo arquivo cujo nome tem `recorte` ou `png` e uma palavra que a fala diz (`recorte-knull.png` aparece quando a narração fala "Knull"). Fazer um recorte para cada personagem citado. O nome deve usar a palavra falada em português (`recorte-carnificina`, `recorte-sentinela`).

1. **Fonte:** arte em alta resolução com o personagem inteiro e fundo simples (capa sem texto, painel da wiki). As artes de jogos nas wikis costumam ter 256 px, pequenas demais.
2. **Recortar localmente** com o rembg num venv isolado (`pip install "rembg[cpu,cli]"`; o modelo de cerca de 180 MB baixa no primeiro uso):
   ```bash
   rembg i -m isnet-general-use entrada.jpg recorte-nome.png
   ```
   Se o resultado ficar ruim (cabelo, mãos ou armas faltando), usar `-m birefnet-general` (cerca de 1 GB, mais preciso; é o padrão para o personagem da thumbnail) ou outra fonte.
3. **Limpar:** zerar o alfa abaixo de cerca de 60 (some o fantasma do fundo) e cortar no contorno do personagem (PIL: `getbbox` do canal alfa).
4. **Conferir** todos sobre um fundo de cor sólida numa faixa de miniaturas. Descartar recorte com fundo sobrando, pedaços faltando ou personagem pequeno demais. Uma capa que junta dois elementos da tese pode virar recorte de bônus (`recorte-hela-knull-gaiola`).

## Áudio

- **Trilha:** biblioteca de áudio do YouTube ou outra licença clara, como CC BY (com o crédito no kit de publicação), importada com `role: "music"`.
- **SFX:** `audio_library` ou o Openverse com licença comercial ([som](../../diazverso-motion/references/som.md)).
