"""Acht selbst erzeugte Klangbetten (lizenzfrei, weil komplett synthetisiert). Je rund 16 Sekunden, Stereo."""
import numpy as np, wave, subprocess, os
from scipy.signal import lfilter, butter
W = '/tmp/claude-0/-home-claude/21fca7b1-37df-5f4f-b10c-f57c5f01c02b/scratchpad/ig-beispiele'
SR = 44100
os.makedirs(f'{W}/klang', exist_ok=True)
hz = lambda m: 440.0 * 2 ** ((m - 69) / 12)

def tt(d): return np.arange(int(d * SR)) / SR
def att(x, ms=4):
    n = min(len(x), int(SR * ms / 1000)); x = x.copy(); x[:n] *= np.linspace(0, 1, n); return x
def rel(x, ms=30):
    n = min(len(x), int(SR * ms / 1000)); x = x.copy(); x[-n:] *= np.linspace(1, 0, n); return x

# --- Instrumente ---------------------------------------------------------
def pluck(m, d=0.6, tau=0.18):          # weicher Sinus-Ton
    t = tt(d); f = hz(m)
    return rel(att((np.sin(2*np.pi*f*t) + 0.2*np.sin(2*np.pi*2*f*t)) * np.exp(-t / tau), 6))
def piano(m, d=2.6):                    # Klavier-aehnlich: Obertoene mit eigenem Ausklang
    t = tt(d); f = hz(m); s = np.zeros_like(t)
    for k in range(1, 8):
        fk = f * k * np.sqrt(1 + 0.0004 * k * k)
        s += np.sin(2*np.pi*fk*t) / k**1.7 * np.exp(-t / (1.6 / k**0.75))
    return rel(att(s, 3), 80)
def epiano(m, d=2.4, idx=1.6):          # E-Piano per FM
    t = tt(d); f = hz(m)
    return rel(att(np.sin(2*np.pi*f*t + idx*np.exp(-t/0.35)*np.sin(2*np.pi*f*t)) * np.exp(-t / 1.1), 5), 80)
def bell(m, d=4.0):                     # Glocke per FM
    t = tt(d); f = hz(m)
    return rel(att(np.sin(2*np.pi*f*t + 2.2*np.exp(-t/0.9)*np.sin(2*np.pi*f*3.5*t)) * np.exp(-t / 1.3), 2), 100)
def marimba(m, d=0.9):
    t = tt(d); f = hz(m)
    return rel(att(np.sin(2*np.pi*f*t)*np.exp(-t/0.22) + 0.35*np.sin(2*np.pi*4*f*t)*np.exp(-t/0.05) + 0.1*np.sin(2*np.pi*10*f*t)*np.exp(-t/0.02), 2))
def guitar(m, d=2.2, seed=0):           # gezupfte Saite (Karplus-Strong)
    f = hz(m); N = int(round(SR / f)); n = int(d * SR)
    rng = np.random.default_rng(seed + m); x = np.zeros(n); burst = rng.uniform(-1, 1, N)
    b, a = butter(1, 2500 / (SR/2)); burst = lfilter(b, a, burst); x[:N] = burst
    den = np.zeros(N + 2); den[0] = 1; den[N] = -0.498; den[N + 1] = -0.498
    return rel(lfilter([1], den, x), 60)
def bass(m, d=0.5):
    t = tt(d); f = hz(m)
    return rel(att((np.sin(2*np.pi*f*t) + 0.3*np.sin(2*np.pi*2*f*t)) * np.exp(-t / 0.35), 8))
def kick(d=0.3):
    t = tt(d); f = 45 + 70*np.exp(-t/0.03)
    return rel(att(np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t / 0.11), 2))
def hat(d=0.06, seed=0):
    rng = np.random.default_rng(seed); x = rng.uniform(-1, 1, int(d*SR)); b, a = butter(2, 7000/(SR/2), 'high')
    return lfilter(b, a, x) * np.exp(-tt(d) / 0.02)
def rim(d=0.12, seed=1):
    rng = np.random.default_rng(seed); x = rng.uniform(-1, 1, int(d*SR)); b, a = butter(2, [900/(SR/2), 3500/(SR/2)], 'band')
    return lfilter(b, a, x) * np.exp(-tt(d) / 0.035)
def padchord(notes, d, seed=0):         # weiche Flaeche
    rng = np.random.default_rng(seed); t = tt(d); s = np.zeros((len(t), 2))
    env = np.sin(np.clip(t/1.2, 0, 1)*np.pi/2)**2 * np.sin(np.clip((d - t)/1.2, 0, 1)*np.pi/2)**2
    for m in notes:
        for det, pan in ((-0.14, 0.3), (0.16, 0.7)):
            f = hz(m) * (1 + det/100); ph = rng.uniform(0, 6.28)
            x = (np.sin(2*np.pi*f*t + ph) + 0.22*np.sin(4*np.pi*f*t + ph)) * env / (1 + (m - 48)/24)
            s[:, 0] += x*(1 - pan); s[:, 1] += x*pan
    return s

