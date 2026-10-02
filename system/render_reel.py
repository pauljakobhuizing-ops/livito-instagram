"""Rendert ein Reel: HTML-Animation mit setTime(t) -> Einzelbilder -> MP4 mit Tonspur.
Aufruf: render_reel.py <html> <dauer> <audio.wav> <out.mp4> [timeline.json] [--stills t1,t2,...]"""
import sys, os, json, subprocess
from playwright.sync_api import sync_playwright
W = os.path.dirname(os.path.abspath(__file__))
html, dur, audio, out = sys.argv[1], float(sys.argv[2]), sys.argv[3], sys.argv[4]
tl = None; stills = None
rest = sys.argv[5:]
for i, a in enumerate(rest):
    if a == '--stills': stills = [float(x) for x in rest[i + 1].split(',')]
    elif a.endswith('.json'): tl = json.load(open(a))
FPS = 30
with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
    pg.goto('file://' + W + '/' + html)
    pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(500)
    if tl: pg.evaluate('tl => setTL(tl)', tl)
    if stills:
        for t in stills:
            pg.evaluate(f'setTime({t})'); pg.screenshot(path=f'{W}/frames/{os.path.splitext(html)[0]}-{t:05.2f}.png')
        print('Standbilder:', stills)
    else:
        ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                               '-i', audio, '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'medium', '-r', str(FPS),
                               '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
        n = int(round(dur * FPS))
        for k in range(n):
            pg.evaluate(f'setTime({k / FPS})')
            ff.stdin.write(pg.screenshot(type='jpeg', quality=93))
        ff.stdin.close(); ff.wait()
        print('Video:', out, n, 'Bilder')
    b.close()
