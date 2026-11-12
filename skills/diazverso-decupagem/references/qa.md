# QA e correções

Escolher o utilitário conforme a evidência disponível. Cada módulo recebe os dados descritos no próprio CLI; não inventar flags de aprovação.

| Necessidade | Utilitário |
| --- | --- |
| Contrato de composição de clips (modo antigo) | ../scripts/validate_composition.py |
| Extração de quadros do MP4 | ../scripts/extract_review_frames.py |
| Estrutura técnica e revisões de código | ../scripts/review_technical.py |
| Quadros, margens e legibilidade | ../scripts/review_visual.py |
| PCM, níveis e sincronismo declarado | ../scripts/review_audio.py |
| Ritmo, gancho, repetição e payoff | ../scripts/review_pacing.py |
| Procedência e direitos | ../scripts/review_rights.py |
| Estado de correção | ../scripts/correction_loop.py |

Os caminhos são relativos a esta referência. A execução real depende de arquivos, Python/FFmpeg e projeto de edição disponíveis. Análise de metadados não prova escuta humana ou inspeção visual.

`correction_loop.py` aceita fontes semânticas technical, visual, audio, pacing, rights e shorts. Fluxo: OPEN → FIX_APPLIED → RERENDERED → REVIEWED → CLOSED. Fechar apenas com alteração verificável, novo render com hash diferente e revisão do mesmo achado nesse render. A autenticação das evidências é responsabilidade do executor.

Após corrigir, conferir identidade, narrativa, direitos, captions, áudio e arquivo final. Encaminhar a decisão de entrega para `../../diazverso-criacao-video/scripts/approval_gate.py`.
