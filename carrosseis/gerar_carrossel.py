"""
Gerador de Carrossel Instagram - PAB Marketing
Gera conteudo para 7 slides no estilo @advogadopremium
e injeta no template master do Canva.

Uso:
    python MARKETING/gerar_carrossel.py "tema do post"
    python MARKETING/gerar_carrossel.py "tema do post" --template DESIGN_ID
    python MARKETING/gerar_carrossel.py "tema do post" --apenas-conteudo
"""

import os
import sys
import json
import argparse
from dotenv import load_dotenv

# Carregar .env
PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
load_dotenv(os.path.join(PROJECT_ROOT, 'config', '.env'))

ANTHROPIC_API_KEY = os.getenv('ANTHROPIC_API_KEY')

# ID do template master no Canva (atualizar quando criar)
TEMPLATE_ID = os.getenv('CANVA_TEMPLATE_CARROSSEL', '')

PROMPT_SISTEMA = """Voce e um copywriter especialista em conteudo para Instagram no estilo editorial premium.
Voce cria carrosseis no estilo do @advogadopremium: direto, impactante, com frases curtas e poderosas.

REGRAS DE ESTILO:
- Headlines: CURTAS, BOLD, IMPACTANTES. Maximo 4 palavras por linha.
- Uma palavra ou frase por headline deve ser o DESTAQUE (sera dourada).
- Labels: sempre uppercase, curtos (2-4 palavras). Ex: "CASO REAL 2026", "O PROBLEMA"
- Texto corpo: conversacional, direto, sem firula. Como se falasse com um amigo advogado.
- CTAs: agressivos mas elegantes. Comandos claros.
- Tom: autoridade + acessibilidade. "Nos ja fizemos, voce tambem pode."
- NUNCA use linguagem generica de marketing. Seja especifico e real.
- Slides escuros = impacto/problema/tecnico. Slides claros = solucao/resultado/CTA.

ESTRUTURA DO CARROSSEL (7 slides):
1. CAPA (escuro) - Gancho forte, numero ou dado impactante
2. PROBLEMA (escuro) - Dor real do publico, headline provocativa
3. FLUXO/SOLUCAO (claro) - Como funciona, 4 etapas em cards
4. DETALHE 1 (escuro) - Aprofunda uma etapa especifica com input/output
5. DETALHE 2 (escuro) - Segunda etapa com comparacao antes/depois
6. RESULTADO (claro) - Metricas reais, numeros, prova social
7. CTA (claro) - Frase de autoridade + chamada pra acao com palavra-gatilho

O perfil e @wpcasalda.ia (Weverton & Pamella), advogados que automatizam escritorios com IA.
"""

PROMPT_GERAR = """Gere o conteudo completo para um carrossel de 7 slides sobre o tema: "{tema}"

Retorne APENAS um JSON valido (sem markdown, sem ```), com esta estrutura exata:

{{
  "titulo_post": "titulo curto para referencia interna",
  "legenda": "legenda completa para o Instagram (com emojis, CTA, hashtags)",
  "slides": {{
    "LABEL_1": "...", "HEAD_1A": "...", "HEAD_1B": "...", "SUB_1": "...",
    "LABEL_2": "...", "HEAD_2A": "...", "HEAD_2B": "...", "BODY_2": "...",
    "LABEL_3": "...", "HEAD_3A": "...", "HEAD_3B": "...",
    "CARD_3A_LABEL": "...", "CARD_3A_TEXT": "...",
    "CARD_3B_LABEL": "...", "CARD_3B_TEXT": "...",
    "CARD_3C_LABEL": "...", "CARD_3C_TEXT": "...",
    "CARD_3D_LABEL": "...", "CARD_3D_TEXT": "...",
    "LABEL_4": "...", "HEAD_4A": "...", "HEAD_4B": "...",
    "INPUT_4": "...", "PROCESS_4": "...", "RESULT_4": "...",
    "LABEL_5": "...", "HEAD_5A": "...", "HEAD_5B": "...",
    "TAB_5A_SKILL": "...", "TAB_5A_ANTES": "...", "TAB_5A_IA": "...",
    "TAB_5B_SKILL": "...", "TAB_5B_ANTES": "...", "TAB_5B_IA": "...",
    "PROMPT_5": "...",
    "LABEL_6": "...", "HEAD_6A": "...", "HEAD_6B": "...",
    "METRIC_6A": "...", "METRIC_6B": "...", "METRIC_6C": "...", "CLOSING_6": "...",
    "INTRO_7": "...", "HEAD_7A": "...", "HEAD_7B": "...",
    "CTA_7_INST": "...", "CTA_7_WORD": "...", "CTA_7_DETAIL": "..."
  }}
}}

IMPORTANTE:
- HEAD_1B, HEAD_2B, HEAD_3B, HEAD_4B, HEAD_5B, HEAD_6B, HEAD_7B sao as palavras que ficam em DOURADO (destaque)
- Headlines devem ser UPPERCASE
- Seja especifico ao tema, use dados reais quando possivel
- A legenda deve ter CTA forte, emojis e ~20 hashtags relevantes
"""


