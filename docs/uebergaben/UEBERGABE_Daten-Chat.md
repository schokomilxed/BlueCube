# Übergabe an den Chat „Daten" (Airtable-Manager)

Projekt: Blauer Kubus (BlueCube). Stand 11.11.2026. Erst `docs/START.md`, `docs/ARBEITSWEISE.md` und `docs/ENTSCHEIDUNGEN.md` lesen. Schema und Zeilen immer frisch aus Airtable holen, nicht aus alten Chats.

## Aufgabe
Dieser Chat ist der einzige, der Schema und Inhalte von Exponate, Medien, Specs und Texte pflegt. Er koordiniert außerdem Beschaffung und Ablage der Medien (Links, Downloads, Ordnerstruktur, Status in Airtable). Der Szenen-Chat schreibt nur in die Tabelle Szenen, der Engine-Chat liest nur.

## Zuständig für
- **Medien-Pipeline:** Media Links von Renke einlesen (Automation „Media Links einlesen (KI)" legt nur neue Zeilen an, fasst manuell angelegte nicht an), Status in Medien pflegen (neu, URL fehlt, geprüft, heruntergeladen, getrimmt, freigegeben, verworfen, in Quelle entfernt), Download koordinieren, Dateien in `Medien/Quellen/<NN>_<slug>/` ablegen (NN = Kunden-Nr.), Pfad in „Datei lokal" eintragen (relativ zu `Medien`).
- **Medien-Metadaten:** Bildrate, Breite und Höhe in Medien nachtragen. Die Szenenerkennung hat sie je Video bereits ermittelt (`Medien/_szenen/<NN>_<slug>/<Video>.szenen.json`, Felder fps, breite, hoehe). Hero-Kacheln brauchen etwa 2200 px und mehr; zu kleine Quellen markieren.
- **Specs und Texte:** Fakten-Trennung für die übrigen Objekte, Freigabe der Vorschläge durch Björn, englische Übersetzungen (alle Texte stehen auf „fehlt").
- **Kapitel 3 vollständig machen** (Testkapitel, seit 11.11. Nr. 14–20; Nr. 31 PCCB ist nach Kapitel 5 gewandert): Nr. 20 hat noch kein Video, ein Kandidat liegt in `_additional_input/111126`.
- **Interface „Inhalts- & Medienstatus":** Entwurf „Status Überblick" muss von Björn manuell veröffentlicht werden.

## Download und Ablage (geklärt 11.11.2026)
- Ablauf, Werkzeug und Regeln stehen in `docs/MEDIEN_ABLAUF.md` (yt-dlp auf Björns MacBook, Start über „Control your Mac“, Link-Listen in `Medien/youtube/`).
- „Renkes OneDrive“: geteilte Bibliothek „VW_FM-Projectshare/01_Autostadt/Blauer Kubus Medien“. Björn kopiert neue Dateien nach `Medien/_additional_input/<Datum>/`.
- Lieferung 101126 erledigt: „Karosseriequalität 1997“ → Nr. 23, drei Dubletten → `_additional_input/_dubletten/101126/`.
- Lieferung 111126 einsortiert: Nr. 20 (AHF 1.9 TDI), Nr. 21 (2 Videos), Nr. 24 (2 Videos), Nr. 26 (2 Bilder, nur lokal), V10 TDI als Dublette. **Offen:** `audi-tt-cup-2014-footage_2160p.mp4` (Zuordnung unklar, liegt noch in `_additional_input/111126`).
- Heruntergeladen heißt nicht freigegeben. Das Feld Rechte ist nicht gepflegt, alles bleibt Vorschlag.
- Zu kleine Quellen (keine Quelle erreicht 2200 px): Stanley (320 × 240), V10 TDI (384 × 288), Audi A2 und weitere (480p), VW-Newsroom und Audi nur 720p. Originale (.mov) liegen als Links in `Medien/_JDownloader_Originale_fullres.txt`.
- Medien-Abgleich „neu einlesen“ meldet auch reine Leerzeilen-Unterschiede und „siehe OneDrive“ ohne Link. Automation dann nicht auslösen. Bilder aus „Bilder-Medien“ liest die Automation nicht ein: Bild-Zeilen legt dieser Chat an (Schlüssel `Exponat-ID|Anhang-ID|Dateiname`).

## Offene Datenpunkte
- Vier Zeilen im Feld „Fakten" bei Renke: Gewicht Karosserie 10 kg (Nr. 12), Wirkungsgrad 83 % Taxibetrieb (Nr. 13), Rekordzeit Nordschleife mit 369,4 km/h (Nr. 14), „Future is an Attitude" (Nr. 16).
- PSCB steht auf Nr. 0 ohne Kapitel, Skoda Eiskratzer (Renke entscheidet).
- XL1-Leistung ist als 75 PS gespeichert, Entscheidung PS oder kW offen. Klartext für V2H, V2L, V2G an der Wand.
- Specs-Status „Vorschlag" und Texte-Status „Entwurf" warten auf Björns Freigabe.

## Regeln
- Deutsch, kurz und konkret. Plan zeigen, Björn entscheidet.
- Nichts Bestehendes überschreiben oder löschen. Link-Felder nur über Record-IDs schreiben (die Anzeigenamen zeigen den INDEX, nicht die Kunden-Nr.). Felder können über die API nicht im Typ geändert werden.
- Objekte mit Kunden-Nr. benennen, nicht mit Fach-ID.
- Mails an Renke: streng im Ton, „bitte", Kunden-Nr. statt Fach-IDs, Korrekturen soll er selbst in Airtable machen. Feste CC-Empfänger gelten (Liste steht in der Projektanweisung bzw. in Claude, nicht im Repo).
- Kundenmaterial vertraulich: keine Kundendateien, Kundentexte oder Ansprechpartner ins Git.
- Neue Entscheidungen am Ende in `docs/ENTSCHEIDUNGEN.md` eintragen, Björn committet.

## Stand der Daten
- Airtable Base `appd9oVo78FNTrPDd`: Exponate `tbl9POWlpNEFKyFlp`, Medien `tblCalNontccPQ6kp`, Specs `tbla9LSViHl9QFMUZ`, Texte `tblA9TC8t8fHNkCYA`, Szenen `tblrZADeAl29MG8tx`, Beats `tbltwL4X66qWyJJsY`.
- Specs 46, Texte 48 (für 14 Objekte aus „Fakten" getrennt, übernommene Zeilen im Feld durchgestrichen).
- Medien: 37 Quellvideos in `Medien/Quellen` (ohne `_original`; neu am 11.11.: Nr. 21, 23, 27, 28), alle Video-Zeilen mit Bildrate und Pixelmaßen. Szenenerkennung lief für die ersten 29, Ergebnisse nur auf der Synology. 39 neue Bild-Zeilen (Nr. 20, 22, 27, 28) am 11.11. angelegt.
