# Thumbnail: quadrinhos, palavra e recorte emocional

## Escolha da arte

Priorizar artes de **quadrinhos e desenhos**, com expressão ou postura que transmita a emoção da promessa: tensão, tristeza, raiva, espanto, culpa ou determinação. Não usar PNG, foto, ator, frame ou pôster de filme/live-action por iniciativa própria. Usar arte de filme somente quando o criador pedir explicitamente. Essa regra é da thumbnail; as cenas dos vídeos continuam seguindo as necessidades do roteiro.

Verificar se é o personagem correto e se a imagem comunica a emoção de verdade; não chamar uma expressão neutra de choro. Preferir originais com pelo menos 1800 px de altura quando o rosto ocupar grande parte da tela. Conferir resolução nativa: exportar em Full HD não cria detalhes que faltam na fonte. Buscar outra fonte quando o recorte depender de ampliar demais uma miniatura.

Separar o personagem em PNG com **alpha real**, sem pedaços de cenário, balões, títulos ou masthead da revista. Preservar cabeça, cabelo, touca, orelhas e mãos relevantes; não usar polígonos grosseiros atravessando a arte. Conferir sobre fundo contrastante. Quando autorizado pelo host e criador, ferramentas de recorte como BiRefNet/rembg podem ajudar; não instalar modelos por suposição. Se uma recriação for necessária e solicitada, usar ferramenta de imagem autorizada e registrar como arte editorial, sem apresentá-la como painel canônico. Fan art não implica licença do titular nem elimina direitos autorais.

Importar cada PNG no Content Lab assim que ficar pronto, registrar fonte e situação de direitos, abrir e conferir a mídia importada. O plugin fornece o Nox canônico; nunca redesenhá-lo.

## Camadas, de trás para a frente

1. **Fundo `quadrinhos` do Content Lab**: colagem de revistinhas do catálogo, discreta e escurecida. Não é preciso copiar um fundo para cada projeto ou gerar outra colagem.
2. **Meio-tom**: pontilhado preto cobrindo o fundo, combinado com vinheta escura; atrás do recorte e dos textos.
3. **Palavra principal** sólida, grande e brilhante em Anton, atrás do recorte.
4. **Personagem da obra**, grande e com halo preto. O rosto e a emoção precisam se ler no celular. Preservar a identidade e os elementos aprovados.
5. **Contorno fino da palavra principal**, alinhado com o preenchimento, na mesma cor e com brilho, na frente do recorte. Conferir que parte suficiente da palavra sólida continua visível.
6. **Palavra complementar opcional**, sólida em Anton, somente na frente. Sem borda pesada ou deformação arbitrária. Até quatro palavras somando os dois textos; complementar o título.
7. **Moldura colorida**: fina, com quinas internas arredondadas e exterior ocupando o retângulo da thumbnail.
8. **Nox por cima de tudo**, inclusive da moldura: cabeça muito grande no canto inferior, olhos e gesto legíveis, corpo cortado pela borda. Depois da aprovação, preservar pose, posição e escala.

As cores das palavras podem variar conforme o conceito. A moldura usa a paleta azul/amarelo/vermelho do canal. Não inserir assinatura, nome do canal ou selo na moldura por padrão. Fundo claro ou outra composição só a pedido do criador ou quando necessário à promessa; conferir o contraste real.

## Receita do Content Lab

Usar **`thumbnails_generate`**, `style: "kit"`, `layout: "palavra"`. O Content Lab fornece o fundo, as camadas, as fontes e o contorno; o plugin define a direção e os parâmetros. Não escrever TSX específico do projeto nem alterar o app para cada thumbnail. Consultar `motion_kit` para o contrato atual. As medidas de estilo usam uma tela de referência 1280×720 e são escaladas pelo app; o longo é exportado em 1920×1080, com prévia de 320 px. No Short, somente A,9:16; adaptar o enquadramento e o texto para o vertical.

Parâmetros do visual do canal:

```json
{
  "layout": "palavra",
  "background": "quadrinhos",
  "texture": "halftone",
  "outline": "cor",
  "backgroundEffects": {"blur": 3, "brightness": 0.7, "saturation": 0.65, "vignette": 0.75},
  "halftone": {"spacing": 9, "radius": 0.3, "opacity": 0.595, "color": "#000000", "full": true},
  "border": {
    "width": 7,
    "radius": 24,
    "colors": ["#2676E8", "#2676E8", "#F5C518", "#E63946"],
    "stops": [0, 20, 52, 88],
    "angle": 115
  }
}
```

A espessura equivale a 10,5 px em Full HD e o raio interno a 36 px. O Nox permanece sobre o contorno automaticamente. Se a moldura cobrir olhos, rosto, mãos ou texto relevante, ajustar só o enquadramento necessário; não mover elementos aprovados sem necessidade.

Completar cada variante com `label`, `mediaId` do PNG transparente, `text`, `tone`, `textY`, `humor`, `pose`, `side`, `focus` e `zoom`. O pacote do Nox precisa estar importado no projeto (`character_import`). Quando necessário:

- `subject: {x,y,width,height}` posiciona e dimensiona somente o recorte; ajustar para dar espaço à palavra e preservar os rostos. As medidas são relativas à tela 1280×720.
- `textStyle: {size,letterSpacing}` ajusta Anton sem trocar a fonte.
- `foregroundText: {text,x,y,width,size,letterSpacing,stretch,tone}` cria a palavra complementar frontal. Referência de escala para um longo: `{"text":"AMIGO","x":330,"y":500,"width":560,"size":165,"letterSpacing":1.65,"stretch":1.15,"tone":"verde"}`. Ajustar à imagem e à leitura; não impor essa posição a todos os vídeos.
- `backgroundMediaId` só quando o criador escolher outro fundo; o catálogo `quadrinhos` dispensa importar um arquivo.

O app salva a receita em `creative.packaging.thumbnailVariants`. Sem `variants`, `thumbnails_generate` reutiliza os parâmetros salvos. Para revisar somente B, enviar só B: o app preserva A e os demais metadados. Na interface, os mesmos controles ficam em **Título e thumbnail → Ajustar composição da thumbnail**. Não editar `project.json` diretamente.

## Conferência e entrega

Abrir a imagem inteira e a prévia de 320 px. Conferir o personagem e a emoção, qualidade do recorte e alpha, rosto e touca íntegros, palavra legível com preenchimento suficiente, meio-tom atrás do assunto, vinheta discreta, moldura sem cobrir o foco e Nox acima dela. Conferir cores e espessura no arquivo real; ajustar e gerar novamente se necessário.

Ler de volta a receita e os vínculos A/B gravados. Atualizar o kit com `deliverable_build`; não declarar aprovação humana sem o ok do criador. Publicação é manual.
