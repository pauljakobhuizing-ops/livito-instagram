// Layout v2 (ab 04.11.2026): eigener Grund je Format, gleiches Geruest auf allen Folien,
// letzte Folie immer Petrol mit Signet. Karussell 1080 x 1350, Reel 1080 x 1920.
const P = ['M47.91 2.05A48 48 0 0 0 2.05 47.91A60.48 60.48 0 0 0 47.91 2.05Z','M97.95 47.91A48 48 0 0 0 52.09 2.05A60.48 60.48 0 0 0 97.95 47.91Z','M52.09 97.95A48 48 0 0 0 97.95 52.09A60.48 60.48 0 0 0 52.09 97.95Z','M2.05 52.09A48 48 0 0 0 47.91 97.95A60.48 60.48 0 0 0 2.05 52.09Z'];
const signet = (fill, two) => `<svg viewBox="0 0 100 100" aria-hidden="true">${P.map((d,i)=>`<path fill="${fill}"${two&&(i==1||i==3)?' fill-opacity=".38"':''} d="${d}"/>`).join('')}</svg>`;

const HELL = { fg:'#201E1A', sub:'#4A473F', lab:'#8A8578', acc:'#1D4442', line:'rgba(32,30,26,.15)', boxbg:'#1D4442', boxfg:'#FFFFFF' };
const DUNKEL = { fg:'#FFFFFF', sub:'#D6DED8', lab:'#D6DED8', acc:'#FFFFFF', line:'rgba(214,222,216,.35)', boxbg:'#FFFFFF', boxfg:'#1D4442' };
const F = {
  rechnung: Object.assign({ label:'Die Rechnung', bg:'#F7F5F1', klang:'3-puls.wav' }, HELL),
  kurz:     Object.assign({ label:'Aus dem Magazin', bg:'#F7F5F1', klang:'3-puls.wav' }, HELL),
  wort:     Object.assign({ label:'Geldwörter', bg:'#FFFFFF', klang:'2-klavier.wav' }, HELL),
  stimmt:   Object.assign({ label:'Stimmt das?', bg:'#FFFFFF', klang:'3-puls.wav' }, HELL),
  buch:     Object.assign({ label:'Gelassen mit Geld', bg:'#FFFFFF', klang:'3-puls.wav' }, HELL),
  ticken:   Object.assign({ label:'Warum wir so ticken', bg:'#201E1A', klang:'3-puls.wav' }, DUNKEL),
  lieber:   Object.assign({ label:'Lieber … oder …?', bg:'#1D4442', klang:'1-flaeche.wav' }, DUNKEL),
  frage:    Object.assign({ label:'Eine Frage zum Geld', bg:'#1D4442', klang:'1-flaeche.wav' }, DUNKEL),
};
const ENDE = Object.assign({ bg:'#1D4442' }, DUNKEL);

// Typografie: geschuetzte Leerzeichen zwischen Zahl und Einheit, ~ als festes Leerzeichen, kein Einzelwort am Zeilenende.
const fix = s => String(s||'').replace(/~/g,' ')
  .replace(/(\d) (Euro|€|%|Prozent|Jahren|Jahre|Jahr|Tage|Tagen|Monate|Monaten|Cent)/g,'$1 $2')
  .replace(/ ([^ <>]{1,14})$/, (m, w, off, str) => { const prev = str.slice(0, off).split(/[  ]/).pop(); return prev.length + w.length <= 12 ? ' ' + w : m; });
const groesse = (t, stufen) => { const n = String(t).length; for (const [max, px] of stufen) if (n <= max) return px; return stufen[stufen.length-1][1]; };

// ---------- Karussell ----------
const KHOOK = [[22,140],[40,122],[60,106],[85,94],[999,84]];
const kopfK = (f, i, n) => `<div class="kopf" style="color:${f.lab}"><span>${f.label}</span><span class="nr">${i}/${n}</span></div>`;
const fussK = (f, hint) => `<div class="fuss" style="color:${f.lab}"><span>@dielivitomethode</span>${hint?`<span class="hint" style="color:${f.acc}">${hint}</span>`:''}</div>`;
const quelle = (f, q) => q ? `<p class="quelle" style="color:${f.lab}">${fix(q)}</p>` : '';
const absatz = (f, b, cls='body') => (b||[]).map(t=>`<p class="${cls}" style="color:${f.sub}">${fix(t)}</p>`).join('');
const zeilen = (f, rows) => rows ? `<div class="rows">${rows.map(r=>`<div class="row" style="border-color:${f.line};${r[2]?`background:${f.boxbg};color:${f.boxfg};`:`color:${f.fg};`}"><span class="l">${fix(r[0])}</span><span class="r">${fix(r[1])}</span></div>`).join('')}</div>` : '';

