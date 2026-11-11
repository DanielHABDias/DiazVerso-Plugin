# D07 — teste real de mídia Nox em editor offline (11/11/2026)

**Teste executado de verdade em ambiente de desenvolvimento local**, sem Google Drive, APIs, upload nem renderizador Remotion. A ferramenta foi o Pillow (editor/compositor de imagens), com o arquivo ORIGINAL `Nox.png` já presente localmente. Nenhuma imagem gerada por busca ou semelhante à identidade foi usada.

## Entrada verificada

- Nox canônico: `assets/brand/nox/Nox.png` no plugin; para esta execução, cópia do próprio original em `/mnt/data/Nox.png`.
- Bytes do arquivo original: **415.179**. Dimensões: **1408×768**, RGBA.
- SHA-256: `6c00a247735261a3fedb1c7059ace8ff486c18b8e18b2e71b6cce1bcccae31c3`.
- Git blob SHA-1: `776d1b26983e6f9095178881c83b44f114a40336`, igual ao manifesto do repositório.
- Ao decodificar a imagem inteira, a área alfa não vazia foi `[508, 53, 920, 722]`. Isso mostra que os pixels do personagem realmente estavam disponíveis, não apenas o cabeçalho PNG.

## Execução do teste

Em um compositor Pillow local, o Nox original foi recortado **somente na imagem derivada** pela caixa alfa, redimensionado preservando proporções e desenhado sobre um fundo sólido produzido no próprio código. O original permaneceu inalterado.

| Saída REAL do editor offline | Resolução | SHA-256 da imagem gerada |
| --- | --- | --- |
| `nox-offline-16x9.png` | 1920×1080 | `f8e8a7b3b4a6829d957774fa2e1d645d08d855b48eda2c1e743f00673e4ff770` |
| `nox-offline-9x16.png` | 1080×1920 | `26689594fda8e041619cebddc1cf45ce22815bd9403105251930fc9d` |

Ambas foram **reabertas e decodificadas**, com dimensões conferidas e pixels do personagem visíveis no centro. O status do teste executado foi `OFFLINE_IMAGE_EDITOR_PASS`. Não houve consulta à conta conectada.

O teste foi incorporado em `scripts/verify_offline_nox_editor.py` (Pillow é dependência **somente do ambiente de teste**, não do plugin) e a suíte GitHub Actions agora tenta executá-lo sobre o **arquivo canônico do checkout**, preservando os quadros como artefatos privados. Esse novo CI ainda não teve resultado confirmado neste registro.

## Limites

- **D07 comprova mídia efetivamente carregada e composta em um editor de imagens offline** e complementa o auditor de ZIP já implementado; não comprova render Remotion nem uso de outros assets que não constam no manifesto.
- Uma tentativa de abrir a mesma imagem em Chromium headless local **travou e não produziu evidência utilizável**; não declarar esse teste aprovado.
- O ZIP final completo continua sujeito a L06 e o funcionamento do runtime Remotion a **G05/H09**. Não houve instalação do plugin e nenhum vídeo foi publicado.
