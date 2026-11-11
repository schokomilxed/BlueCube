# Entscheidungen und offene Punkte

Neueste zuerst. Format: Datum · Entscheidung · Grund. Entscheidungen trifft Björn.

## Stand 11.11.2026

- **Automation „Media Links einlesen“ abgesichert** (Formel „Medien-Abgleich“): Leerzeichen/Zeilenumbrüche werden ignoriert; ohne Link steht „kein Link – nichts einzulesen“ (kein Lauf); „neu einlesen“ erst, wenn das Feld 10 Minuten nicht mehr geändert wurde. Grund: Die Automation hatte während Renkes Eingabe halbe Texte eingelesen (Nr. 7, 15, 22, 37 von Hand repariert, Fehlimporte auf „verworfen“). Grenze: Werden alle Links aus einem Feld gelöscht, markiert die Automation die alten Zeilen nicht mehr als entfernt.
- **Szenenerkennung, zweiter Lauf:** 19 weitere Videos (Nr. 5, 7, 15, 20, 21, 22, 23, 24, 27, 28, 37), 434 Szenen, davon 198 ab 5 s. Jetzt 48 Videos mit Ergebnis. `driver.py` überspringt künftig Videos, die schon ein Ergebnis haben.
- **Fachtausch Nr. 50/57 und Nr. 20 (Renke, 11.11.):** nicht umgesetzt, Maße bei Renke angefragt (echte Maße AI:ME und Rumpfmotor, eine Felge oder Paar). Nach geschätzten Maßen passen Felgen-Paar in Fach 26 und Motor in Fach 58 nicht.
- **Renkes Antworten zu den vier Fakten-Zeilen übernommen** (Mail 11.11.): Nr. 12 Gewicht GFK-Karosserie 10 kg; Nr. 13 Wirkungsgrad 83 % und „Taxibetrieb in Wien und Berlin“ getrennt; Nr. 14 369,4 km/h = Höchstgeschwindigkeit auf der Rekordrunde Nordschleife; Nr. 16 „Future is an Attitude“ als Aussage (Claim von Audi). Specs „Vorschlag“, Texte „Entwurf“, Zeilen in „Fakten“ durchgestrichen.
- **Objekttitel: Maßgeblich ist der Siebdruck** (`4-01-060_Objekttitel_261027_sl_PROD`). Titel_DE/Titel_EN in Airtable am 11.11. angeglichen; bei einsprachigen Titeln steht der Titel auch in Titel_EN. **Graphic-ID = Nummer im Siebdruck** (1–65). Auch Nr. 38 EN „Nardó“, Nr. 13 EN „wheel-hub“ und Nr. 2 „Einmillionster Volkswagen Stoßstange“ wörtlich wie im Siebdruck übernommen (Björn, 11.11. abends: so ist es abgenommen). Renke informiert.
- **Kapitel 3 umfasst Nr. 14–20** (7 Objekte). Renke hat am 11.11. die 919-Nummern neu zugeordnet: Nr. 14 (Rekuperator) steht in Kapitel 3, Nr. 31 (PCCB) in Kapitel 5. PSCB steht weiter auf Nr. 0 ohne Kapitel. Ersetzt die Angabe „Nr. 14–20 und 31“ weiter unten.
- **„VW Karosseriequalität 1997“ gehört zu Nr. 23** (Golf 4 Klarglasscheinwerfer), laut Renke (Mail 11.11.). Liegt in `Quellen/23_golf4-klarglas/`.
- **Medien-Downloads mit yt-dlp auf Björns MacBook**, nicht mehr JDownloader. Ablauf und Regeln in `docs/MEDIEN_ABLAUF.md`. „Renkes OneDrive“ ist die geteilte Bibliothek „VW_FM-Projectshare/01_Autostadt/Blauer Kubus Medien“; Björn kopiert nach `Medien/_additional_input/<Datum>/`.
- **Dubletten werden nicht gelöscht**, sondern nach `Medien/_additional_input/_dubletten/` verschoben.
- **Testkapitel ist Kundenkapitel 3** („Aus Hybriden wird Motorsport und Diesel"; Stand 11.11.: Nr. 14–20, siehe oben). Nr. 14–19 haben Video, Specs und Texte, Nr. 20 hat noch kein Video. Fehlende Medien werden durch Bilder aus dem Airtable-Feld „Abbildung" ersetzt und in der Vorschau als Platzhalter markiert. Grund: das vollste Kapitel; Alternative wäre Kapitel 2 gewesen.
- **Szenenerkennung ist gelaufen**: 29 Videos, 1.932 Szenen, davon 874 ab 5 s. Ergebnisse liegen auf der Synology unter `Medien/_szenen/`, nicht im Git; die Skripte liegen in `tools/szenen-erkennung/`. Alle Szenen sind Vorschläge.
- **Übergaben und Entscheidungen gehören ins Git**, Inhalte (Medien, Kundendateien) auf die Synology. Einstieg ist `docs/START.md`.
- **Arbeit in drei Strängen** (je ein eigener Chat): Daten, Szenen, Engine. Übergaben liegen in `docs/uebergaben/`.

## Davor (bis 10.11.2026)

- **Final ist ein gerenderter Film**, kein HTML in der Installation. 3840 × 2057 px, 60 fps Master, 30 fps abgeleitet, Art-Net-Cueliste läuft im Gleichlauf (Details in `ARBEITSWEISE.md`).
- **Objekte werden mit der Kunden-Nr. benannt**, nie mit der Fach-ID. Kundenkapitel 1–8 gelten für Airtable und Film; die alte Story-Nummerierung („Kapitel 2 · Fahrdynamik & Sicherheit" im Mockup) wird nicht ohne Rückfrage verknüpft.
- **Das Feld „Fakten" (Text von Renke, früher „Sicherheitskommentar")** wird in Specs (Zahlen, Status „Vorschlag"), Texte (Aussagen, Status „Entwurf") und Interna getrennt. Übernommene Zeilen sind im Feld durchgestrichen, das Originalfeld bleibt sonst unverändert. Specs und Texte sind für 14 Objekte angelegt.
- **Szenen sind Vorschläge**, solange das Rechte-Feld nicht gepflegt ist. Nichts gilt als freigegeben.
- **Ordner `Medien/Quellen/14_919-rekuperator`** (vorher anders benannt), Medien-Zeilen angepasst, elf neue Medien-Zeilen angelegt.
- **XL1-Leistung** ist als 75 PS gespeichert (nicht kW). Maße und cW-Wert stehen nur als Anzeigetext, weil „Wert" zwei Dezimalstellen hat.
- **Mails an Renke**: streng im Ton („bitte"), mit Kunden-Nr. statt Fach-IDs, ohne Hinweise zur Auflösung. Feste CC-Empfänger gelten (Liste in Claude, nicht im Repo).
- **Cowork-Artifact „blauer-kubus-layout"** wird nicht ohne Freigabe verändert. Nichts Bestehendes wird überschrieben.

## Offen

- Nr. 14: Soll die Rundenzeit der Rekordrunde Nordschleife an die Wand? Rückfrage an Renke (11.11.).
- PSCB steht auf Nr. 0 ohne Kapitel (Renke prüft), Skoda Eiskratzer (Renke entscheidet).
- `_additional_input/111126/audi-tt-cup-2014-footage_2160p.mp4`: Zuordnung offen (Nr. 21?).
- XL1-Leistung in PS oder kW; Klartext für V2H, V2L, V2G an der Wand; englische Übersetzungen aller Texte.
- Länge je Kapitel, Ton, Codec, Abspielsoftware, Pilot-Ablauf.
- Quellen mit zu geringer Auflösung für große Kacheln (Stanley, V10 TDI, Audi A2 und weitere): Ersatz oder Einsatz nur klein.
- `story/Blauer_Kubus_Storyline.md` nennt noch die alte Wandgröße.