def gerar_conteudo(tema: str) -> dict:
    """Gera conteudo do carrossel usando Claude API."""
    import anthropic

    if not ANTHROPIC_API_KEY:
        print("ERRO: ANTHROPIC_API_KEY nao encontrada no config/.env")
        sys.exit(1)

    client = anthropic.Anthropic(api_key=ANTHROPIC_API_KEY)

    print(f"Gerando conteudo para: {tema}...")

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=4000,
        system=PROMPT_SISTEMA,
        messages=[{"role": "user", "content": PROMPT_GERAR.format(tema=tema)}]
    )

    texto = response.content[0].text.strip()

    # Limpar possivel markdown
    if texto.startswith("```"):
        texto = texto.split("\n", 1)[1]
        if texto.endswith("```"):
            texto = texto[:-3]

    # Tentar extrair JSON mesmo com texto extra
    try:
        dados = json.loads(texto)
    except json.JSONDecodeError:
        # Tentar encontrar JSON dentro da resposta
        import re
        match = re.search(r'\{[\s\S]*\}', texto)
        if match:
            try:
                dados = json.loads(match.group())
            except json.JSONDecodeError as e:
                print(f"ERRO ao parsear JSON: {e}")
                # Salvar resposta bruta para debug
                debug_path = os.path.join(os.path.dirname(__file__), 'posts_gerados', '_debug_last.txt')
                os.makedirs(os.path.dirname(debug_path), exist_ok=True)
                with open(debug_path, 'w', encoding='utf-8') as f:
                    f.write(texto)
                print(f"Resposta salva em: {debug_path}")
                sys.exit(1)
        else:
            print("ERRO: Nenhum JSON encontrado na resposta.")
            sys.exit(1)

    return dados