# --- Mischen -------------------------------------------------------------
def put(buf, x, t0, gain=1.0, pan=0.5):
    i = int(t0 * SR)
    if i >= len(buf): return
    if x.ndim == 1: x = np.stack([x*np.cos(pan*np.pi/2), x*np.sin(pan*np.pi/2)], 1)
    n = min(len(x), len(buf) - i); buf[i:i+n] += x[:n] * gain
def reverb(x, wet=0.25, size=1.0):
    out = np.zeros_like(x)
    for ch, off in ((0, 0), (1, 23)):
        acc = np.zeros(len(x))
        for D, g in ((1557, .80), (1617, .79), (1491, .81), (1422, .78), (1277, .80), (1356, .79)):
            D = int((D + off) * size); b = np.zeros(D + 1); b[D] = 1; a = np.zeros(D + 1); a[0] = 1; a[D] = -g
            acc += lfilter(b, a, x[:, ch])
        for D, g in ((225, .5), (556, .5)):
            b = np.zeros(D + 1); b[0] = -g; b[D] = 1; a = np.zeros(D + 1); a[0] = 1; a[D] = -g
            acc = lfilter(b, a, acc)
        bb, aa = butter(1, 4500/(SR/2)); out[:, ch] = lfilter(bb, aa, acc) / 6
    return x * (1 - wet*0.4) + out * wet
def finish(buf, d, name, lp=None):
    if lp: b, a = butter(2, lp/(SR/2)); buf = lfilter(b, a, buf, axis=0)
    buf = buf[:int(d*SR)]; t = tt(d)[:len(buf)]
    buf = buf * (np.clip(t/0.25, 0, 1) * np.clip((d - t)/1.6, 0, 1))[:, None]
    buf = buf / np.max(np.abs(buf)) * 0.7
    p = f'{W}/klang/{name}.wav'
    with wave.open(p, 'wb') as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes((np.clip(buf, -1, 1)*32767).astype('<i2').tobytes())
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-i', p, '-c:a', 'libmp3lame', '-b:a', '160k', f'{W}/klang/{name}.mp3'], check=True)
    rms = 20*np.log10(np.sqrt(np.mean(buf**2)) + 1e-9)
    print(f'{name}: {len(buf)/SR:.1f} s, RMS {rms:.1f} dB')
new = lambda d: np.zeros((int((d + 3) * SR), 2))

# Akkorde (MIDI): C-Dur-Welt, ruhig und offen
Cmaj7 = [48, 55, 60, 64, 71]; Am7 = [45, 52, 57, 60, 67]; Fmaj7 = [41, 53, 57, 60, 64]; G6 = [43, 50, 59, 62, 64]
Dm9 = [50, 57, 60, 65, 64]; G13 = [43, 53, 59, 64, 65]; Cmaj9 = [48, 55, 59, 62, 64]; Am9 = [45, 52, 55, 60, 59]

# 1 Flaeche: nur weiche Akkorde
d = 16.0; b = new(d)
for k, ch in enumerate([Fmaj7, Am7, Cmaj7, G6]): put(b, padchord(ch, 5.2, k), k*4.0 - 0.4 if k else 0, 1.0)
finish(reverb(b, .3), d, '1-flaeche')

# 2 Klavier: ruhige gebrochene Akkorde, 60 Schlaege pro Minute
d = 16.0; b = new(d); beat = 1.0
for k, ch in enumerate([Cmaj7, Am7, Fmaj7, G6]):
    t0 = k*4*beat; put(b, piano(ch[0]-12, 3.6), t0, .55, .45)
    for j, idx in enumerate([1, 2, 3, 4, 3, 2, 3, 4]): put(b, piano(ch[idx]+12, 2.4), t0 + j*beat/2, .30 + .06*(j % 4 == 0), .5 + .12*np.sin(j))
    put(b, padchord(ch[:4], 4.6, k), t0, .10)
finish(reverb(b, .32), d, '2-klavier')

# 3 Puls: gleichmaessige weiche Achtel, 96 Schlaege pro Minute
bpm = 96; beat = 60/bpm; d = 6*4*beat; b = new(d)
for k, ch in enumerate([Am7, Fmaj7, Cmaj7, G6, Am7, Fmaj7]):
    t0 = k*4*beat; put(b, bass(ch[0]-12, 1.6), t0, .7); put(b, padchord(ch[1:4], 4*beat + .6, k), t0, .16)
    for j in range(8): put(b, pluck(ch[[2, 3, 4, 3][j % 4]] + 12, .5, .14), t0 + j*beat/2, .34 if j % 2 == 0 else .22, .35 + .3*(j % 2))
