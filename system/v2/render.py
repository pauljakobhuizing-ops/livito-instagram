"""Rendert Beitraege aus posts.js (Layout v2).
Aufruf: render.py [id ...] [--nur-karussell] [--nur-reel] [--stills]
Karussells -> ../../media/v2/<id>-<n>.png
Reels      -> ../../media/v2/<id>.mp4 und <id>-cover.jpg; --stills legt nur Standbilder je Abschnitt in v2/frames/ ab.
Am Ende: ../../media/v2/index.json mit Dauer und Titelbild-Zeitpunkt je Reel."""
import os, sys, json, subprocess, tempfile
from playwright.sync_api import sync_playwright
W = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.normpath(os.path.join(W, '..', '..', 'media', 'v2'))
KLANG = os.path.normpath(os.path.join(W, '..', 'klang'))
os.makedirs(OUT, exist_ok=True)
args = [a for a in sys.argv[1:] if not a.startswith('--')]
flags = [a for a in sys.argv[1:] if a.startswith('--')]
FPS = 30
idx_path = os.path.join(OUT, 'index.json')
idx = json.load(open(idx_path)) if os.path.exists(idx_path) else {}
with sync_playwright() as p:
    b = p.chromium.launch()
    if '--nur-reel' not in flags:
        pg = b.new_page(viewport={'width': 1080, 'height': 1350}, device_scale_factor=1)
        pg.goto('file://' + W + '/karussell.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        ids = pg.eval_on_selector_all('.slide', 'els => els.map(e => e.id)')
        if args: ids = [i for i in ids if i.rsplit('-', 1)[0] in args]
        over = []
        for i in ids:
            pg.locator('#' + i).screenshot(path=f'{OUT}/{i}.png')
            sh, ch = pg.evaluate(f"(()=>{{const e=document.getElementById('{i}');return [e.scrollHeight,e.clientHeight]}})()")
            if sh > ch: over.append(i)
        print('Folien:', len(ids), 'Ueberlauf:', over)
        pg.close()
    if '--nur-karussell' not in flags:
        pg = b.new_page(viewport={'width': 1080, 'height': 1920}, device_scale_factor=1)
        pg.goto('file://' + W + '/reel.html'); pg.evaluate('document.fonts.ready'); pg.wait_for_timeout(400)
        rids = pg.evaluate("POSTS.filter(p => p.typ === 'reel').map(p => p.id)")
        if args: rids = [i for i in rids if i in args]
        for rid in rids:
            r = pg.evaluate('id => setPost(id)', rid); dur, cover = r['dur'], r['cover']
            fmt = pg.evaluate('id => POSTS.find(p => p.id === id).format', rid)
            loop = pg.evaluate('id => !!POSTS.find(p => p.id === id).loop', rid)
            klang = pg.evaluate('f => F[f].klang', fmt)
            if '--stills' in flags:
                os.makedirs(W + '/frames', exist_ok=True)
                ts = pg.evaluate('SEGS.map(s => Math.max(s.a + .5, (s.a + s.b) / 2))')
                for k, t in enumerate(ts):
                    pg.evaluate(f'setTime({t})'); pg.screenshot(path=f'{W}/frames/{rid}-{k}.png')
                continue
            tmp = tempfile.mkdtemp()
            subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-stream_loop', '-1', '-i', f'{KLANG}/{klang}', '-t', str(dur),
                            '-af', ('afade=t=in:st=0:d=0.04,afade=t=out:st=%s:d=0.04' % (dur - 0.04)) if loop else f'afade=t=in:st=0:d=0.3,afade=t=out:st={dur - 1.2}:d=1.2', f'{tmp}/bett.wav'], check=True)
            out = f'{OUT}/{rid}.mp4'
            ff = subprocess.Popen(['ffmpeg', '-y', '-loglevel', 'error', '-f', 'image2pipe', '-framerate', str(FPS), '-c:v', 'mjpeg', '-i', '-',
                                   '-i', f'{tmp}/bett.wav', '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '21', '-preset', 'veryfast', '-r', str(FPS),
                                   '-c:a', 'aac', '-b:a', '128k', '-shortest', '-movflags', '+faststart', out], stdin=subprocess.PIPE)
            for k in range(int(round(dur * FPS))):
                pg.evaluate(f'setTime({k / FPS})')
                ff.stdin.write(pg.screenshot(type='jpeg', quality=92))
            ff.stdin.close(); ff.wait()
            pg.evaluate(f'setTime({cover})'); pg.screenshot(path=f'{OUT}/{rid}-cover.jpg', type='jpeg', quality=88)
            idx[rid] = {'dur': dur, 'cover_ms': int(cover * 1000)}
            print('Reel', rid, dur, 's')
    b.close()
json.dump(idx, open(idx_path, 'w'), indent=1, ensure_ascii=False)
