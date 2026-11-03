// Redaktionsplan November 2026, Layout v2. Ein Eintrag je Beitrag.
// Felder: id, datum, zeit, typ (karussell|reel), format (siehe F in common.js), hook (Art des Einstiegs),
// thema, magazin (Slug oder ''), buch (true bei Beitraegen, die auf die Methode verweisen), text (Bildunterschrift),
// slides (Karussell) bzw. segs (Reel, d = Dauer in Sekunden).
const MAG = {
  'zinseszins-erklaert': 'Zinseszins einfach erklärt: Formel, Beispiel und Excel',
  'zuhause': 'Ein eigenes Zuhause: was du dir wirklich leisten kannst',
  'buy-now-pay-later-neue-regeln': 'Buy now, pay later: Was ab 20. November neu gilt',
  'erst-schulden-oder-sparen': 'Erst Schulden tilgen oder erst sparen?',
  'grundlagen': 'Finanzielle Gelassenheit: warum Struktur wichtiger ist als Einkommen',
  'altersvorsorgedepot-vergleich': 'Altersvorsorgedepot im Vergleich: Stand vor dem Start',
  'notgroschen': 'Der Notgroschen: 1.500 Euro, die alles leichter machen',
};
const magZeile = slug => `Mehr dazu im Magazin: „${MAG[slug]}“. Link in der Bio.`;
const TEILEN = 'Schreib’s gern in die Kommentare. Oder schick die Frage jemandem, mit dem du darüber reden magst.';
const frageReel = (id, datum, q, text) => ({ id, datum, zeit:'20:30', typ:'reel', format:'frage', hook:'Frage', thema:'Frage', magazin:'', buch:false,
  text: text + '\n\n' + TEILEN, coverS: 1.0, loop: true,
  segs: [ { t:'frage', q, d: q.length > 45 ? 6 : 5 } ] });

