# Acesso à internet: ler e baixar

Consultar ao pesquisar fora da busca comum (YouTube, X, Reddit, Instagram, TikTok, GitHub) e ao buscar mídia das obras. Ler e baixar são caminhos diferentes.

## Ler (pesquisa)

1. **Ferramentas próprias primeiro:** busca e leitura web, com `site:dominio` quando ajudar. Se o corpo, os comentários ou as legendas encontrados bastarem, responder sem instalar nem logar nada.
2. **Agent Reach** ([Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach), MIT) só preenche lacunas: quando a busca falha ou traz apenas o trecho, ou para legendas e transcrições do YouTube, posts e threads do X, Reddit e perfis do Instagram.
   - Conferir com `agent-reach doctor --text`.
   - Se não estiver instalado, dizer ao criador que existe e como instalar (`npx skills add Panniantong/Agent-Reach@agent-reach`). Instalar só a pedido dele.
   - Uso: `agent-reach read <url>`, `agent-reach <canal> search "<termo>" --limit 5`, `agent-reach youtube subtitle <url>`. A resposta vem em JSON: `ok`, `items[].text`, `error.code`.
   - Em `NEED_LOGIN`, `RATE_LIMITED`, `PLATFORM_BLOCKED` ou `BUSY`: parar a tentativa, manter o que já foi obtido e avisar. Não trocar de conta, de backend ou de navegador, nem tentar em loop.
   - O login é sempre do criador (`agent-reach login <canal>`). Nunca pedir nem exibir senhas ou cookies.
3. **Dizer o que se tem.** Trecho de busca, casca de página, contagem de comentários e lista de faixas de legenda não são corpo, comentários nem legenda. Sem a fonte lida, a alegação fica "a verificar".
4. TikTok não tem canal de leitura. Nesse caso, ler pela web ou pedir o link ao criador.

## Baixar (mídia do vídeo)

- **Vídeo** do YouTube, TikTok, Instagram, X e outros sites suportados pelo yt-dlp: `media_import_url` do Content Lab, com o link exato e os direitos confirmados pelo criador. Preferir o canal oficial (estúdio, editora). Não usar vídeo de outro criador de conteúdo.
- **Imagens** (capas, painéis, pôsteres): fontes com proveniência, como as wikis da obra, a Wikipedia e os sites oficiais.
  - Quando o servidor recusa download automático, baixar pelo navegador do app ou pelo navegador do criador, que carregam a página como um usuário comum.
  - Nunca disfarçar o cliente (user-agent ou referer falsos), resolver captcha ou contornar bloqueio de robô.
- Nomear cada arquivo pelo que mostra (`hq-king-in-black-01-capa.jpg`, `filme-venom3-trailer-final.mp4`) antes de `media_import_files`.
- Abrir as imagens antes de importar: a capa certa, sem variante errada nem marca d'água.
