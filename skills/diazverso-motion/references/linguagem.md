# Linguagem de edição das referências

Medições feitas nos vídeos de referência com FFmpeg (trocas de imagem detectadas) e frames amostrados. São pontos de partida, não regra fixa por segundo.

| Referência | Intervalo médio entre trocas | Papel no Diazverso |
| --- | --- | --- |
| RunnyIA | 1,3 s | Explicação visual e motion: o padrão de ritmo do canal |
| FALL | 1,7 s | Tempo de reação: preparação → acontecimento → reação |
| Um Nerd | 3,4 s | Imagem da obra sustentada enquanto o argumento se completa |

## Técnicas que o kit implementa

| Técnica (referência) | Cena ou efeito do kit |
| --- | --- |
| Palavras gigantes em cortes secos, com bordas vermelha e azul, e zoom contínuo (RunnyIA) | `titulo`, `Punch` |
| Frases "pensadas" em fonte arredondada sobre fundo de estrelas, como respiro (RunnyIA) | `frase` |
| Avatar âncora cuja expressão está nos olhos (RunnyIA) | Nox com 8 humores em `nox`, `evidencia`, `lista`, `numero` e `cta` |
| Interface recriada como prova: painel, número, seta (RunnyIA) | `numero`, `ficha` |
| Lista como objeto: fichas em perspectiva às quais o vídeo volta (RunnyIA) | `lista` |
| Mangá e HQ com linhas de velocidade atrás (RunnyIA) | Fundo `explosao`, `pagina` com onomatopeia |
| Arte da obra sustentada com aproximação lenta (Um Nerd) | `evidencia` com `movimento` |
| Personagens frente a frente na comparação (Um Nerd) | `comparacao` |
| Título condensado sobre a cena escurecida e congelamento na piada (FALL) | `evidencia` com `legenda`, `titulo` |
| Personagem 3D e câmera voando pelo espaço (vídeos feitos com IA e Three.js) | `nox3d` (Nox 3D com gesto) e `paineis3d` (painéis da obra no espaço) |
| Textura constante: grão, linhas de scan, vinheta | Sempre ativa na composição |
| Som em cada troca, pausa da música antes da virada | SFX por beat; ducking sob a voz |

## Aberturas observadas

- **RunnyIA:** "Imagina só…", uma situação dolorosa contada na segunda pessoa, seguida de prova e promessa.
- **FALL:** a premissa absurda, depois a reação e o CTA logo no início.
- **Um Nerd:** um teste direto ao espectador ("quem foi o segundo…?"), que vira a tese.

## Escolher por beat

- **Humor e reação:** corte rápido e Nox.
- **Ensino:** demonstração e progresso, com `formula` e `lista`.
- **Argumento:** a imagem da obra sustentada por 3–5 s com câmera lenta.

Combinar conforme a função. A cena muda quando a informação muda; nunca fica parada por falta de material.
