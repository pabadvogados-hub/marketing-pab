---
name: apresentacao-premium
description: |
  Skill para criar APRESENTAÇÕES / SLIDES / DECKS premium no padrão "dark + dourado cinematográfico" (padrão Oficina Palladium), renderizar em alta resolução e subir no Google Drive já como APRESENTAÇÃO NATIVA do Google Slides (com botão "Apresentar"), além de PDF e HTML interativo.

  Ative SEMPRE que o usuário pedir: apresentação, slides, deck, palestra, oficina, aula, treinamento, pitch, "monta uma apresentação", "cria slides", "quero um deck", "apresentação de slides", "sobe no Drive como Google Slides", "apresentação pro projetor".

  Produz slides 16:9 idênticos em qualquer projetor (cada slide vira imagem em tela cheia), sem risco de fonte quebrar.
trigger: /apresentacao
---

# 🎬 Apresentação Premium — Padrão Casal da IA / Oficina Palladium

Você monta apresentações com nível de palco: estética **dark + dourado cinematográfica**, tipografia de impacto e conteúdo com arco narrativo de palestra. Entrega final = **Google Slides nativo** no Drive (apresenta direto) + PDF (backup) + HTML interativo.

Kit reutilizável: `MARKETING/_KIT_APRESENTACAO/`
- `template_deck.html` — deck-modelo com TODOS os componentes prontos (copiar e preencher)
- `render.py` — HTML → PNGs 1920×1080 (x2) + PDF
- `subir_google_slides.py` — monta .pptx e sobe convertendo para Google Slides (+ PDF + HTML)

---

## 🎨 SISTEMA DE DESIGN (não alterar sem pedido)

**Formato:** 16:9, 1920×1080. Vinheta + grão + glows radiais dourados. Numeração `01 / NN`. Barra de progresso dourada.

**Cores (CSS vars já no template):**
| Token | Hex | Uso |
|---|---|---|
| `--bg` | `#0b0805` | fundo (warm near-black) |
| `--gold` | `#e4ad57` | dourado principal |
| `--gold-bright` | `#f6cd84` | brilho/degradê |
| `--gold-deep` | `#b8853a` | sombra do degradê |
| `--ink` | `#f6efe3` | texto principal |
| `--ink-soft` | `#cdbfa9` | texto secundário |
| `--ink-mute` | `#9c8b72` | labels/rodapé |

**Fontes (Google Fonts):** `Anton` (hero/display gigante) · `Oswald` (subtítulos e labels condensados) · `Montserrat` (corpo). Destaque sempre a palavra-chave do título com a classe `.grad` (degradê dourado).

---

## 🧩 BIBLIOTECA DE COMPONENTES (classes do template)

Cada slide é `<section class="slide">` com `.topbar` (kicker + pageno), `.body` e `.foot`. Componentes para o `.body`:

| Componente | Classe | Quando usar |
|---|---|---|
| **Capa** | `#s1`: `.cover-tag`, `.eyebrow`, `h1.hero`, `.sub`, `.speakers`, `.when` | abertura |
| **Agenda** | `.agenda > .item (.num/.txt)` | mapa da apresentação |
| **Hook** | `h1.hero` grande + `.lead.lead-xl` | pergunta provocativa |
| **Bullets** | `ul.bullets > li (.mk + b)` | lista de pontos |
| **Antes → Depois** | `.compare (.col.before / .arrow / .col.after)` | virada/contraste |
| **Divisor de seção** | `.divider .three` (palavras gigantes) | separar blocos |
| **Conceito (1 termo)** | `.concept (.glyph + .def h2 + .one + .quote)` | "o que é X" |
| **Grid de cards** | `.grid4 > .c (.n/h3/p)` (3 ou 4 colunas) | pilares/produtos |
| **Detalhe (1 item)** | `.detail (.left num/h2/.tagline + .right .what/.ideal)` | aprofundar 1 item |
| **Áreas + caso real** | `.areas > .a (h4/p)` + `.casebar (.badge/p)` | aplicação no negócio |
| **Escada/passos** | `.ladder > .step (.lvl/.info)` | plano de ação |
| **Demo** | `.demolist > .d (.ic/b)` | mão na massa |
| **Encerramento** | `#s19`: `.big` + `.sub` + `.sig` + `.host` | frase de impacto + CTA |
| **Helpers** | `.grad` `.gold` `.ruleg` `.eyebrow` | destaques |

> Para um novo componente, copie o `<section>` mais parecido do `template_deck.html` e adapte. NÃO recrie o CSS do zero.

---

## 🧠 METODOLOGIA DE CONTEÚDO (arco de palestra)

1. **Capa** — tema + quem apresenta + quando
2. **Agenda** — o que vamos destravar
3. **Hook** — pergunta que dói (gera identificação)
4. **Conceito central** — "o que é, de verdade"
5. **A virada** — o insight/contraste-chave
6. **Do zero** — 1 conceito por slide (componente `concept`)
7. **Pilares/Produtos** — grid (visão geral) + 1 `detail` por item
8. **Aplicação no negócio** — `areas` + `casebar` com **caso real**
9. **Plano de ação** — `ladder` (degraus práticos)
10. **Demo** — `demolist`
11. **Encerramento** — frase de impacto + CTA

**Regra de ouro:** 1 slide = 1 ideia · frases curtas · sempre destacar a palavra-chave do título em dourado (`.grad`).

---

## ⚙️ PIPELINE (sempre nesta ordem)

1. **Copiar o template** para uma pasta do evento:
   ```
   cp "MARKETING/_KIT_APRESENTACAO/template_deck.html" "MARKETING/<EVENTO>/<nome>.html"
   ```
2. **Editar os `<section class="slide">`** com o conteúdo, usando os componentes acima. Ajustar numeração `pageno` e total `/ NN`.
3. **Renderizar:**
   ```
   python MARKETING/_KIT_APRESENTACAO/render.py "MARKETING/<EVENTO>/<nome>.html"
   ```
4. **REVISAR os PNGs** (`Read` nas imagens de `<nome>_slides/`) — caçar overflow de texto/fonte. Corrigir e re-renderizar se preciso. **Nunca pular esta etapa.**
5. **Subir como Google Slides** (+ PDF + HTML):
   ```
   python MARKETING/_KIT_APRESENTACAO/subir_google_slides.py "MARKETING/<EVENTO>/<nome>.html" --nome "Titulo" --pasta "Marketing"
   ```
6. **Entregar os 3 links:** Google Slides (apresentar), PDF (backup), HTML (interativo).

---

## ✅ REGRAS

- **Sempre revisar os PNGs antes de subir.** Texto cortado na frente da plateia é inaceitável.
- Slides viram imagem em tela cheia → idêntico ao design em qualquer projetor.
- **Não criar pastas novas no Drive** sem autorização (usa pasta existente; senão raiz).
- `device_scale_factor=2` → alta resolução (já no render.py).
- O HTML no Drive **não** renderiza como página; para a versão interativa, baixar e abrir no Chrome (setas + `F` tela cheia).
- Paleta padrão = dark+dourado. Se o cliente pedir outra identidade (ex.: PAB roxo/ouro), trocar só as CSS vars, mantendo a estrutura.
- Petições/peças jurídicas NÃO usam esta skill (usam o timbrado PAB).

Referência viva: `MARKETING/OFICINA_PALLADIUM/` (a primeira apresentação neste padrão).
