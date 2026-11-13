# Acesso à internet: ler e baixar

Consultar ao pesquisar fora da busca comum (YouTube, X, Reddit, Instagram, TikTok, GitHub). Ler e baixar são caminhos diferentes.

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

## Baixar

Vídeo, imagem e trilha para o projeto: [baixar mídia](../../diazverso-contentlab/references/baixar-midia.md).