const POSTS = [
// ---------------- Mittwoch, 4. November ----------------
{ id:'rechnung01', datum:'2026-11-04', zeit:'07:30', typ:'karussell', format:'rechnung', hook:'Zahl', thema:'Zinseszins', magazin:'zinseszins-erklaert', buch:false, hint:'Nachrechnen →',
  text:'50 € im Monat klingen nach eher wenig. 🌿\n\nÜber 30 Jahre werden daraus rund 41.600 €. Mehr als die Hälfte davon hast du nicht selbst eingezahlt.\n\n' + magZeile('zinseszins-erklaert') + '\n\nSpeicher dir den Beitrag für den Tag, an dem du denkst, es lohnt sich nicht.',
  slides:[
   { t:'hook', l1:'50 € im Monat.', l2:'Klingt nach eher wenig.' },
   { t:'zahl', vor:'30 Jahre lang zahlst du ein:', zahl:'18.000 €' },
   { t:'zahl', vor:'Mit 5 % pro Jahr werden daraus rund:', zahl:'41.600 €', akzent:true },
   { t:'balken', h:'Mehr als die Hälfte hast du nicht selbst eingezahlt.', l:{label:'Eingezahlt', wert:'18.000 €', p:43}, r:{label:'Zinsertrag', wert:'rund 23.600 €'} },
   { t:'zwei', a:'Nicht der Betrag macht den größten Unterschied.', b:'Die Zeit macht ihn.' },
   { t:'ende', h:'Speicher dir die Rechnung für den Tag, an dem 50 € nach wenig klingen.', note:'Modellrechnung: 50 € monatlich, 30 Jahre, 5 % Rendite pro Jahr, monatlich verzinst. Keine Prognose.' },
  ]},
{ id:'stimmt01', datum:'2026-11-04', zeit:'11:30', typ:'reel', format:'stimmt', hook:'Behauptung', thema:'Wohnen', magazin:'zuhause', buch:false,
  text:'„Mieten ist rausgeworfenes Geld.“ Stimmt das? 🌿\n\nNicht ganz. Auch beim Kauf ist ein Teil des Geldes weg: Zinsen, Kaufnebenkosten, Instandhaltung. Beides kann richtig sein.\n\n' + magZeile('zuhause') + '\n\nMietest du, oder hast du gekauft?',
  segs:[
   { t:'zitat', q:'Mieten ist rausgeworfenes Geld.', d:3 },
   { t:'zitat', q:'Mieten ist rausgeworfenes Geld.', dim:true, plus:'Nicht ganz.', d:2 },
   { t:'text', b:['Beim Kauf baut ein Teil der Rate Vermögen auf.'], d:3 },
   { t:'text', h:'Der Rest ist auch weg:', rows:['Zinsen','Kaufnebenkosten','Instandhaltung'], d:3.5 },
   { t:'text', b:['Beides kann richtig sein.','Rausgeworfen ist nur Geld, über das du nicht entschieden hast.'], akzent:1, d:3.8 },
  ]},
{ id:'ticken10', datum:'2026-11-04', zeit:'16:30', typ:'karussell', format:'ticken', hook:'Frage', thema:'Mental Accounting', magazin:'', buch:false,
  text:'Warum fühlt sich eine Steuererstattung an wie geschenkt? 🌿\n\nEs ist dein eigenes Geld. Trotzdem landet es im Kopf auf einem Extrakonto und ist schneller ausgegeben. Der Ökonom Richard Thaler nennt das Mental Accounting.\n\nWas machst du mit deiner Erstattung?',
  slides:[
   { t:'hook', l1:'Warum fühlt sich eine Steuererstattung an wie geschenkt?', farbe:'fg' },
   { t:'zwei', a:'Dabei ist es dein Geld.', b:'Du hast im Laufe des Jahres nur zu viel davon abgegeben.' },
   { t:'boxen', h:'Im Kopf landet es trotzdem auf einem anderen Konto.', boxes:[{label:'Konto', wert:'Gehalt'}, {label:'Konto', wert:'Bonus', hl:true}] },
   { t:'text', h:'Der Ökonom Richard Thaler nennt das Mental Accounting.', b:['Wir sortieren Geld nach Herkunft, nicht nach Wert.'] },
   { t:'text', h:'Geld vom Konto „Bonus“ geben wir leichter aus.', q:'Thaler, Journal of Behavioral Decision Making, 1999. Arkes u. a., Organizational Behavior and Human Decision Processes, 1994.' },
   { t:'zwei', a:'Gelassen wird es, wenn jeder Euro vorher eine Aufgabe hat.', b:'Auch der aus der Erstattung.' },
   { t:'ende', h:'Kennst du jemanden, dessen Erstattung schon verplant ist?' },
  ]},
frageReel('r-frage05', '2026-11-04', 'Welcher Kauf hat sich wirklich gelohnt?', 'Welcher Kauf hat sich wirklich gelohnt? 🌿\n\nManche Dinge benutzt man zehn Jahre lang fast täglich. Andere liegen nach einer Woche im Schrank.\n\nWas gehört bei dir zur ersten Sorte?'),

// ---------------- Donnerstag, 5. November ----------------
{ id:'wort02', datum:'2026-11-05', zeit:'07:30', typ:'karussell', format:'wort', hook:'Wortspiel', thema:'Kredit', magazin:'', buch:false,
  text:'Kredit heißt eigentlich: Ich glaube dir. 🌿\n\nDas Wort kommt vom lateinischen credere. Wer Geld verleiht, vertraut darauf, dass es zurückkommt.\n\nWelches Geldwort sollen wir als Nächstes auseinandernehmen?',
  slides:[
   { t:'wort', w:'Kredit', hook:'heißt eigentlich: Ich glaube dir.' },
   { t:'text', h:'Das steckt im Wort', b:['Kredit kommt vom lateinischen~Wort~credere.', 'Das heißt: glauben.'] },
   { t:'text', h:'Darum heißt es Gläubiger', b:['Wer Geld verleiht, glaubt daran, dass es zurückkommt.', 'Ein Kredit ist also vor allem eins: Vertrauen.'], q:'Quellen: Wahrig Herkunftswörterbuch; Online Etymology Dictionary' },
   { t:'ende', h:'Welches Geldwort sollen wir als Nächstes auseinandernehmen?' },
  ]},
{ id:'r-lieber04', datum:'2026-11-05', zeit:'11:30', typ:'reel', format:'lieber', hook:'Wahl', thema:'Bezahlen', magazin:'', buch:false,
  text:'Bar oder Karte? 🌿\n\nDie Frage teilt Freundeskreise.\n\nA oder B? Schreib es in die Kommentare.',
  loop:true, segs:[ { t:'wahl', a:'Bar bezahlen', b:'Mit Karte bezahlen', d:5.5 } ]},
{ id:'ticken05', datum:'2026-11-05', zeit:'16:30', typ:'karussell', format:'ticken', hook:'Behauptung', thema:'Bezahlen', magazin:'', buch:false,
  text:'Mit Karte zahlen wir mehr. Viel mehr. 🌿\n\nIn einem Experiment boten Menschen mit Kreditkarte mehr als doppelt so viel wie mit Bargeld.\n\nZahlst du lieber bar oder mit Karte?',
  slides:[
   { t:'hook', l1:'Mit Karte zahlen wir mehr. Viel mehr.', farbe:'fg' },
   { t:'text', h:'Das Experiment', b:['Studierende boten auf Tickets für ein ausverkauftes Basketballspiel.', 'Die eine Hälfte sollte bar zahlen, die andere mit Kreditkarte.'] },
   { t:'text', h:'Das Ergebnis', b:['Mit Kreditkarte boten sie im Schnitt mehr als doppelt so viel.', 'Für genau dieselben Tickets.'], q:'Prelec und Simester, Marketing Letters, 2001.' },
   { t:'text', h:'Der Grund', b:['Bargeld sehen wir gehen.', 'Bei der Karte spüren wir das Bezahlen kaum.'] },
   { t:'ende', h:'Bequem ist nicht immer günstig.', sub:'Wer das weiß, schaut einmal mehr auf den Betrag.' },
  ]},
frageReel('r-frage06', '2026-11-05', 'Mit wem sprichst du offen über Geld?', 'Mit wem sprichst du offen über Geld? 🌿\n\nÜber fast alles reden wir leichter als über den eigenen Kontostand.\n\nWer ist bei dir die Ausnahme?'),

// ---------------- Freitag, 6. November ----------------
{ id:'kurz01', datum:'2026-11-06', zeit:'07:30', typ:'karussell', format:'kurz', hook:'Neuigkeit', thema:'Buy now, pay later', magazin:'buy-now-pay-later-neue-regeln', buch:false,
  text:'„Später bezahlen“ gilt ab dem 20. November als Kredit. 🌿\n\nAnbieter wie Klarna oder PayPal müssen dann vorher prüfen, ob du zurückzahlen kannst. Dafür bekommst du ein Widerrufsrecht, auch bei kleinen Beträgen.\n\n' + magZeile('buy-now-pay-later-neue-regeln') + '\n\nNutzt du „Später bezahlen“?',
  slides:[
   { t:'hook', l1:'„Später bezahlen“ ist ab 20.~November ein Kredit.' },
   { t:'text', h:'Was sich ändert', b:['Anbieter wie Klarna oder PayPal müssen vorher prüfen, ob du zurückzahlen kannst.', 'Auch bei kleinen Beträgen.'] },
   { t:'text', h:'Neu für dich', rows:[['Widerruf innerhalb von 14~Tagen',''],['Kosten und Mahngebühren vorab',''],['Entgegenkommen bei Zahlungsproblemen','']] },
   { t:'text', h:'Was bleibt', b:['Der Kauf auf Rechnung direkt beim Shop ist meist nicht betroffen.', 'Solange er kostenlos ist und die Frist kurz bleibt.'] },
   { t:'zwei', a:'Eine Schuld war es auch vorher schon.', b:'Jetzt steht es im Gesetz.' },
   { t:'ende', h:'Kauf nur, was du heute bezahlen könntest.', note:'Quellen: Bundesregierung; Bundesministerium der Justiz und für Verbraucherschutz. Mehr im Magazin auf die-livito-methode.de' },
  ]},
{ id:'stimmt02', datum:'2026-11-06', zeit:'11:30', typ:'reel', format:'stimmt', hook:'Behauptung', thema:'Notgroschen', magazin:'erst-schulden-oder-sparen', buch:false,
  text:'„Solange ich Schulden habe, bringt Sparen nichts.“ Stimmt das? 🌿\n\nNicht ganz. Ohne kleine Rücklage landet der nächste Notfall wieder im Dispo. Darum kommt erst ein Notgroschen von 1.500 €, dann der Schuldenabbau.\n\n' + magZeile('erst-schulden-oder-sparen') + '\n\nWie machst du es?',
  segs:[
   { t:'zitat', q:'Solange ich Schulden habe, bringt Sparen nichts.', d:3.2 },
   { t:'zitat', q:'Solange ich Schulden habe, bringt Sparen nichts.', dim:true, plus:'Nicht ganz.', d:2 },
   { t:'text', b:['Ohne Rücklage landet die nächste kaputte Waschmaschine im Dispo.'], d:3.4 },
   { t:'text', b:['Darum zuerst 1.500 € Notgroschen.','Dann die Schulden.'], akzent:1, d:3 },
   { t:'text', b:['So wächst kein neuer Schuldenberg nach.'], d:2.6 },
  ]},
{ id:'lieber02', datum:'2026-11-06', zeit:'16:30', typ:'karussell', format:'lieber', hook:'Wahl', thema:'Arbeit', magazin:'', buch:false, hint:'Erst wählen, dann wischen →',
  text:'Mehr Gehalt oder mehr Freizeit? 🌿\n\nEs gibt keine falsche Antwort. Nur deine.\n\nA oder B? Schreib es in die Kommentare.',
  slides:[ { t:'wahl', a:'Mehr Gehalt', b:'Mehr Freizeit' }, { t:'ende', h:'Es gibt keine falsche Antwort. Nur deine.', sub:'A oder B?' } ]},
frageReel('r-frage07', '2026-11-06', 'Was würdest du deinem 20-jährigen Ich über Geld sagen?', 'Was würdest du deinem 20-jährigen Ich über Geld sagen? 🌿\n\nEin Satz genügt. Die besten Ratschläge sind meistens kurz.\n\nWie lautet deiner?'),

// ---------------- Samstag, 7. November ----------------
{ id:'rechnung02', datum:'2026-11-07', zeit:'07:30', typ:'karussell', format:'rechnung', hook:'Frage', thema:'72er-Regel', magazin:'zinseszins-erklaert', buch:false, hint:'Nachrechnen →',
  text:'Wann verdoppelt sich dein Geld? 🌿\n\nTeil 72 durch den Zinssatz. Bei 5 % pro Jahr sind es rund 14 Jahre. Die Regel funktioniert auch andersherum: Bei 2 % Inflation halbiert sich die Kaufkraft in rund 36 Jahren.\n\n' + magZeile('zinseszins-erklaert') + '\n\nKanntest du die Regel schon?',
  slides:[
   { t:'hook', l1:'Wann verdoppelt sich dein Geld?', l2:'Eine Zahl reicht: 72.' },
   { t:'text', h:'Die 72er-Regel', b:['Teil 72 durch den Zinssatz.', 'Das Ergebnis ist ungefähr die Zahl der Jahre, bis sich dein Geld verdoppelt.'] },
   { t:'text', h:'Zum Beispiel', rows:[['2 % pro Jahr','36 Jahre'],['5 % pro Jahr','rund 14 Jahre',1],['8 % pro Jahr','9 Jahre']] },
   { t:'zwei', a:'Die Regel funktioniert auch andersherum.', b:'Bei 2 % Inflation halbiert sich die Kaufkraft in rund 36~Jahren.' },
   { t:'ende', h:'Zinsen arbeiten leise. Aber sie arbeiten.', note:'Faustregel, gilt näherungsweise für Zinssätze zwischen etwa 2 und 10 % pro Jahr.' },
  ]},
{ id:'r-wort01', datum:'2026-11-07', zeit:'11:30', typ:'reel', format:'wort', hook:'Wortspiel', thema:'Bank', magazin:'', buch:false,
  text:'Deine Bank ist eigentlich ein Möbelstück. 🌿\n\nGeldwechsler in Italien saßen an einem Tisch, der banca. Und wer pleite war, dessen Tisch war kaputt: banca rotta.\n\nKanntest du das schon?',
  segs:[
   { t:'wort', w:'Bank', hook:'ist eigentlich ein Möbelstück.', d:3.5 },
   { t:'text', h:'Das steckt im Wort', b:['Geldwechsler in Italien saßen an einem Tisch.', 'Er hieß banca.'], akzent:1, d:4 },
   { t:'text', h:'Und wer pleiteging?', b:['Dessen Tisch war kaputt: banca~rotta.', 'Daraus wurde bankrott.'], akzent:1, q:'Quellen: Duden; Online Etymology Dictionary', d:4.6 },
  ]},
{ id:'ticken06', datum:'2026-11-07', zeit:'16:30', typ:'karussell', format:'ticken', hook:'Behauptung', thema:'Besitztumseffekt', magazin:'', buch:false,
  text:'Sobald dir etwas gehört, ist es dir mehr wert. 🌿\n\nDas zeigt ein Experiment mit Kaffeetassen. Und es erklärt, warum Aussortieren so schwerfällt.\n\nWas würdest du nie verkaufen?',
  slides:[
   { t:'hook', l1:'Sobald dir eine Tasse gehört, ist sie dir doppelt so viel wert.', farbe:'fg' },
   { t:'text', h:'Das Experiment', b:['Die Hälfte einer Gruppe bekam eine Kaffeetasse geschenkt.', 'Dann durften die Besitzer verkaufen und die anderen kaufen.'] },
   { t:'text', h:'Das Ergebnis', b:['Die Besitzer verlangten etwa doppelt so viel, wie die anderen zahlen wollten.', 'Es kam kaum ein Handel zustande.'], q:'Kahneman, Knetsch und Thaler, Journal of Political Economy, 1990.' },
   { t:'text', h:'Im Alltag', b:['Darum fällt Aussortieren so schwer.', 'Was uns gehört, schätzen wir höher ein.'] },
   { t:'ende', h:'Besitz macht wertvoll. Zumindest im Kopf.', sub:'Eine Frage hilft: Würde ich es heute zu diesem Preis kaufen?' },
  ]},
frageReel('r-frage08', '2026-11-07', 'Wann hast du dich zuletzt reich gefühlt?', 'Wann hast du dich zuletzt reich gefühlt? 🌿\n\nOft hat der Moment wenig mit dem Kontostand zu tun.\n\nWann war es bei dir?'),

// ---------------- Sonntag, 8. November ----------------
{ id:'wort03', datum:'2026-11-08', zeit:'07:30', typ:'karussell', format:'wort', hook:'Wortspiel', thema:'Groschen', magazin:'', buch:false,
  text:'Bei dir ist er bestimmt schon mal gefallen. 🌿\n\nDer Groschen fiel früher wirklich: in den Automaten. Erst dann gab es Kaugummi oder Briefmarken.\n\nWann ist bei dir zuletzt der Groschen gefallen?',
  slides:[
   { t:'wort', w:'Groschen', hook:'Bei dir ist er bestimmt schon mal gefallen.' },
   { t:'text', h:'Woher das kommt', b:['Das Zehnpfennigstück hieß früher Groschen.', 'Man warf es in Automaten.', 'Erst wenn die Münze unten ankam, gab der Automat etwas heraus.'] },
   { t:'text', h:'Darum sagen wir:', b:['„Der Groschen ist gefallen.“', 'Gemeint ist: Jetzt hat es Klick~gemacht.'], q:'Quellen: BRF; Austria-Forum' },
   { t:'ende', h:'Wann ist bei dir zuletzt der Groschen gefallen?' },
  ]},
{ id:'stimmt03', datum:'2026-11-08', zeit:'11:30', typ:'reel', format:'stimmt', hook:'Behauptung', thema:'Sparen anfangen', magazin:'grundlagen', buch:false,
  text:'„Ich verdiene zu wenig, um zu sparen.“ Stimmt das? 🌿\n\nNicht ganz. Am Anfang zählt nicht der Betrag, sondern dass es läuft. Und wenn gerade nichts übrig ist, ist es schon ein Schritt, genau das zu wissen.\n\n' + magZeile('grundlagen') + '\n\nWomit hast du angefangen?',
  segs:[
   { t:'zitat', q:'Ich verdiene zu wenig, um zu sparen.', d:3 },
   { t:'zitat', q:'Ich verdiene zu wenig, um zu sparen.', dim:true, plus:'Nicht ganz.', d:2 },
   { t:'text', b:['Am Anfang zählt nicht der Betrag.', 'Sondern, dass es läuft.'], akzent:1, d:3.4 },
   { t:'text', b:['20 € im Monat sind nach einem Jahr 240 €.', 'Ein Anfang.'], akzent:1, d:3 },
   { t:'text', b:['Und wenn gerade nichts übrig ist:', 'Dann ist der erste Schritt, genau das zu wissen.'], akzent:1, d:3.6 },
  ]},
{ id:'buch02', datum:'2026-11-08', zeit:'16:30', typ:'karussell', format:'buch', hook:'Frage', thema:'Methode: Reihenfolge', magazin:'notgroschen', buch:true,
  text:'Für ruhigen Schlaf braucht es weniger Geld, als die meisten denken. 🌿\n\nWas es braucht, ist eine Reihenfolge: erst der Notgroschen, dann die Schulden, dann der Puffer, dann die Altersvorsorge.\n\nGenau das ist die Livito-Methode: Rechner, Arbeitsblätter und ein E-Book für diese vier Schritte. Link in der Bio.',
  slides:[
   { t:'hook', l1:'Wie viel Geld brauchst du, um ruhig zu schlafen?' },
   { t:'text', h:'Für den Anfang: 1.500 Euro', b:['So viel braucht dein erster Notgroschen.', 'Nicht drei Monatsgehälter. Nicht 10.000 Euro.'] },
   { t:'text', h:'Was 1.500 Euro verändern', b:['Ohne Rücklage geht die kaputte Waschmaschine in den Dispo.', 'Mit Rücklage ist sie einfach bezahlt.'] },
   { t:'text', h:'Und dann?', rows:[['1.~Notgroschen',''],['2.~Raus aus den Schulden',''],['3.~Puffer von vier Monatsausgaben',''],['4.~Altersvorsorge','']] },
   { t:'ende', h:'Ruhig schlafen ist keine Frage des Kontostands. Sondern der Reihenfolge.', sub:'Die ganze Reihenfolge ist die Livito-Methode. Link in der Bio.' },
  ]},
frageReel('r-frage09', '2026-11-08', 'Welche Geldsorge war im Rückblick unnötig?', 'Welche Geldsorge war im Rückblick unnötig? 🌿\n\nManche Sorgen kosten mehr Schlaf, als die Sache am Ende wert war.\n\nWelche fällt dir ein?'),

// ---------------- Montag, 9. November ----------------
{ id:'kurz02', datum:'2026-11-09', zeit:'07:30', typ:'karussell', format:'kurz', hook:'Neuigkeit', thema:'Altersvorsorgedepot', magazin:'altersvorsorgedepot-vergleich', buch:false,
  text:'Am 1. Januar startet das Altersvorsorgedepot. Musst du dich jetzt entscheiden? 🌿\n\nNein. Abschließen kannst du erst ab Januar, zertifiziert ist noch kein Angebot. Ein erster Blick auf die Kosten lohnt sich trotzdem.\n\n' + magZeile('altersvorsorgedepot-vergleich') + '\n\nHast du dich schon vormerken lassen?',
  slides:[
   { t:'hook', l1:'Am 1.~Januar startet das Altersvorsorgedepot.', l2:'Musst du dich jetzt entscheiden?' },
   { t:'text', h:'Kurze Antwort: nein.', b:['Abschließen kannst du erst ab Januar.', 'Zertifiziert ist bisher noch kein Angebot.'] },
   { t:'text', h:'Was feststeht', rows:[['50 % Zulage','auf die ersten 360 € im Jahr'],['25 % Zulage','auf weitere Beiträge bis 1.800 €'],['bis zu 300 €','Zulage pro Kind']] },
   { t:'text', h:'Worauf du achten kannst', b:['Auf die Kosten nach der Aktionsphase, nicht im ersten Jahr.', 'Startprämien sind klein. Laufende Kosten wirken über Jahrzehnte.'] },
   { t:'ende', h:'Vergleich in Ruhe. Du hast Zeit.', note:'Stand Ende Oktober 2026. Quellen: Bundesministerium der Finanzen; finanzfacts; Handelsblatt.' },
  ]},
{ id:'r-lieber05', datum:'2026-11-09', zeit:'11:30', typ:'reel', format:'lieber', hook:'Wahl', thema:'Paare', magazin:'', buch:false,
  text:'Gemeinsames Konto oder getrennte Kassen? 🌿\n\nJedes Paar findet seinen eigenen Weg.\n\nWie macht ihr es? Schreib’s gern in die Kommentare.',
  loop:true, segs:[ { t:'wahl', a:'Ein gemeinsames Konto', b:'Getrennte Kassen', d:5.5 } ]},
{ id:'lieber03', datum:'2026-11-09', zeit:'16:30', typ:'karussell', format:'lieber', hook:'Wahl', thema:'Kontostand', magazin:'', buch:false, hint:'Erst wählen, dann wischen →',
  text:'Jeden Tag aufs Konto schauen oder nie? 🌿\n\nBeides hat seine Fans.\n\nA oder B? Und warum?',
  slides:[ { t:'wahl', a:'Jeden Tag aufs Konto schauen', b:'Nie aufs Konto schauen' }, { t:'ende', h:'Beides hat seine Fans.', sub:'A oder B? Und warum?' } ]},
frageReel('r-frage10', '2026-11-09', 'Was bedeutet Sicherheit für dich: eine Zahl oder ein Gefühl?', 'Was bedeutet Sicherheit für dich: eine Zahl oder ein Gefühl? 🌿\n\nFür die einen ist es ein Betrag auf dem Konto. Für die anderen die Gewissheit, dass es schon irgendwie geht.\n\nWozu gehörst du?'),
];
