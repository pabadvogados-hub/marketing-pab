# Marketing PAB - especialistas, skills e automações

Kit de marketing jurídico do PAB Advogados, montado para ser compartilhado. Tudo aqui é método e ferramenta: não há dados de clientes, tokens ou senhas. Telefones e IDs de conta de anúncio foram trocados por zeros (`5511900000000`, `000000000000`). Troque pelos seus.

## O que tem

| Pasta | Conteúdo |
|---|---|
| `agentes/` | Especialistas (subagentes do Claude Code): **Benjamin Roch.ai** (expansão estratégica, marketing jurídico, Provimento 205/2021 OAB, precificação) e **Estrategista Método Éuro** (organograma, POPs, fluxos, cargos) |
| `skills/` | **lexel-marketing** (marketing jurídico), **design-expert / ARIA** (carrosséis e posts HTML/SVG), **apresentacao-premium** (decks), skill `brand`, e `references/` com fórmulas de copy, identidade da marca e template para criar novas skills |
| `conteudo/` | Máquina de artigos: busca notícias jurídicas, gera o artigo com IA e prepara para o Jusbrasil |
| `agencia-conteudo/` | Gerador diário de roteiros de vídeo curto (5 por dia) + banco de roteiros de reserva |
| `carrosseis/` | Geração de carrosséis e slides, exportação de imagens, templates e placeholders |
| `apresentacoes/` | Pipeline HTML -> PDF/PPTX -> Google Slides (`render.py`, `subir_google_slides.py`, `template_deck.html`) |
| `campanhas/` | **Kit de campanha Meta Ads** para caminhoneiros: guia passo a passo, blueprint da campanha vencedora, integração com a Graph API, dashboards, mapa de calor e landing page de calculadora |

## Como usar com o Claude Code

1. Copie os arquivos de `agentes/` para `.claude/agents/` do seu projeto.
2. Copie `skills/` para `.claude/skills/` (o arquivo `brand-SKILL.md` vira `brand/SKILL.md`).
3. Em `skills/references/brand-pab.md`, troque a identidade visual pela do seu escritório.
4. Para as campanhas, comece por `campanhas/KIT_CAMPANHA_AUTOMACAO/GUIA_ALUNO.md` e copie `.env.example` para `.env` com as suas chaves. Nunca suba o `.env` preenchido.

## Antes de publicar qualquer coisa

Respeite o Provimento 205/2021 da OAB (sem captação indevida, sem promessa de resultado) e revise o texto gerado por IA.
