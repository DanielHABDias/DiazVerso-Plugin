---
name: diazverso-nox
description: "Use quando precisar inserir o mascote Nox no roteiro, thumbnail, composição ou criar/revisar nova pose sem alterar a identidade do personagem original."
---

**Protocolo obrigatório Diazverso:** antes de agir, aplicar `../diazverso-contexto-eficiente/SKILL.md`. Ler uma vez por sessão/versão e reutilizar o contexto válido; abrir somente a skill principal e as dependências necessárias.

# Diazverso — Nox e Character Lock (character-lock)

**Fonte única:** `assets/brand/nox/Nox.png` (imagem original fornecida pelo criador). A versão canônica consta no `assets/manifest.json`; não inferir que outro arquivo nomeado Nox é equivalente. A referência canônica não deve ser editada ou substituída. A criação de poses **não é automática**.

## Procedimento

1. Localizar a imagem física no pacote e comparar **bytes, dimensões e digest do blob Git** com `assets/manifest.json`, usando `scripts/character_lock.py`. O manifesto atual declara PNG de **1408×768** e **415.179 bytes** com `git_blob_sha1`. Se a imagem não estiver disponível para leitura real, **bloquear** a criação/revisão; não inventar o rosto ou a roupa.
2. Observar o Nox original diretamente: preservar silhueta, proporções, cores, traços faciais/olhos, roupa/acessórios existentes e linguagem visual do personagem. **Não descrever detalhes concretos que não tenham sido inspecionados.**
3. Para uma nova pose, elaborar uma ação pequena e contextual para o roteiro (ex.: apontar, reagir, olhar), sem redesign de proporções, roupa, paleta ou estilo. Passar o PNG original como referência à ferramenta de imagem autorizada, quando realmente possível.
4. Salvar o candidato com **novo nome e versão**, nunca sobrescrevendo `Nox.png`. Separar arte original e derivados. Registrar origem, prompt/instrução, relação com a cena e evidência de direitos.
5. **Character Lock:** comparar visualmente candidata e canônica lado a lado; documentar seis aspectos: silhueta/proporções, traços faciais, paleta, roupa/acessórios, estilo e ausência de redesign. Se algum divergir, reprovar e corrigir uma mudança por vez.
6. Com prova de leitura do arquivo original, imagem derivada efetivamente existente e notas de inspeção humana, executar `python skills/diazverso-nox/scripts/character_lock.py <avaliacao.json> --root <raiz-do-plugin>`. O script mede identidade de arquivo e integridade documental; **não reconhece personagens por visão computacional**, não autentica que a comparação humana aconteceu e não declara geração de imagem sem arquivo.
7. Empregar Nox somente quando contribuir para a narrativa ou a thumbnail. **Não obrigar o mascote a aparecer em toda cena.**


Sem upload, postagem ou automação de publicação. O criador publica os vídeos manualmente.

Para elaborar uma variação, consultar [orientação de pose](references/pose.md) somente quando necessário.

## Na edição

O Nox entra pelo kit (`../diazverso-motion/SKILL.md`) em opinião e humor, quase sempre em aparte: a cena desfoca e ele aparece inteiro subindo pela borda de baixo, com as pernas fora do quadro.

Ele **gesticula em stop motion**: cada fala troca o desenho inteiro para outra pose, de uma vez, sem animação entre as poses. Exemplos:

- mão na frente do rosto, pensando;
- arminha;
- apontando;
- dando de ombros;
- facepalm.

As poses se combinam: cada pose é um PNG do corpo com o gesto e o rosto vazio, e o kit desenha por cima os olhos de qualquer um dos 8 humores, nas posições gravadas no `poses.json` da pasta de poses. Uma pose pode ter variantes desenhadas, sorteadas a cada fala. A lista, o formato, o `poses.json` e o pedido para a ferramenta de imagem estão em [poses](references/poses.md). Sem a pose, o kit usa o Nox canônico com o humor (`assets/brand/nox/nox-sem-olhos.png`).
