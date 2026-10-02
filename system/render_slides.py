import os, sys
from playwright.sync_api import sync_playwright
W = os.path.dirname(os.path.abspath(__file__))
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
    pg.goto('file://' + W + '/slides.html')
    pg.evaluate('document.fonts.ready')
    pg.wait_for_timeout(400)
    ids = pg.eval_on_selector_all('.slide', 'els => els.map(e => e.id)')
    over = []
    for i in ids:
        el = pg.locator('#' + i)
        el.screenshot(path=f'{W}/slides/{i}.png')
        # Ueberlauf pruefen: Inhalt hoeher als die Folie?
        sh, ch = pg.evaluate(f"(()=>{{const e=document.getElementById('{i}');return [e.scrollHeight,e.clientHeight]}})()")
        if sh > ch: over.append((i, sh, ch))
    print('Folien:', len(ids), ids)
    print('Ueberlauf:', over)
    b.close()