finish(reverb(b, .26), d, '3-puls')

# 4 Marimba: leicht und freundlich, 104 Schlaege pro Minute
bpm = 104; beat = 60/bpm; d = 7*4*beat; b = new(d)
pat = [(0, 2), (.75, 3), (1.5, 4), (2, 3), (2.5, 2), (3.25, 3), (3.5, 4)]
for k, ch in enumerate([Cmaj7, Fmaj7, Am7, G6, Cmaj7, Fmaj7, G6]):
    t0 = k*4*beat; put(b, bass(ch[0]-12, 1.2), t0, .5); put(b, bass(ch[0]-12, .8), t0 + 2.5*beat, .35)
    for j, (bt, idx) in enumerate(pat): put(b, marimba(ch[idx] + 12), t0 + bt*beat, .5 if bt == 0 else .36, .3 + .4*((j*37) % 10)/10)
finish(reverb(b, .22), d, '4-marimba')

# 5 Lo-fi: E-Piano, weicher Beat, 80 Schlaege pro Minute
bpm = 80; beat = 60/bpm; d = 5*4*beat + 1; b = new(d); sw = beat*0.16
for k, ch in enumerate([Dm9, G13, Cmaj9, Am9, Dm9]):
    t0 = k*4*beat
    for m in ch: put(b, epiano(m + 12, 2.6), t0 + 0.012*(m % 5), .16, .4 + .2*((m % 7)/7)); put(b, epiano(m + 12, 1.6), t0 + 2.5*beat, .10, .5)
    put(b, bass(ch[0]-12, 1.4), t0, .55); put(b, bass(ch[0]-12, .7), t0 + 2.5*beat, .35)
    for q in range(4):
        if q in (0, 2): put(b, kick(), t0 + q*beat, .5)
        else: put(b, rim(seed=q+k), t0 + q*beat, .30, .55)
        put(b, hat(seed=k*8+q), t0 + q*beat, .10, .7); put(b, hat(seed=k*8+q+4), t0 + q*beat + beat/2 + sw, .07, .7)
rng = np.random.default_rng(5); b += rng.uniform(-1, 1, b.shape) * 0.004
finish(reverb(b, .18), d, '5-lofi', lp=5200)

# 6 Gitarre: gezupft, 88 Schlaege pro Minute
bpm = 88; beat = 60/bpm; d = 6*4*beat; b = new(d)
Gb = [47, 50, 55, 59, 62]
for k, ch in enumerate([Cmaj7, Gb, Am7, Fmaj7, Cmaj7, G6]):
    t0 = k*4*beat
    for j, idx in enumerate([0, 2, 1, 3, 0, 4, 2, 3]):
        m = ch[idx] + (0 if idx == 0 else 12)
        put(b, guitar(m, 2.4, j), t0 + j*beat/2, .5 if idx == 0 else .34, .4 + .2*(idx % 2))
finish(reverb(b, .2), d, '6-gitarre', lp=7000)

# 7 Glocken: einzelne Toene mit viel Raum
d = 16.0; b = new(d); rng = np.random.default_rng(11); penta = [72, 74, 76, 79, 81, 84]
for k, ch in enumerate([Cmaj7, Am7, Fmaj7, Cmaj7]): put(b, padchord(ch[:4], 5.0, k), max(0, k*4.0 - .4), .30)
t0 = 0.3
while t0 < d - 2.5:
    put(b, bell(int(rng.choice(penta))), t0, .26, float(rng.uniform(.25, .75))); t0 += float(rng.choice([1.0, 1.5, 2.0]))
finish(reverb(b, .42, 1.25), d, '7-glocken')

# 8 Schritt: leichter Antrieb, 100 Schlaege pro Minute
bpm = 100; beat = 60/bpm; d = 6*4*beat + 1; b = new(d)
for k, ch in enumerate([Am7, Fmaj7, Cmaj7, G6, Am7, Fmaj7]):
    t0 = k*4*beat; put(b, padchord(ch[1:4], 4*beat + .5, k), t0, .12)
    for q in range(4):
        put(b, kick(), t0 + q*beat, .42); put(b, hat(seed=k*4+q), t0 + q*beat + beat/2, .09, .65)
        put(b, bass(ch[0]-12, .28), t0 + q*beat, .45); put(b, bass(ch[0]-12, .22), t0 + q*beat + beat/2, .28)
        for m in ch[2:5]: put(b, pluck(m + 12, .22, .07), t0 + q*beat + beat/2, .13, .3 + .4*((m % 5)/5))
finish(reverb(b, .2), d, '8-schritt')
