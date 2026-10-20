"""
KIT APRESENTACAO PREMIUM - Renderizador
Converte um deck HTML (16:9) em PNGs 1920x1080 (alta resolucao) + PDF.

Uso:
    python MARKETING/_KIT_APRESENTACAO/render.py "caminho/do/deck.html"

Saida (ao lado do HTML):
    <stem>_slides/slide_01.png ...      e      <stem>.pdf
"""
import os
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

W, H = 1920, 1080


def render(html_path: str, scale: int = 2):
    html_path = os.path.abspath(html_path)
    if not os.path.exists(html_path):
        print("ERRO: HTML nao encontrado:", html_path); sys.exit(1)

    stem = Path(html_path).stem
    base = os.path.dirname(html_path)
    out = os.path.join(base, stem + "_slides")
    pdf = os.path.join(base, stem + ".pdf")
    os.makedirs(out, exist_ok=True)

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()
    styles = (re.search(r"<style>(.*?)</style>", html, re.DOTALL) or [None, ""])[1]
    fonts = "\n".join(re.findall(r"<link[^>]*(?:googleapis|gstatic)[^>]*>", html))
    file_url = "file:///" + html_path.replace(os.sep, "/")

    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page()
        pg.goto(file_url); pg.wait_for_timeout(800)
        n = pg.evaluate('document.querySelectorAll(".slide").length')
        slides = [pg.evaluate(f'document.querySelectorAll(".slide")[{k}].outerHTML') for k in range(n)]
        br.close()

    print(f"{n} slides. Renderizando {W}x{H} (x{scale})...\n")
    override = f"""
* {{ transition:none !important; animation:none !important; }}
html,body {{ width:{W}px; height:{H}px; overflow:hidden; background:#000; }}
.slide {{ position:absolute !important; inset:0 !important; width:{W}px !important; height:{H}px !important;
         opacity:1 !important; visibility:visible !important; transform:none !important; }}
.progress,.navhint {{ display:none !important; }}
"""
    paths = []
    with sync_playwright() as p:
        br = p.chromium.launch()
        for k, shtml in enumerate(slides):
            doc = (f'<!DOCTYPE html><html lang="pt-BR"><head><meta charset="UTF-8">{fonts}'
                   f'<style>{styles}\n{override}</style></head><body>{shtml}</body></html>')
            tmp = os.path.join(out, f"_tmp_{k}.html")
            with open(tmp, "w", encoding="utf-8") as f:
                f.write(doc)
            page = br.new_page(viewport={"width": W, "height": H}, device_scale_factor=scale)
            page.goto("file:///" + tmp.replace(os.sep, "/"))
            try:
                page.evaluate("document.fonts.ready")
            except Exception:
                pass
            page.wait_for_timeout(1600)
            outpng = os.path.join(out, f"slide_{k+1:02d}.png")
            page.screenshot(path=outpng, type="png")
            page.close(); os.remove(tmp); paths.append(outpng)
            print(f"  OK slide_{k+1:02d}.png")
        br.close()

    try:
        from PIL import Image
        imgs = [Image.open(p).convert("RGB") for p in paths]
        imgs[0].save(pdf, save_all=True, append_images=imgs[1:], resolution=144.0)
        print(f"\nPDF: {pdf}")
    except Exception as e:
        print(f"\n[aviso] PDF via Pillow falhou ({e}); usando Playwright.")
        with sync_playwright() as p:
            br = p.chromium.launch(); page = br.new_page()
            page.goto(file_url); page.wait_for_timeout(800)
            page.pdf(path=pdf, width=f"{W}px", height=f"{H}px", print_background=True)
            br.close()
        print(f"PDF: {pdf}")

    print(f"PNGs: {out}")
    return out, pdf


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print('Uso: python render.py "caminho/deck.html"'); sys.exit(1)
    render(sys.argv[1])
