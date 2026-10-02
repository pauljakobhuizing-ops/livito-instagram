"""Rendert die Folien aus slides.html nach ../media/karussell/<serie>-<nr>.png.
Aufruf: render_slides.py [praefix ...]   ohne Angabe werden alle Folien gerendert, sonst nur die mit passendem Anfang (z. B. frage methode-6)."""
import os, sys
from playwright.sync_api import sync_playwright
W = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(W, '..', 'media', 'karussell'))
os.makedirs(OUT, exist_ok=True)
nur = sys.argv[1:]
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
    pg.goto('file://' + W + '/slides.html')
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(400)
    ids = pg.eval_on_selector_all('.slide', 'els => els.map(e => e.id)')
    if nur: ids = [i for i in ids if any(i.startswith(n) for n in nur)]
    over = []
    for i in ids:
        pg.locator('#' + i).screenshot(path=f'{OUT}/{i}.png')
        # Ueberlauf pruefen: Inhalt hoeher als die Folie?
        sh, ch = pg.evaluate(f"(()=>{{const e=document.getElementById('{i}');return [e.scrollHeight,e.clientHeight]}})()")
        if sh > ch: over.append((i, sh, ch))
    print('Folien:', len(ids), ids)
    print('Ueberlauf:', over)
    b.close()
