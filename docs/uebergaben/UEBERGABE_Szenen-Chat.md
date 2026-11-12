# Übergabe an den Chat „Szenen"

Projekt: Blauer Kubus (BlueCube). Ziel dieses Chats: aus den Quellvideos pro Objekt 2–3 Szenenkandidaten (5–10 s) vorschlagen, die zu Exponat und Text passen. Du schlägst vor, Björn gibt in Airtable frei.

## Stand
- Schnitterkennung ist vollständig gelaufen (zweiter Lauf 11.11.): 48 Videos, 2.366 Szenen, davon 1.072 ab 5 s.
- Ergebnisse: `Blue Cube/Medien/_szenen/<NN>_<slug>/<Video>.szenen.json` und `.csv` (nr, von, bis, dauer, ab_5s). Mittelbilder der Szenen ab 5 s: `thumbs/<Video>/NNN.jpg`. Details in `_szenen/README.md`.
- Quellen: `Medien/Quellen/<NN>_<slug>/`, Objekte 06, 08–12, 14–19, 37. Originale nie verändern.
- Airtable Base `appd9oVo78FNTrPDd`: Exponate `tbl9POWlpNEFKyFlp`, Medien `tblCalNontccPQ6kp`, Specs `tbla9LSViHl9QFMUZ`, Texte `tblA9TC8t8fHNkCYA`, Szenen `tblrZADeAl29MG8tx` (noch leer), Beats `tbltwL4X66qWyJJsY`. Verknüpfungen immer über Record-IDs, nicht über Anzeigenamen.
- Texte und Specs: Aussagen/Zahlen aus dem Feld „Fakten" (Text von Renke) sind getrennt, alles Status „Vorschlag"/„Entwurf".

## Bekannte Grenzen
- Auflösung zu klein für große Kacheln: Stanley RaceDay und Stanley_DARPA (320×240), Fusca (352×288), V10 TDI (384×288), Phaeton 2010 (420×226), Audi A2 und mehrere weitere (480p).
- Wenig Material: 919 „Technology" (keine Szene ab 5 s), 919 „New king of the ring" (4), XL1 (je 2–4).
- Erkennung findet harte Schnitte, keine Überblendungen oder Kamerafahrten.
- 1.294 Szenen sind kürzer als 5 s; für Loops zu kurz, außer sie werden verlängert.

## Regeln
- Deutsch, kurz und konkret. Erst Plan zeigen, Björn entscheidet.
- Nichts Bestehendes überschreiben. Cowork-Artifact „blauer-kubus-layout" nicht ändern.
- Kundenmaterial vertraulich. Rechte-Feld nicht gepflegt: Szenen nur vorschlagen, nie als freigegeben behandeln.
- Objekte immer mit Kunden-Nr. benennen, nicht mit Fach-ID. Kundenkapitel 1–8, nicht die alte Story-Nummerierung.
- Ergebnisse als Dateien im Ordner ablegen, nicht nur im Chat.

## Nächste Schritte
1. Pilot ist Kundenkapitel 3 (von Björn bestätigt): Nr. 14 Porsche 919, 15 ID. R, 16 RS Q e-tron, 17 Race Touareg, 18 Stanley, 19 V10 TDI, 20 1.9 TDI (Kapitel 3 umfasst Nr. 14–20; Nr. 31 ist nach Kapitel 5 gewandert). Nr. 20 hat ein Video ohne Tonspur und ohne Schnitte (eine Szene). Wo Szenen fehlen, dienen die Bilder aus dem Feld „Abbildung" in Exponate als Platzhalter. Szenen dafür nicht erfinden.
2. Szenen gegen Exponat und Text bewerten (Mittelbilder ansehen, Texte aus Airtable lesen), pro Objekt 2–3 Kandidaten mit Von/Bis, Begründung, geeigneten Kachelgrößen und Auflösungswarnung.
3. Kandidaten als Vorschau (Kontaktbogen) zeigen. Erst nach Björns Okay in die Tabelle Szenen schreiben, Status „Vorschlag".
4. Danach Clips trimmen (Medien/Clips/<Objekt>/) erst nach Freigabe in Airtable.

## Offen (nicht in diesem Chat lösen)
Renkes Antworten zu vier Fakten-Zeilen, PCCB/PSCB-Nummerierung, Nr. 14 Kundenkapitel, Skoda Eiskratzer, Codec und Playout-Software.


## Stand 12.11.2026 abends: Ton-Bewertung je Szene ergänzen (keine neue Szenenerkennung)
Die Szenengrenzen bleiben gültig; 47 von 48 Quellen haben Ton. Es fehlt nur eine Bewertung des Originaltons pro Szene, weil Originalton beim Hero künftig hörbar sein kann (siehe ENTSCHEIDUNGEN 12.11. abends).
1. Für alle Szenen ab 5 s den Ton einordnen: Skript `tools/szenen-erkennung/ton_bewerten.py` (AudioSet-Klassifikator AST, CPU, ca. 1 s je Szene). Eingabe: Quelle als Mono-16-kHz-WAV + `<Video>.szenen.csv`. Ausgabe je Szene: Fahrzeug, Musik, Sprache (0–1), Lautheit (dBFS), Vorschlag ★ (Fahrzeug > 0,15, Musik < 0,3, Sprache < 0,3).
2. Ergebnisse neben die Szenendateien legen: `Medien/_szenen/<NN>_<slug>/<Video>.ton.csv`.
3. In der Tabelle Szenen Felder ergänzen: „Ton Fahrzeug", „Ton Musik", „Ton Sprache", „Lautheit", „Originalton-Vorschlag" (automatisch) und getrennt „Originalton-Status" (ungeprüft / gehört ok / abgelehnt, setzt nur Björn). Originalton-Rechte sind unabhängig von den Bildrechten.
4. Bei der Kandidatenwahl (2–3 je Objekt) zählt guter Originalton als Kriterium neben der Bildqualität.
- Der Klassifikator sortiert nur vor und irrt (Beispiel: 15.1.027 als „Sprache" eingeordnet). Elektrische Fahrzeuge erscheinen oft als „Whir"/„Hum", nicht als „Engine"; das ist in den Kategorien berücksichtigt.
- Test 12.11.: Nr. 15 Quelle 3 (`20180706143134_720p.mp4`) hat in 15 von 16 Szenen ab 5 s sauberen Rennton (stark: 15.3.038, 15.3.001, 15.3.016). Kandidaten für Nr. 15 dort suchen.
