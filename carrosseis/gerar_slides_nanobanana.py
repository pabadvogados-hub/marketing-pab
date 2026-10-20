"""
Gerador de Slides com Nano Banana Pro (Gemini Image API)
Gera imagens 1080x1080 de alta qualidade para carrossel Instagram.

Uso:
    python MARKETING/gerar_slides_nanobanana.py MARKETING/posts_gerados/arquivo.json
    python MARKETING/gerar_slides_nanobanana.py MARKETING/posts_gerados/arquivo.json --modelo flash
"""

import os
import sys
import json
import argparse
import base64
from pathlib import Path
from dotenv import load_dotenv

PROJECT_ROOT = os.path.join(os.path.dirname(__file__), '..')
load_dotenv(os.path.join(PROJECT_ROOT, 'config', '.env'))

GOOGLE_API_KEY = os.getenv('GOOGLE_AI_API_KEY', os.getenv('GEMINI_API_KEY', ''))

# Prompt base de estilo visual
STYLE_PROMPT = """You are a world-class graphic designer creating an Instagram carousel slide.

STRICT VISUAL RULES:
- Dimensions: exactly 1080x1080 pixels, square format
- Typography: Bold, condensed, uppercase headlines. Clean sans-serif body text.
- Color palette: Primary gold #C9A84C, black #0A0A0A, off-white #F5F0E8
- Layout: Content positioned in the bottom 60% of the slide, lots of breathing space at top
- Header: Small text "@wpcasalda.ia" top-right, very subtle gray
- A thin gold decorative line above the label text
- Gold progress bar at the very bottom (3px height)
- Page counter bottom-right (e.g. "1/7")
- Style reference: Premium editorial, like a high-end magazine or @advogadopremium Instagram
- All text must be in BRAZILIAN PORTUGUESE
- Text must be PERFECTLY READABLE, sharp and clear
- NO stock photos, NO people, purely typographic/graphic design
"""

DARK_SLIDE = """BACKGROUND: Deep purple (#1A0A2E) with subtle gradient to (#2D1B69). Gold accents.
Text color: White (#F8FAFC) for body, Gold (#C9A84C) for highlighted headline words.
Cards and borders use purple (#5B21B6) with translucent purple backgrounds.
"""

LIGHT_SLIDE = """BACKGROUND: Warm cream/off-white (#F5F0E8). Elegant and clean.
Text color: Dark purple (#1A0A2E) for body, Gold (#C9A84C) for highlighted headline words.
Cards with white background, subtle purple (#5B21B6) border, rounded corners.
"""


def build_slide_prompts(slides_data: dict) -> list:
    """Constroi prompts especificos para cada slide."""
    s = slides_data

    prompts = [
        # Slide 1 - CAPA (escuro)
        f"""{STYLE_PROMPT}
{DARK_SLIDE}
SLIDE 1 of 7 — COVER SLIDE

Small gold label at top of content area: "{s['LABEL_1']}"
Main headline in HUGE bold white text:
"{s['HEAD_1A']}"
Below that, the word "{s['HEAD_1B']}" in GOLD color, same huge bold size.

Below headline, smaller subtitle in light gray:
"{s['SUB_1']}"

At bottom, small gold text: "Desliza pra descobrir →"
A large decorative "?" character at very low opacity (3%) in the background right area.
Progress bar at bottom showing 1/7 filled.""",

        # Slide 2 - PROBLEMA (escuro)
        f"""{STYLE_PROMPT}
{DARK_SLIDE}
SLIDE 2 of 7 — PROBLEM SLIDE

Small gold label: "{s['LABEL_2']}"
Main headline bold white:
"{s['HEAD_2A']}"
Next line in GOLD: "{s['HEAD_2B']}"

Below, body text in smaller white font (readable):
"{s['BODY_2']}"

Decorative "2" number at very low opacity in background.
Progress bar showing 2/7.""",

        # Slide 3 - FLUXO (claro)
        f"""{STYLE_PROMPT}
{LIGHT_SLIDE}
SLIDE 3 of 7 — SOLUTION/FLOW SLIDE

Small gold label: "{s['LABEL_3']}"
Headline in bold black: "{s['HEAD_3A']}"
Next line in GOLD: "{s['HEAD_3B']}"

Below, 4 cards in a 2x2 grid layout, each with:
Card 1: Gold label "{s['CARD_3A_LABEL']}" / Text "{s['CARD_3A_TEXT']}"
Card 2: Gold label "{s['CARD_3B_LABEL']}" / Text "{s['CARD_3B_TEXT']}"
Card 3: Gold label "{s['CARD_3C_LABEL']}" / Text "{s['CARD_3C_TEXT']}"
Card 4: Gold label "{s['CARD_3D_LABEL']}" / Text "{s['CARD_3D_TEXT']}"

Cards have white background, subtle border, rounded corners.
Progress bar showing 3/7.""",

        # Slide 4 - DETALHE 1 (escuro)
        f"""{STYLE_PROMPT}
{DARK_SLIDE}
SLIDE 4 of 7 — DETAIL SLIDE

Small gold label: "{s['LABEL_4']}"
Headline bold white: "{s['HEAD_4A']}"
Next line in GOLD: "{s['HEAD_4B']}"

Below, 3 stacked cards with dark glass effect:
Card 1 — Gold label "ENTRADA" / White text: "{s['INPUT_4']}"
Card 2 — Gold label "PROCESSAMENTO" / White text: "{s['PROCESS_4']}"
Card 3 — Gold label "SAIDA" / White text: "{s['RESULT_4']}"

Cards have subtle gold border, dark translucent background.
Progress bar showing 4/7.""",

        # Slide 5 - DETALHE 2 (escuro)
        f"""{STYLE_PROMPT}
{DARK_SLIDE}
SLIDE 5 of 7 — COMPARISON SLIDE

Small gold label: "{s['LABEL_5']}"
Headline bold white: "{s['HEAD_5A']}"
Next line in GOLD: "{s['HEAD_5B']}"

A comparison table with 3 columns:
Header row: SKILL | ANTES | COM CLAUDE (gold text for last column)
Row 1: "{s['TAB_5A_SKILL']}" | "{s['TAB_5A_ANTES']}" | "{s['TAB_5A_IA']}" (gold)
Row 2: "{s['TAB_5B_SKILL']}" | "{s['TAB_5B_ANTES']}" | "{s['TAB_5B_IA']}" (gold)

Below table, a card with gold tinted background:
Label "PROMPT REAL USADO"
Italic text: "{s['PROMPT_5']}"

Progress bar showing 5/7.""",

        # Slide 6 - RESULTADO (claro)
        f"""{STYLE_PROMPT}
{LIGHT_SLIDE}
SLIDE 6 of 7 — RESULTS SLIDE

Small gold label: "{s['LABEL_6']}"
Headline bold black: "{s['HEAD_6A']}"
Next line in GOLD: "{s['HEAD_6B']}"

3 metrics, each with a gold left border bar (3px):
Metric 1: "{s['METRIC_6A']}" — bold the number/key data
Metric 2: "{s['METRIC_6B']}" — bold the number/key data
Metric 3: "{s['METRIC_6C']}" — bold the number/key data

Closing quote in italic at bottom:
"{s['CLOSING_6']}"

Progress bar showing 6/7.""",

        # Slide 7 - CTA (claro)
        f"""{STYLE_PROMPT}
{LIGHT_SLIDE}
SLIDE 7 of 7 — CTA FINAL SLIDE

Italic intro text near middle: "{s['INTRO_7']}"

Bold headline black: "{s['HEAD_7A']}"
Next line in GOLD: "{s['HEAD_7B']}"

Below, a prominent CTA box with gold border, centered:
Small text: "{s['CTA_7_INST']}"
HUGE gold text: "{s['CTA_7_WORD']}"
Small text below: "{s['CTA_7_DETAIL']}"

At bottom: gold dot + "@wpcasalda.ia - Envio automatico via DM"

Progress bar showing 7/7 (full).""",
    ]

    return prompts


