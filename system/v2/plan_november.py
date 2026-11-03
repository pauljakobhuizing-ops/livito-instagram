"""Redaktionsplan 04.–30.11.2026: vier Schienen, eine Zeile je Beitrag. Schreibt plan_november.json.
Spalten: datum, zeit, schiene, typ, format, id, thema, hook, magazin, methode, quelle_inhalt (neu|Bestand)"""
import json, datetime as dt
FMT = {'rechnung':'Die Rechnung','kurz':'Aus dem Magazin','wort':'Geldwörter','stimmt':'Stimmt das?','buch':'Gelassen mit Geld',
       'ticken':'Warum wir so ticken','lieber':'Lieber … oder …?','frage':'Eine Frage zum Geld'}
SCHIENE = {'07:30':'Karussell früh','11:30':'Reel Mittag','16:30':'Karussell Nachmittag','20:30':'Reel Abend'}
# (id, thema, hook, magazin, methode, neu)
T = {
 'rechnung01':('50 € im Monat über 30 Jahre','Zahl','zinseszins-erklaert',0,1),
 'rechnung02':('Die 72er-Regel','Frage','zinseszins-erklaert',0,1),
 'rechnung03':('Was 1.000 € im Dispo im Jahr kosten','Zahl','dispo',0,1),
 'rechnung04':('Was 100 € in 20 Jahren noch wert sind (Inflation)','Zahl','',0,1),
 'rechnung05':('Ein Prozentpunkt Kosten über 30 Jahre','Zahl','altersvorsorgedepot-anbieter',0,1),
 'rechnung06':('Wie schnell 1.500 € Notgroschen stehen','Zahl','notgroschen-hoehe',1,1),
 'rechnung07':('Schneeballmethode in Zahlen','Zahl','schulden-reihenfolge',1,1),
 'rechnung08':('100 € im Monat ab Geburt bis 18','Zahl','kinder-sparen',0,1),
 'rechnung09':('Frühstart-Rente: 10 € vom Staat','Zahl','fruehstart-rente',0,1),
 'rechnung10':('Die 4-Prozent-Regel','Zahl','4-prozent-regel',0,1),
 'kurz01':('Buy now, pay later: neue Regeln ab 20.11.','Neuigkeit','buy-now-pay-later-neue-regeln',0,1),
 'kurz02':('Altersvorsorgedepot: Stand vor dem Start','Neuigkeit','altersvorsorgedepot-vergleich',0,1),
 'kurz03':('Der Notgroschen: 1.500 €','Zahl','notgroschen',1,1),
 'kurz04':('Der Puffer: vier Monatsausgaben','Zahl','puffer',1,1),
 'kurz05':('Schneeball oder Lawine?','Frage','schulden-reihenfolge',1,1),
 'kurz06':('Ab heute: „Später bezahlen“ ist ein Kredit','Neuigkeit','buy-now-pay-later-neue-regeln',0,1),
 'kurz07':('Wie viel für die Rente? 12 %','Frage','wie-viel-altersvorsorge',1,1),
 'kurz08':('Weihnachtsgeld: wohin damit?','Frage','weihnachtsgeld-wohin-damit',1,1),
 'kurz09':('Black Friday und „Später bezahlen“','Frage','buy-now-pay-later-neue-regeln',0,1),
 'kurz10':('Eigenkapital fürs Zuhause: 30/20/30','Zahl','eigenkapital-immobilie',1,1),
 'wort02':('Kredit','Wortspiel','',0,0),'wort03':('Groschen','Wortspiel','',0,0),'wort07':('Heller','Wortspiel','',0,0),
 'wort08':('Konto','Wortspiel','',0,0),'wort09':('Bilanz','Wortspiel','',0,0),'wort10':('Euro','Wortspiel','',0,0),
 'wort11':('Budget','Wortspiel','',0,1),'wort12':('Rabatt','Wortspiel','',0,1),'wort13':('Zins','Wortspiel','zinseszins',0,1),
 'stimmt01':('„Mieten ist rausgeworfenes Geld.“','Behauptung','zuhause',0,1),
 'stimmt02':('„Solange ich Schulden habe, bringt Sparen nichts.“','Behauptung','erst-schulden-oder-sparen',1,1),
 'stimmt03':('„Ich verdiene zu wenig, um zu sparen.“','Behauptung','grundlagen',0,1),
 'stimmt04':('„Zahl zuerst die Schuld mit dem höchsten Zins.“','Behauptung','schulden-reihenfolge',1,0),
 'stimmt05':('„Mit 40 ist es für die Rente zu spät.“','Behauptung','wie-viel-altersvorsorge',0,1),
 'stimmt06':('„Riester kündigen und ins Depot wechseln.“','Behauptung','riester-altersvorsorgedepot',0,1),
 'stimmt07':('„0-%-Finanzierung kostet nichts.“','Behauptung','buy-now-pay-later-neue-regeln',0,1),
 'stimmt08':('„Mit mehr Gehalt wären meine Geldsorgen weg.“','Behauptung','grundlagen',0,1),
 'stimmt09':('„Der Notgroschen gehört aufs Girokonto.“','Behauptung','notgroschen',1,1),
 'stimmt10':('„Fürs Kind sparen lohnt sich erst mit viel Geld.“','Behauptung','kinder',0,1),
 'stimmt11':('„Am Black Friday spare ich Geld.“','Behauptung','',0,1),
 'stimmt12':('„Betriebsrente lohnt sich nicht.“','Behauptung','lohnt-sich-bav',0,1),
 'ticken03':('Das zukünftige Ich als Fremder','Behauptung','',0,0),'ticken04':('Der Anker-Effekt (Glücksrad)','Behauptung','',0,0),
 'ticken05':('Mit Karte zahlen wir mehr','Behauptung','',0,0),'ticken06':('Der Besitztumseffekt (Tassen)','Behauptung','',0,0),
 'ticken07':('Voreinstellung bei der Betriebsrente','Behauptung','lohnt-sich-bav',0,0),'ticken08':('Versunkene Kosten (Skireisen)','Frage','',0,0),
 'ticken09':('Gegenwartsvorliebe (Äpfel)','Frage','',0,0),'ticken10':('Mental Accounting (Steuererstattung)','Frage','',0,1),
 'ticken11':('Warum Geldgeschenke sich falsch anfühlen','Frage','',0,1),'ticken12':('Großer Schein bleibt länger im Portemonnaie','Behauptung','',0,1),
 'ticken13':('Warum wir uns an mehr Geld gewöhnen','Behauptung','',0,1),'ticken14':('Macht mehr Geld glücklicher?','Frage','',0,1),
 'lieber02':('Mehr Gehalt oder mehr Freizeit','Wahl','',0,0),'lieber03':('Jeden Tag aufs Konto schauen oder nie','Wahl','',0,0),
 'lieber06':('Einmal teuer oder öfter günstig','Wahl','',0,0),'lieber07':('Erlebnisse oder Dinge','Wahl','',0,0),
 'lieber08':('Über Gehalt reden oder nicht','Wahl','',0,0),'lieber09':('Geschenk oder Geld','Wahl','',0,0),
 'lieber10':('Früher in Rente oder später','Wahl','',0,0),'lieber11':('Jede Ausgabe aufschreiben oder nach Gefühl','Wahl','',0,0),
 'lieber12':('Erst sparen oder erst ausgeben','Wahl','',0,0),
 'buch01':('Woher der Name kommt (Hefe)','Frage','',1,0),'buch02':('Wie viel Geld für ruhigen Schlaf?','Frage','notgroschen',1,0),
 'buch03':('Disziplin wird überschätzt','Behauptung','',1,0),'buch04':('Gelassenheit verschenken (Advent)','Frage','',1,1),
}
FR = ['Welcher Kauf hat sich wirklich gelohnt?','Mit wem sprichst du offen über Geld?','Was würdest du deinem 20-jährigen Ich über Geld sagen?',
 'Wann hast du dich zuletzt reich gefühlt?','Welche Geldsorge war im Rückblick unnötig?','Was bedeutet Sicherheit für dich: eine Zahl oder ein Gefühl?',
 'Was würdest du tun, wenn Geld keine Rolle spielte?','Was hast du über Geld geglaubt, das nicht stimmte?','Was war deine beste Entscheidung mit Geld?',
 'Wie würdest du einem Kind erklären, was Geld ist?','Was war deine teuerste Lektion?','Worüber streitet ihr, wenn es um Geld geht?',
 'Was kann Geld nicht kaufen, das du gerade brauchst?','Worauf bist du beim Thema Geld stolz?','Wofür ist dir dein Geld zu schade?',
 'Woran merkst du, dass es dir finanziell gut geht?','Wer ist dein Vorbild im Umgang mit Geld?','Worauf verzichtest du leicht, worauf schwer?',
 'Was hat dich Geld über dich selbst gelehrt?','Wie soll sich Geld in zehn Jahren für dich anfühlen?',
 'Was gönnst du dir ohne schlechtes Gewissen?','Wie haben deine Großeltern über Geld gedacht?','Wann bist du beim Thema Geld am ruhigsten?',
 'Was schenkst du, wenn du nichts kaufen willst?','Welche Gewohnheit hat dir beim Geld am meisten geholfen?','Wofür hast du zuletzt gern gespart?',
 'Was wünschst du dir für dein Geld im nächsten Jahr?']
