---
name: diazverso-nox
description: "Use para pôr o Nox no vídeo ou na thumbnail, escolher poses do catálogo e criar ou revisar uma pose nova sem mudar a identidade do personagem."
---

# Nox

**Fonte única:** `assets/brand/nox/Nox.png` (PNG 1408×768, integridade no `assets/manifest.json`). Nunca editar, substituir nem redesenhar. Pose nova não é automática.

## Na edição

O Content Lab não traz o Nox: em cada projeto, o pacote `assets/brand/nox/` (poses e `assets/brand/nox/poses/catalogo.json`) entra como personagem por `character_import`, com os direitos confirmados (`../diazverso-contentlab/SKILL.md`). Depois, o Nox entra pelo kit (`../diazverso-motion/SKILL.md`) em opinião e humor, quase sempre em aparte: a cena desfoca e ele sobe inteiro pela borda de baixo. Ele gesticula em **stop motion**: enquanto fala, troca o desenho inteiro de uma vez a cada 0,7–1 s, e todas as poses do catálogo aparecem ao longo do vídeo.

Cada pose é um PNG pronto (gesto e olhos desenhados) em `assets/brand/nox/poses/`. Variantes `-b` são sorteadas. O [catálogo e as regras de uso](references/poses.md) listam as 21 poses com gesto, olhos e tons. A expressão vem do desenho da pose: o kit não desenha olhos, só escolhe a pose pelo tom.

## Pose nova

1. Gerar pela ferramenta de imagem com o `Nox.png` como referência, com o pedido de [poses](references/poses.md). A ferramenta precisa permitir uso comercial.
2. **Character Lock:** comparar lado a lado com o `Nox.png` e reprovar se silhueta, proporções, paleta, roupa ou estilo mudarem, ou se aparecer boca ou nariz.
3. Salvar com nome novo, registrar no `assets/manifest.json` e no `catalogo.json`, e rodar o validador. `scripts/character_lock.py <avaliacao.json> --root <plugin>` confere a identidade do arquivo e a avaliação registrada; ele não reconhece o personagem por visão.

O Nox entra quando ajuda a narrativa ou a thumbnail; não precisa estar em toda cena. O criador publica manualmente.