def gerar_slides(json_path: str, output_dir: str = None, modelo: str = 'flash'):
    """Gera imagens dos slides usando Nano Banana Pro."""
    from google import genai
    from google.genai import types

    if not GOOGLE_API_KEY:
        print("ERRO: GOOGLE_AI_API_KEY ou GEMINI_API_KEY nao encontrada no config/.env")
        print("Pegue sua chave em: https://aistudio.google.com/apikey")
        sys.exit(1)

    # Carregar conteudo
    with open(json_path, 'r', encoding='utf-8') as f:
        dados = json.load(f)

    slides_data = dados.get('slides', dados)

    if not output_dir:
        slug = Path(json_path).stem
        output_dir = os.path.join(os.path.dirname(json_path), f'{slug}_nanobanana')

    os.makedirs(output_dir, exist_ok=True)

    # Selecionar modelo
    if modelo == 'pro':
        model_name = 'nano-banana-pro-preview'
    else:
        model_name = 'gemini-2.5-flash-image'

    print(f"Modelo: {model_name}")
    print(f"Gerando 7 slides com Nano Banana...\n")

    client = genai.Client(api_key=GOOGLE_API_KEY)
    prompts = build_slide_prompts(slides_data)

    for i, prompt in enumerate(prompts):
        print(f"  Gerando slide {i+1}/7...", end=' ', flush=True)

        try:
            response = client.models.generate_content(
                model=model_name,
                contents=[prompt],
                config=types.GenerateContentConfig(
                    response_modalities=['IMAGE', 'TEXT'],
                ),
            )

            # Salvar imagem
            saved = False
            for part in response.candidates[0].content.parts:
                if part.inline_data is not None:
                    filepath = os.path.join(output_dir, f'slide_{i+1:02d}.png')
                    img_data = part.inline_data.data
                    if isinstance(img_data, str):
                        img_data = base64.b64decode(img_data)
                    with open(filepath, 'wb') as f:
                        f.write(img_data)
                    print(f"OK - salvo!")
                    saved = True
                    break

            if not saved:
                print("AVISO: Nenhuma imagem retornada")
                # Tentar pegar texto de erro
                for part in response.candidates[0].content.parts:
                    if part.text:
                        print(f"    Resposta: {part.text[:200]}")

        except Exception as e:
            print(f"ERRO: {e}")

    print(f"\n{'='*50}")
    print(f"  Slides exportados em: {output_dir}")
    print(f"  Pronto pra postar no Instagram!")
    print(f"{'='*50}")

    return output_dir


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Gerar slides com Nano Banana Pro')
    parser.add_argument('json_path', help='Caminho do JSON com conteudo dos slides')
    parser.add_argument('--modelo', choices=['flash', 'pro'], default='flash',
                        help='flash = rapido/gratis | pro = alta qualidade')
    parser.add_argument('--output', help='Pasta de saida', default=None)
    args = parser.parse_args()

    gerar_slides(args.json_path, output_dir=args.output, modelo=args.modelo)