for i, q in enumerate(FR):
    T[f'r-frage{i+5:02d}'] = (q, 'Frage', '', 0, 1 if i >= 20 else 0)
REEL = { # Reel-Fassungen bestehender Karussells
 'r-lieber02':'lieber02','r-lieber03':'lieber03','r-lieber04':('Bar oder Karte','Wahl','',0,0),'r-lieber05':('Gemeinsames Konto oder getrennte Kassen','Wahl','',0,0),
 'r-lieber06':'lieber06','r-lieber07':'lieber07','r-wort01':('Bank','Wortspiel','',0,0),'r-wort02':'wort02','r-wort03':'wort03','r-wort07':'wort07','r-wort08':'wort08',
 'r-ticken01':('Verlustaversion (Münzwurf-Wette)','Frage','',0,0),'r-ticken02':('Theaterkarte verloren','Frage','',0,0),'r-ticken03':'ticken03','r-ticken05':'ticken05',
}
for k, v in REEL.items(): T[k] = T[v] if isinstance(v, str) else v
TAGE = [  # 07:30 Karussell, 11:30 Reel, 16:30 Karussell, 20:30 Reel
 ('04','rechnung01','stimmt01','ticken10'),('05','wort02','r-lieber04','ticken05'),('06','kurz01','stimmt02','lieber02'),
 ('07','rechnung02','r-wort01','ticken06'),('08','wort03','stimmt03','buch02'),('09','kurz02','r-lieber05','lieber03'),
 ('10','rechnung03','stimmt04','lieber06'),('11','kurz03','r-ticken01','ticken03'),('12','wort07','stimmt05','lieber07'),
 ('13','rechnung04','r-lieber02','ticken04'),('14','kurz04','r-wort02','ticken11'),('15','wort08','stimmt06','buch01'),
 ('16','rechnung05','r-ticken02','lieber08'),('17','kurz05','stimmt07','ticken07'),('18','wort09','r-lieber03','ticken12'),
 ('19','rechnung06','stimmt08','lieber09'),('20','kurz06','r-wort03','ticken08'),('21','rechnung07','stimmt09','lieber10'),
 ('22','wort10','r-ticken03','buch03'),('23','kurz07','stimmt10','ticken09'),('24','rechnung08','r-lieber06','lieber11'),
 ('25','kurz08','r-wort07','ticken13'),('26','kurz09','r-ticken05','lieber12'),('27','wort11','stimmt11','rechnung10'),
 ('28','wort12','stimmt12','ticken14'),('29','rechnung09','r-lieber07','buch04'),('30','kurz10','r-wort08','wort13'),
]
WT = ['Mo','Di','Mi','Do','Fr','Sa','So']
rows = []
for n, (tag, k1, r1, k2) in enumerate(TAGE):
    d = dt.date(2026, 11, int(tag)); fr = f'r-frage{n+5:02d}'
    for zeit, pid in (('07:30',k1),('11:30',r1),('16:30',k2),('20:30',fr)):
        thema, hook, mag, methode, neu = T[pid]
        fmt = pid.replace('r-','').rstrip('0123456789')
        rows.append(dict(datum=d.isoformat(), wt=WT[d.weekday()], zeit=zeit, schiene=SCHIENE[zeit], typ='Reel' if zeit in ('11:30','20:30') else 'Karussell',
                         format=FMT[fmt], id=pid, thema=thema, hook=hook, magazin=mag, methode='ja' if methode else 'nein',
                         inhalt='neu' if neu else 'Bestand', woche=1 if d.day<=9 else 2 if d.day<=16 else 3 if d.day<=23 else 4))
json.dump(rows, open('plan_november.json','w'), ensure_ascii=False, indent=0)
print(len(rows), 'Beiträge;', sum(r['inhalt']=='neu' for r in rows), 'neu;', sum(r['methode']=='ja' for r in rows), 'mit Methodenbezug;', sum(bool(r['magazin']) for r in rows), 'mit Magazin-Verweis')
