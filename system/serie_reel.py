"""Baut Reels fuer die Serien aus den Rohdaten in slides.html (C[key].raw).
Aufruf: serie_reel.py <key> [<key> ...] [--stills]
Ergebnis: ../media/reels/reel-<key>.mp4; gibt Dauer und Titelbild-Zeitpunkt (ms) aus.
Klang: Geldwoerter 2 (Klavier), Lieber oder 1 (Flaeche), Warum wir so ticken und Gelassen mit Geld 3 (Puls)."""
import sys, os, json, subprocess, tempfile
from playwright.sync_api import sync_playwright
W = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(W, '..', 'media', 'reels'))
KLANG = {'wort': '2-klavier.wav', 'lieber': '1-flaeche.wav', 'ticken': '3-puls.wav', 'buch': '3-puls.wav'}
FPS = 30
keys = [a for a in sys.argv[1:] if not a.startswith('--')]
stills = '--stills' in sys.argv
info = {}
with sync_playwright() as p:
    b = p.chromium.launch()
    src = b.new_page(); src.goto('file://' + W + '/slides.html')
    pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
    pg.goto('file://' + W + '/serie_reel.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
    for key in keys:
        raw = src.evaluate(f'C["{key}"].raw')
        r = pg.evaluate('raw => setTL(raw)', raw)
        dur, cover = r['dur'], r['cover']
        info[key] = {'dur': dur, 'cover_ms': int(cover * 1000)}
        if stills:
            os.makedirs(W + '/frames', exist_ok=True)
            ts = pg.evaluate('SC.map(s => Math.max(s.a + .3, s.b - .4))')
            for i, t in enumerate(ts):
                pg.evaluate(f'setTime({t})'); pg.screenshot(path=f'{W}/frames/{key}-{i}.png')
            continue
        tmp = tempfile.mkdtemp()
        typ = raw['typ']
        subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-stream_loop', '-1', '-i', f'{W}/klang/{KLANG[typ]}', '-t', str(dur),
                        '-af', f'afade=t=in:st=0:d=0.3,afade=t=out:st={dur - 1.2}:d=1.2', f'{tmp}/bett.wav'], check=True)
        out = f'{OUT}/reel-{key}.mp4'
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-i', f'{tmp}/bett.wav', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'veryfast', '-r', str(FPS),
                               '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
        for k in range(int(round(dur * FPS))):
            pg.evaluate(f'setTime({k / FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=93))
        ff.stdin.close(); ff.wait()
        pg.evaluate(f'setTime({cover})'); pg.screenshot(path=f'{OUT}/poster-{key}.jpg', type='jpeg', quality=88)
    b.close()
print(json.dumps(info))
