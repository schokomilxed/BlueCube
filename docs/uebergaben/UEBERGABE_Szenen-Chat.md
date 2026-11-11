# Übergabe an den Chat „Szenen"

Projekt: Blauer Kubus (BlueCube). Ziel dieses Chats: aus den Quellvideos pro Objekt 2–3 Szenenkandidaten (5–10 s) vorschlagen, die zu Exponat und Text passen. Du schlägst vor, Björn gibt in Airtable frei.

## Stand
- Schnitterkennung ist gelaufen: 29 Videos, 1.932 Szenen, davon 874 ab 5 s.
- Ergebnisse: `Blue Cube/Medien/_szenen/<NN>_<slug>/<Video>.szenen.json` und `.csv` (nr, von, bis, dauer, ab_5s). Mittelbilder der Szenen ab 5 s: `thumbs/<Video>/NNN.jpg`. Details in `_szenen/README.md`.
- Quellen: `Medien/Quellen/<NN>_<slug>/`, Objekte 06, 08–12, 14–19, 37. Originale nie verändern.
- Airtable Base `appd9oVo78FNTrPDd`: Exponate `tbl9POWlpNEFKyFlp`, Medien `tblCalNontccPQ6kp`, Specs `tbla9LSViHl9QFMUZ`, Texte `tblA9TC8t8fHNkCYA`, Szenen `tblrZADeAl29MG8tx` (noch leer), Beats `tbltwL4X66qWyJJsY`. Verknüpfungen immer über Record-IDs, nicht über Anzeigenamen.
- Texte und Specs: Aussagen/Zahlen aus dem Feld „Fakten" (Text von Renke) sind getrennt, alles Status „Vorschlag"/„Entwurf".

## Bekannte Grenzen
- Auflösung zu klein für große Kacheln: Stanley RaceDay und Stanley_DARPA (320×240), V10 TDI (384×288), Audi A2 und mehrere weitere (480p).
- Wenig Material: 919 „Technology" (keine Szene ab 5 s), 919 „New king of the ring" (4), XL1 (je 2–4).
- Erkennung findet harte Schnitte, keine Überblendungen oder Kamerafahrten.
- 1.058 Szenen sind kürzer als 5 s; für Loops zu kurz, außer sie werden verlängert.

## Regeln
- Deutsch, kurz und konkret. Erst Plan zeigen, Björn entscheidet.
- Nichts Bestehendes überschreiben. Cowork-Artifact „blauer-kubus-layout" nicht ändern.
- Kundenmaterial vertraulich. Rechte-Feld nicht gepflegt: Szenen nur vorschlagen, nie als freigegeben behandeln.
- Objekte immer mit Kunden-Nr. benennen, nicht mit Fach-ID. Kundenkapitel 1–8, nicht die alte Story-Nummerierung.
- Ergebnisse als Dateien im Ordner ablegen, nicht nur im Chat.

## Nächste Schritte
1. Pilot ist Kundenkapitel 3 (von Björn bestätigt): Nr. 14 Porsche 919, 15 ID. R, 16 RS Q e-tron, 17 Race Touareg, 18 Stanley, 19 V10 TDI. Nr. 20 und 31 haben kein Video; dort dienen die Bilder aus dem Feld „Abbildung" in Exponate als Platzhalter. Szenen dafür nicht erfinden.
2. Szenen gegen Exponat und Text bewerten (Mittelbilder ansehen, Texte aus Airtable lesen), pro Objekt 2–3 Kandidaten mit Von/Bis, Begründung, geeigneten Kachelgrößen und Auflösungswarnung.
3. Kandidaten als Vorschau (Kontaktbogen) zeigen. Erst nach Björns Okay in die Tabelle Szenen schreiben, Status „Vorschlag".
4. Danach Clips trimmen (Medien/Clips/<Objekt>/) erst nach Freigabe in Airtable.

## Offen (nicht in diesem Chat lösen)
Renkes Antworten zu vier Fakten-Zeilen, PCCB/PSCB-Nummerierung, Nr. 14 Kundenkapitel, Skoda Eiskratzer, Codec und Playout-Software.
