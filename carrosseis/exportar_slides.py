"""
Exportador de Carrossel HTML → PNG
Converte cada slide do carrossel em imagem 1080x1080 pronta pro Instagram.

Uso:
    python MARKETING/exportar_slides.py MARKETING/posts_gerados/arquivo.html
"""

import sys
import os
from pathlib import Path
from playwright.sync_api import sync_playwright


def exportar_slides(html_path: str, output_dir: str = None, size: int = 1080):
    """Abre o HTML, extrai cada slide como HTML isolado e tira screenshot."""
    import re

    html_path = os.path.abspath(html_path)
    if not os.path.exists(html_path):
        print(f"ERRO: Arquivo nao encontrado: {html_path}")
        sys.exit(1)

    if not output_dir:
        output_dir = os.path.join(os.path.dirname(html_path), Path(html_path).stem + '_slides')

    os.makedirs(output_dir, exist_ok=True)

    # Ler HTML original
    with open(html_path, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Extrair bloco <style>
    style_match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
    styles = style_match.group(1) if style_match else ''

    # Extrair link de fontes
    font_links = re.findall(r'<link[^>]*googleapis[^>]*>', html_content)
    font_html = '\n'.join(font_links)

    # Extrair slides usando Playwright para pegar o HTML de cada .slide
    slides = []
    with sync_playwright() as p_temp:
        br = p_temp.chromium.launch()
        pg = br.new_page()
        pg.goto(f'file:///{html_path.replace(os.sep, "/")}')
        pg.wait_for_timeout(1000)
        total_count = pg.evaluate('document.querySelectorAll(".slide").length')
        for idx in range(total_count):
            outer = pg.evaluate(f'document.querySelectorAll(".slide")[{idx}].outerHTML')
            slides.append(outer)
        br.close()

    total = len(slides)
    print(f"Encontrados {total} slides. Exportando em {size}x{size}px...\n")

    with sync_playwright() as p:
        browser = p.chromium.launch()

        for i, slide_html in enumerate(slides):
            # Criar HTML isolado para cada slide
            single_html = f'''<!DOCTYPE html>
<html><head>
<meta charset="UTF-8">
{font_html}
<style>
{styles}

/* Override para screenshot */
* {{ margin: 0; padding: 0; box-sizing: border-box; transition: none !important; animation: none !important; }}
body {{ width: {size}px; height: {size}px; overflow: hidden; }}
.carousel-wrapper {{ display: none; }}
.slide {{
    position: relative !important;
    width: {size}px !important;
    height: {size}px !important;
    opacity: 1 !important;
    transform: none !important;
    pointer-events: all !important;
}}
.nav-arrow, .dots, .counter, .progress-bar {{ display: none !important; }}
.slide-header {{ position: absolute; top: 18px; left: 44px; right: 44px; }}
</style>
</head>
<body>
{slide_html}
</body></html>'''

            # Salvar HTML temporario
            temp_path = os.path.join(output_dir, f'_temp_{i}.html')
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(single_html)

            # Screenshot
            page = browser.new_page(viewport={'width': size, 'height': size})
            page.goto(f'file:///{temp_path.replace(os.sep, "/")}')
            page.wait_for_timeout(2000)  # Aguardar fontes

            filename = f'slide_{i+1:02d}.png'
            filepath = os.path.join(output_dir, filename)
            page.screenshot(path=filepath, type='png')
            page.close()

            # Limpar temp
            os.remove(temp_path)
            print(f"  OK: {filename} exportado")

        browser.close()

    print(f"\n{'='*50}")
    print(f"  {total} slides exportados em: {output_dir}")
    print(f"  Formato: {size}x{size}px PNG")
    print(f"  Pronto pra postar no Instagram!")
    print(f"{'='*50}")

    return output_dir


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Uso: python MARKETING/exportar_slides.py <arquivo.html> [--size 1080]")
        sys.exit(1)

    html = sys.argv[1]
    size = 1080
    if '--size' in sys.argv:
        idx = sys.argv.index('--size')
        size = int(sys.argv[idx + 1])

    exportar_slides(html, size=size)