def salvar_conteudo(dados: dict, tema: str):
    """Salva o conteudo gerado em JSON e MD para referencia."""
    output_dir = os.path.join(os.path.dirname(__file__), 'posts_gerados')
    os.makedirs(output_dir, exist_ok=True)

    # Nome do arquivo baseado no titulo
    slug = dados.get('titulo_post', tema)[:50].lower()
    slug = ''.join(c if c.isalnum() or c == ' ' else '' for c in slug).strip().replace(' ', '_')

    # Salvar JSON (para injecao no Canva)
    json_path = os.path.join(output_dir, f'{slug}.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(dados, f, ensure_ascii=False, indent=2)

    # Salvar MD legivel (para revisao)
    md_path = os.path.join(output_dir, f'{slug}.md')
    slides = dados.get('slides', {})
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(f"# {dados.get('titulo_post', tema)}\n\n")

        f.write("## SLIDE 1 - CAPA\n")
        f.write(f"**{slides.get('LABEL_1', '')}**\n")
        f.write(f"# {slides.get('HEAD_1A', '')}\n")
        f.write(f"# **{slides.get('HEAD_1B', '')}**\n")
        f.write(f"_{slides.get('SUB_1', '')}_\n\n")

        f.write("## SLIDE 2 - PROBLEMA\n")
        f.write(f"**{slides.get('LABEL_2', '')}**\n")
        f.write(f"# {slides.get('HEAD_2A', '')}\n")
        f.write(f"# **{slides.get('HEAD_2B', '')}**\n")
        f.write(f"{slides.get('BODY_2', '')}\n\n")

        f.write("## SLIDE 3 - FLUXO\n")
        f.write(f"**{slides.get('LABEL_3', '')}**\n")
        f.write(f"# {slides.get('HEAD_3A', '')} **{slides.get('HEAD_3B', '')}**\n")
        for letter in ['A', 'B', 'C', 'D']:
            label = slides.get(f'CARD_3{letter}_LABEL', '')
            text = slides.get(f'CARD_3{letter}_TEXT', '')
            f.write(f"- **{label}:** {text}\n")
        f.write("\n")

        f.write("## SLIDE 4 - DETALHE 1\n")
        f.write(f"**{slides.get('LABEL_4', '')}**\n")
        f.write(f"# {slides.get('HEAD_4A', '')} **{slides.get('HEAD_4B', '')}**\n")
        f.write(f"- Input: {slides.get('INPUT_4', '')}\n")
        f.write(f"- Processo: {slides.get('PROCESS_4', '')}\n")
        f.write(f"- Resultado: {slides.get('RESULT_4', '')}\n\n")

        f.write("## SLIDE 5 - DETALHE 2\n")
        f.write(f"**{slides.get('LABEL_5', '')}**\n")
        f.write(f"# {slides.get('HEAD_5A', '')} **{slides.get('HEAD_5B', '')}**\n")
        f.write(f"| Skill | Antes | Com IA |\n|---|---|---|\n")
        f.write(f"| {slides.get('TAB_5A_SKILL', '')} | {slides.get('TAB_5A_ANTES', '')} | {slides.get('TAB_5A_IA', '')} |\n")
        f.write(f"| {slides.get('TAB_5B_SKILL', '')} | {slides.get('TAB_5B_ANTES', '')} | {slides.get('TAB_5B_IA', '')} |\n")
        f.write(f"_{slides.get('PROMPT_5', '')}_\n\n")

        f.write("## SLIDE 6 - RESULTADO\n")
        f.write(f"**{slides.get('LABEL_6', '')}**\n")
        f.write(f"# {slides.get('HEAD_6A', '')} **{slides.get('HEAD_6B', '')}**\n")
        f.write(f"- {slides.get('METRIC_6A', '')}\n")
        f.write(f"- {slides.get('METRIC_6B', '')}\n")
        f.write(f"- {slides.get('METRIC_6C', '')}\n")
        f.write(f"**{slides.get('CLOSING_6', '')}**\n\n")

        f.write("## SLIDE 7 - CTA\n")
        f.write(f"{slides.get('INTRO_7', '')}\n")
        f.write(f"# {slides.get('HEAD_7A', '')} **{slides.get('HEAD_7B', '')}**\n")
        f.write(f"{slides.get('CTA_7_INST', '')}\n")
        f.write(f"## **{slides.get('CTA_7_WORD', '')}**\n")
        f.write(f"{slides.get('CTA_7_DETAIL', '')}\n\n")

        f.write("---\n\n## LEGENDA\n\n")
        f.write(dados.get('legenda', ''))

    print(f"Conteudo salvo em:")
    print(f"  JSON: {json_path}")
    print(f"  Preview: {md_path}")

    return json_path, md_path


def exibir_preview(dados: dict):
    """Exibe preview do conteudo no terminal."""
    slides = dados.get('slides', {})

    print(f"\n{'='*60}")
    print(f"  {dados.get('titulo_post', 'CARROSSEL')}")
    print(f"{'='*60}")

    print(f"\n  SLIDE 1 | {slides.get('LABEL_1', '')}")
    print(f"  {slides.get('HEAD_1A', '')}")
    print(f"  {slides.get('HEAD_1B', '')}  << GOLD")
    print(f"  {slides.get('SUB_1', '')}")

    print(f"\n  SLIDE 2 | {slides.get('LABEL_2', '')}")
    print(f"  {slides.get('HEAD_2A', '')}")
    print(f"  {slides.get('HEAD_2B', '')}  << GOLD")

    print(f"\n  SLIDE 3 | {slides.get('LABEL_3', '')}")
    print(f"  {slides.get('HEAD_3A', '')} {slides.get('HEAD_3B', '')}  << GOLD")

    print(f"\n  SLIDE 4 | {slides.get('LABEL_4', '')}")
    print(f"  {slides.get('HEAD_4A', '')} {slides.get('HEAD_4B', '')}  << GOLD")

    print(f"\n  SLIDE 5 | {slides.get('LABEL_5', '')}")
    print(f"  {slides.get('HEAD_5A', '')} {slides.get('HEAD_5B', '')}  << GOLD")

    print(f"\n  SLIDE 6 | {slides.get('LABEL_6', '')}")
    print(f"  {slides.get('HEAD_6A', '')} {slides.get('HEAD_6B', '')}  << GOLD")

    print(f"\n  SLIDE 7 | CTA")
    print(f"  {slides.get('HEAD_7A', '')} {slides.get('HEAD_7B', '')}  << GOLD")
    print(f"  CTA: {slides.get('CTA_7_WORD', '')}")

    print(f"\n{'='*60}\n")


# ============================================================
# CLI
# ============================================================
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gerador de Carrossel Instagram - @wpcasalda.ia')
    parser.add_argument('tema', help='Tema do carrossel (ex: "como automatizamos a contratacao")')
    parser.add_argument('--template', help='ID do template Canva (sobrescreve env)', default=TEMPLATE_ID)
    parser.add_argument('--apenas-conteudo', action='store_true', help='Apenas gera conteudo, nao injeta no Canva')
    parser.add_argument('--json', help='Usar JSON existente ao inves de gerar novo')
    args = parser.parse_args()

    # Gerar ou carregar conteudo
    if args.json:
        with open(args.json, 'r', encoding='utf-8') as f:
            dados = json.load(f)
        print(f"Conteudo carregado de: {args.json}")
    else:
        dados = gerar_conteudo(args.tema)

    # Exibir preview
    exibir_preview(dados)

    # Salvar
    json_path, md_path = salvar_conteudo(dados, args.tema)

    if args.apenas_conteudo:
        print("Modo apenas-conteudo. Use o JSON gerado com o Claude Code para injetar no Canva.")
        print(f"\nProximo passo: abra o Claude Code e diga:")
        print(f'  "Injeta o conteudo de {json_path} no template do Canva"')
    else:
        if not args.template:
            print("\nAVISO: Template Canva nao configurado.")
            print("Configure CANVA_TEMPLATE_CARROSSEL no config/.env")
            print("ou passe --template DESIGN_ID")
            print(f"\nPor enquanto, use o JSON gerado com o Claude Code:")
            print(f'  "Injeta o conteudo de {json_path} no template do Canva"')
        else:
            print(f"\nTemplate: {args.template}")
            print("Injecao no Canva sera feita via Claude Code (MCP tools).")
            print(f'Diga: "Injeta {json_path} no template {args.template}"')
