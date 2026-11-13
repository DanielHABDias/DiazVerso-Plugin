# Narração

## Voz

1. **Preferida:** a voz do criador, gravada ou clonada a partir de amostra com consentimento registrado.
2. **Alternativa aprovada pelo criador:** voz sintética de licença comercial, escolhida uma vez e mantida no canal. Usar a mesma voz em todos os vídeos de uma série.
3. Voz sintética nunca imita uma pessoa real sem consentimento dela.

## Texto de gravação e tempos

No Content Lab, a pessoa lê somente o texto dos blocos `narration`, agrupado por capítulos; títulos de capítulo/bloco, cenas, direção e fontes não são narrados. A voz de IA do app é sempre a voz clonada do criador com consentimento.

Montar a narração também transcreve o áudio final com Whisper `large-v3` completo em português, com início/fim por palavra. Aguardar a conclusão antes da edição e consultar `narration_transcript` para sincronizar os elementos com a fala real. Falha preserva a montagem e permite retomar com `narration_transcribe`; não substituir por estimativas do texto.

## Direção

- Tom de conversa com um amigo que entende do assunto: opinativo, irônico quando o contexto pede, sem locução épica, sem gritar e sem leitura de trailer.
- Ritmo de **150–170 palavras por minuto**; Shorts podem chegar a 180 no gancho. Pausa curta antes do payoff e depois de uma pergunta.
- Frases curtas para falar em voz alta: até cerca de 20 palavras; números e nomes ditos como se fala ("mil novecentos e noventa e seis" pode virar "em noventa e seis" quando natural).
- Revisar pronúncia de nomes estrangeiros (personagens, editoras, criadores) antes de gerar; corrigir com grafia fonética na fala, nunca no roteiro aprovado.

## Mix

- Narração em −16 LUFS integrados (aceitável −14 a −18), pico até −1 dBTP.
- Música 18–24 dB abaixo da voz enquanto há fala (ducking), subindo nas pausas e transições. Consultar `../../diazverso-decupagem/references/musica.md`.
- Escuta completa obrigatória antes da aprovação: medição de LUFS não substitui ouvir.
