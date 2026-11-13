# Usar o plugin Diazverso

Comece por `skills/diazverso/SKILL.md`: ela reúne as regras do canal, a ordem de produção e a tabela que indica qual skill abrir. Use uma skill principal por etapa e apenas as referências necessárias à próxima ação.

Produza no Content Lab com `skills/diazverso-contentlab/SKILL.md`. O plugin define o estilo do canal e fornece o Nox; o Content Lab executa e guarda o projeto. Abra o projeto para o criador acompanhar e respeite o modo de aprovação combinado.

O roteiro segue a organização audiovisual do VD_0008: capítulos temáticos e blocos alternados de narração, cena/som original e direção visual. Só `narration.text` é lido pela pessoa ou pela voz clonada. Na gravação, mostrar apenas a fala, por capítulo; títulos não são narrados.

Depois de montar a narração, aguarde a transcrição automática com Whisper `large-v3` completo. Leia `narration_transcript` antes de editar: a imagem da obra, o corte e a legenda devem acompanhar o tempo real da fala. Falha ou dependência ausente exige retomar com `narration_transcribe`, sem certificar a etapa como pronta.

As mídias das obras são a base visual e precisam corresponder ao que é dito. O motion compõe com elas; não substitua evidências por telas genéricas de texto. Importe o pacote do Nox e preserve o desenho canônico, licenças e autorizações.

Confira prévias, áudio, render e leituras de retorno de Drive/Sheets. Não declare resultados sem artefatos reais. Entregue o kit revisado; o criador publica manualmente. Não instalar o plugin automaticamente.