const SLIDE = {
  hook: (f, s) => `<div class="mitte"><h1 class="hook" style="color:${s.farbe==='fg'?f.fg:f.acc};font-size:${groesse(s.l1+(s.l2||''), KHOOK)}px">${fix(s.l1)}</h1>${s.l2?`<p class="hook2" style="color:${f.sub};font-size:${Math.round(groesse(s.l1+(s.l2||''), KHOOK)*.72)}px">${fix(s.l2)}</p>`:''}</div>`,
  wort: (f, s) => `<div class="mitte"><h1 class="wort" style="color:${f.acc}">${s.w}</h1><p class="hook2" style="color:${f.fg};font-size:84px">${fix(s.hook)}</p></div>`,
  wahl: (f, s) => `<div class="mitte"><div class="wahl"><div class="opt" style="color:${f.fg}"><span class="ab" style="border-color:${f.sub};color:${f.sub}">A</span><span>${fix(s.a)}</span></div><p class="oder" style="color:${f.sub}">oder</p><div class="opt" style="color:${f.fg}"><span class="ab" style="border-color:${f.sub};color:${f.sub}">B</span><span>${fix(s.b)}</span></div></div></div>`,
  text: (f, s) => `<div class="mitte">${s.h?`<h2 class="h" style="color:${f.fg}">${fix(s.h)}</h2>`:''}${absatz(f, s.b)}${zeilen(f, s.rows)}${absatz(f, s.b2)}${quelle(f, s.q)}</div>`,
  zwei: (f, s) => `<div class="mitte"><p class="zwei" style="color:${f.sub}">${fix(s.a)}</p><p class="zwei" style="color:${f.acc};margin-top:44px">${fix(s.b)}</p>${quelle(f, s.q)}</div>`,
  zahl: (f, s) => `<div class="mitte"><p class="vor" style="color:${f.sub}">${fix(s.vor)}</p><p class="zahl" style="color:${s.akzent?f.acc:f.fg}">${fix(s.zahl)}</p>${s.nach?`<p class="vor" style="color:${f.sub};margin-top:36px">${fix(s.nach)}</p>`:''}${quelle(f, s.q)}</div>`,
  balken: (f, s) => `<div class="mitte"><h2 class="h" style="color:${f.fg}">${fix(s.h)}</h2><div class="balken"><div style="width:${s.l.p}%;background:${f.fg}"></div><div style="width:${100-s.l.p}%;background:${f.acc}"></div></div><div class="bl"><div><p class="lab" style="color:${f.lab}">${s.l.label}</p><p class="bw" style="color:${f.fg}">${fix(s.l.wert)}</p></div><div style="text-align:right"><p class="lab" style="color:${f.lab}">${s.r.label}</p><p class="bw" style="color:${f.acc}">${fix(s.r.wert)}</p></div></div>${quelle(f, s.q)}</div>`,
  boxen: (f, s) => `<div class="mitte"><h2 class="h" style="color:${f.fg}">${fix(s.h)}</h2><div class="boxen">${s.boxes.map(x=>`<div class="box" style="${x.hl?`background:${f.boxbg};color:${f.boxfg}`:`border:3px solid ${f.line};color:${f.sub}`}"><p class="lab">${x.label}</p><p class="bw">${fix(x.wert)}</p></div>`).join('')}</div>${absatz(f, s.b2)}</div>`,
  ende: (f, s) => `<div class="mitte"><div class="sig">${signet('#FFFFFF')}</div><p class="endh">${fix(s.h)}</p>${s.sub?`<p class="ends">${fix(s.sub)}</p>`:''}</div>${s.note?`<p class="note">${fix(s.note)}</p>`:''}`,
};

function karussell(post) {
  const f = F[post.format]; const n = post.slides.length;
  return post.slides.map((s, i) => {
    const istEnde = s.t === 'ende'; const ff = istEnde ? Object.assign({}, f, ENDE, { label: f.label }) : f;
    const hint = i === 0 ? (post.hint || 'Weiter →') : '';
    return { id: `${post.id}-${i+1}`, bg: ff.bg, html: kopfK(ff, i+1, n) + SLIDE[s.t](ff, s) + fussK(ff, hint) };
  });
}

// Alternativtexte aus den Folien
const plain = s => String(s||'').replace(/~/g,' ').replace(/<[^>]+>/g,'');
function altText(s) {
  switch (s.t) {
    case 'hook': return [s.l1, s.l2].filter(Boolean).map(plain).join(' ');
    case 'wort': return `${s.w} ${plain(s.hook)}`;
    case 'wahl': return `A: ${plain(s.a)} oder B: ${plain(s.b)}`;
    case 'zwei': return `${plain(s.a)} ${plain(s.b)}${s.q?' '+plain(s.q):''}`;
    case 'zahl': return `${plain(s.vor)} ${plain(s.zahl)}${s.nach?' '+plain(s.nach):''}`;
    case 'balken': return `${plain(s.h)} ${s.l.label}: ${plain(s.l.wert)}. ${s.r.label}: ${plain(s.r.wert)}.`;
    case 'boxen': return `${plain(s.h)} ${s.boxes.map(b=>b.label+': '+plain(b.wert)).join('. ')}.`;
    case 'ende': return [s.h, s.sub, s.note].filter(Boolean).map(plain).join(' ');
    default: return [s.h, ...(s.b||[]), ...(s.rows||[]).map(r=>plain(r[0])+(r[1]?': '+plain(r[1]):'')), ...(s.b2||[]), s.q].filter(Boolean).map(plain).join(' ');
  }
}
