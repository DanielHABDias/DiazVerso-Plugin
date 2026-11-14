# Modelo "palavra": personagem atravessando o texto

Consultar antes de compor ou revisar qualquer thumbnail. As referências visuais do canal em `../examples/` mostram a palavra brilhante atravessada pelo personagem e a reação grande do Nox.

## Camadas, de trás para a frente

1. **Fundo simples e escuro.** Quase preto, com leve tom da cor da palavra, chiado de TV discreto e vinheta. O fundo não disputa atenção. Arte de fundo só quando tiver função editorial; não importar automaticamente bandeiras, cenários ou detalhes da imagem de origem.
2. **Palavra principal sólida e brilhante.** Anton gigante, com brilho forte na cor escolhida. Ela ocupa boa parte da largura e atravessa a região do personagem. A/B podem ter cores diferentes.
3. **Personagem da obra em PNG transparente.** Grande, reconhecível e imponente, com sombra ou halo preto suave acompanhando sua silhueta. Esse contorno escuro separa corpo e letras nos cruzamentos. A arte cobre o preenchimento brilhante, sem levar junto o fundo original.
4. **Contorno frontal da palavra principal.** Duplicar exatamente a posição, escala e quebra do texto de trás, deixando só um contorno branco fino e o interior transparente. Ele passa por cima do personagem. Manter preenchimento e contorno como camadas independentes.
5. **Palavra complementar opcional.** Pode ficar em outro ponto livre, grande, sólida e brilhante, inteiramente na frente do personagem, sem duplicata vazada nem contorno frontal. Exemplo de composição: PASSADO gigante no alto atravessado pelo personagem; SUJO separado à direita, um pouco acima da base, sólido e brilhante. Não é obrigatório quebrar toda frase desse jeito.
6. **Nox por cima de tudo.** Num canto inferior, muito grande, com foco na cabeça, olhos e gesto. Cortar o corpo pela borda; não mostrar o corpo completo nem exigir corte na cintura. A emoção precisa se ler no celular. Não cobrir o sentido da palavra; ajustar o texto quando necessário. Depois que o criador aprovar posição, escala e pose, preservá-las nos ajustes seguintes, salvo pedido explícito.

## Personagem e recorte

- Escolher arte em alta resolução, com rosto, mãos e elementos importantes íntegros. Preferir original com pelo menos 1800 px de altura; conferir a resolução real e não chamar ampliação de detalhe nativo.
- Enquadrar com mais corpo quando a pose ajudar, sem limitar obrigatoriamente à cintura. Aumentar até ficar imponente e manter o rosto reconhecível no celular; evitar tanto o boneco pequeno quanto o zoom que elimina a pose solicitada.
- Separar o personagem do fundo antes de compor. Um arquivo PNG opaco ainda carrega o cenário: conferir alpha real e abrir sobre um fundo contrastante para detectar sobras, buracos ou partes faltantes.
- Ao derivar o recorte de uma imagem, preservar a posição e escala necessárias para sobreposição. Não usar a imagem inteira sobre a palavra: isso faz a bandeira ou o cenário esconderem o preenchimento.
- Usar uma ferramenta de edição disponível e autorizada. BiRefNet/rembg pode fazer o recorte quando o host e o criador autorizarem esse método. Não baixar modelos ou instalar dependências por suposição; respeitar as ferramentas e restrições da sessão.
- Importar o recorte como `mediaId`. `backgroundMediaId` é opcional e fica ausente no fundo simples; só importar a arte original como fundo quando ela for escolhida editorialmente.
- Mudança de aparência, como metade do rosto monstruoso, só com pedido do criador e ferramenta de imagem adequada. Preservar a identidade e não apresentar uma arte editorial como painel canônico. Falha do gerador não significa edição concluída.

## Texto, cor e tamanho

Até quatro palavras somadas, em Anton; complementar a promessa do título sem inventar fatos. A palavra principal sempre atravessa o personagem com preenchimento atrás e contorno na frente. A palavra complementar pode ser só frontal, sólida e brilhante. Cores podem variar entre palavras e variantes, desde que se leiam no fundo escuro. Halo preto ao redor do personagem, brilho do texto e contorno branco frontal têm funções distintas.

## Execução com o kit do Content Lab

Usar `layout: "palavra"`, `mediaId` do recorte transparente, `texture: "tv"`, `tone`, `pose`, `humor`, `side`, `focus`, `zoom` e `textY`. `backgroundMediaId` é opcional. Definir enquadramento e altura pela imagem real; não fixar um zoom ou corte universal.

`thumbnails_generate` monta a palavra principal, mas o contrato disponível pode não expor sombra ajustável, palavra complementar independente ou todos os controles de camadas. Conferir o contrato real antes de chamar; não inventar parâmetros. Para esses ajustes, reutilizar o componente Thumbnail do kit numa composição específica do projeto, mantendo as camadas independentes e os assets canônicos, em vez de desenhar um kit novo ou editar o aplicativo. Salvar a composição editável, renderizar, importar os PNGs e vinculá-los à embalagem pela API/CLI autorizada, com revisão atual e leitura de retorno. Atualizar as cópias visíveis, as prévias de 320 px e o kit de entrega. Não editar `project.json` diretamente.

Ao revisar somente B, preservar o arquivo, o hash e o vínculo de A. Alterar somente os campos pedidos e manter títulos, descrição, tags e elementos já aprovados.

## Conferência real

Abrir a imagem inteira e a versão de 320 px e verificar:

- fundo discreto, sem cenário indesejado;
- personagem grande, recorte íntegro e transparente, sombra escura visível onde atravessa as letras;
- preenchimento brilhante atrás, contorno fino alinhado na frente do personagem;
- palavra complementar, quando usada, sólida, grande e brilhante na camada frontal;
- Nox grande no canto, cabeça e expressão legíveis, acima das outras camadas;
- posição, escala e pose já aprovadas preservadas e textos compreensíveis;
- arquivos e vínculos finais relidos, sem declarar aprovação humana que não ocorreu.
