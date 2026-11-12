# Entscheidungen und offene Punkte

Neueste zuerst. Format: Datum · Entscheidung · Grund. Entscheidungen trifft Björn.

## Stand 12.11.2026 (Texte-Chat, Nacht 11./12.11.)

- **Ich-Zitate (Feld STORY_ICH in Exponate) für alle Objekte mit Kunden-Text geschrieben**: 57 Zitate, Nr. 0–57 außer Nr. 31. Kapitel 3 (Nr. 14–20) ist von Björn abgenommen, alle anderen sind Entwürfe zur Abnahme. Übersicht mit Szenen-Kandidaten als PDF auf der Synology: `Claude outputs/BlauerKubus_Ich-Zitate_Szenen_2026-11-11.pdf` (enthält Kundentexte, daher nicht im Git).
- **Regel Quellen:** Zahlen, Rekorde und Superlative nur aus Kunden-Text, Fakten oder Specs. Allgemein bekannter, unstrittiger Kontext darf als Bild hinein, aber ohne Zahl. Grund: Björn will etwas Spielraum, aber keine erfundenen Belege.
- **Regel Kausalität:** Keine Ursache-Wirkung-Behauptung, die nicht in einer Quelle steht. Grund: „dünne Bergluft" am Pikes Peak ist Fakt, dass Verbrenner deshalb langsamer waren, ist eine Behauptung (Nr. 15).
- **Regel Rückbezug:** Ein Zitat darf auf ein anderes Objekt anspielen, aber nur auf eines, das vorher erscheint (Reihenfolge Kunden-Nr., über Kapitelgrenzen erlaubt), als Antwort darauf. Das frühere Objekt wird dabei nicht kleiner gemacht. Grund: Jede Kachel muss auch ohne die späteren verständlich sein. Ändert sich die Reihenfolge im Film, Bezüge neu prüfen.
- **Nr. 15 ID. R:** Zitat „Man wollte wissen, wozu ein Elektroantrieb im Motorsport fähig ist …" statt einer Variante mit Rückbezug auf den 919, weil die den 919 abwertete.
- **Duktus:** Vom alten Prompt des Felds „Story-Baustein (AI) v2" übernommen: organisatorische Vermerke sind kein Inhalt, Ausschlüsse gelten hart, bei zu wenig Quelle „(zu wenig recherchiert)". Nicht übernommen: freie Nutzung von Allgemeinwissen für Zuspitzung, Charakterzug/Konflikt/Beziehung.
- **Abnahme der Ich-Zitate in Airtable** (12.11. vormittags): neues Feld „Zitat-Status" (Entwurf / überarbeiten / abgenommen) in Exponate, Kapitel 3 = abgenommen, Rest = Entwurf. Neues Lookup-Feld „Szenen-Vorschau" (Vorschaubilder der verknüpften Szenen, nach KI-Score). Im Interface „Inhalts- & Medienstatus" zwei neue Seiten: „Ich-Zitate & Szenen" (Durchsicht je Objekt, Zitat direkt bearbeitbar) und „Ich-Zitate Überblick" (Kennzahlen). Sichtbar für alle, die das Interface sehen (auch Renke/Kunde). Grund: ersetzt das PDF, bleibt aktuell.

## Stand 11.11.2026

- **Ton (vorläufige Richtung):** Im Raum gibt es Ton, Annahme Stereo. Ambient-Bett, Effekte zu den Kachel-Übergängen und gelegentlich Originalton aus den Clips (z. B. Rennszenen). Kein gesprochenes Zitat-Gespräch im Kern, als spätere Ergänzung für einzelne Momente denkbar. Die Effekt-Cues werden aus den Beat-Schritten abgeleitet. Grund: passt zur Kachel-Mechanik, braucht keine Sprecher und Sprachvarianten. Details in der Engine-Übergabe.
- **Automation „Media Links einlesen“ abgesichert** (Formel „Medien-Abgleich“): Leerzeichen/Zeilenumbrüche werden ignoriert; ohne Link steht „kein Link – nichts einzulesen“ (kein Lauf); „neu einlesen“ erst, wenn das Feld 10 Minuten nicht mehr geändert wurde. Grund: Die Automation hatte während Renkes Eingabe halbe Texte eingelesen (Nr. 7, 15, 22, 37 von Hand repariert, Fehlimporte auf „verworfen“). Grenze: Werden alle Links aus einem Feld gelöscht, markiert die Automation die alten Zeilen nicht mehr als entfernt.
- **Szenenerkennung, zweiter Lauf:** 19 weitere Videos (Nr. 5, 7, 15, 20, 21, 22, 23, 24, 27, 28, 37), 434 Szenen, davon 198 ab 5 s. Jetzt 48 Videos mit Ergebnis. `driver.py` überspringt künftig Videos, die schon ein Ergebnis haben.
- **Fachtausch umgesetzt (12.11.):** Nr. 57 Audi AI:ME (107 × 47 × 38 cm) → Fach 2 / A-A-2; Nr. 50 Lamborghini-Felge → Fach 26 / B-F-5 (Annahme: eine Felge, ca. 44 cm, Bestätigung und Maße bei Renke angefragt); Nr. 20 1.9 TDI → Fach 58 / C-D-5 (tragfähig), Fach 56 bleibt leer. Graphic-ID folgt dem Siebdruck Stand 12.11. Fachtiefen bleiben, wie gebaut. Wandabwicklung und Licht müssen neu aus Airtable erzeugt werden.
- **Fächer-Tabelle als feste Zuordnung (12.11.):** neue Tabelle „Fächer" (`tblJerZ3C0jO4oSw8`), 65 Zeilen = Siebdruck-Fachnummern 1–65, mit Fach-ID, Wand, Größe in Modulen (80 × 60 cm) und Verknüpfung zum Exponat. Das Feld „Prüfung" zeigt je Fach „ok", „leer (laut Siebdruck)" oder ⚠ mit Grund (inaktiv, mehrfach belegt, Fach-ID oder Graphic-ID am Exponat weicht ab). Stand: 59 ok, 6 leer (11, 21, 29, 38, 53, 56). Licht-Animation und Wandabwicklung lesen die Zuordnung aus dieser Tabelle und nutzen nur Fächer mit „ok". Grund: Das Regal ist gebaut, die Zuordnung Exponat → Fach muss stabil bleiben, damit das Licht das richtige Objekt hervorhebt.
- **Inaktive Altzeilen entkoppelt (12.11.):** Fach-ID geleert bei Audi V12 TDI (war C-C-3), VR-Motor Passat (B-A-3), Polo WRC (B-R-3), VW MQB (B-N-2, dazu Graphic-ID 27). Alter Wert steht jeweils als Kommentar am Datensatz. Grund: Die Fach-IDs kollidierten mit aktiven Objekten.
- **Layout-Position ist veraltet (12.11.):** Das Feld stammt aus dem alten 34-Spalten-Raster und wird nicht mehr gepflegt. Grasshopper wird nicht mehr gebraucht. Maßgeblich sind Fach-ID und die Fächer-Tabelle.
- **Leistung immer kW mit PS (12.11.):** Anzeigetext DE „230 kW (313 PS)“, EN „230 kW (313 hp)“. Wert und Einheit stehen in kW, PS = kW × 1,36, auf ganze PS gerundet. Ergänzt bei Nr. 1.2 TDI, Race Touareg, V10 TDI, ID. R. XL1 von 75 PS auf 55 kW (75 PS) umgestellt (damit ist die offene Frage PS oder kW erledigt). Neues Feld „Format-Prüfung“ in Specs meldet Verstöße. Ausnahme (Björn, 12.11.): Lade- und V2L-Leistung nur in kW. XL1: 75 PS sind die Gesamtleistung laut Kunde, so bleibt es.
- **Renkes Antworten zu den vier Fakten-Zeilen übernommen** (Mail 11.11.): Nr. 12 Gewicht GFK-Karosserie 10 kg; Nr. 13 Wirkungsgrad 83 % und „Taxibetrieb in Wien und Berlin“ getrennt; Nr. 14 369,4 km/h = Höchstgeschwindigkeit auf der Rekordrunde Nordschleife; Nr. 16 „Future is an Attitude“ als Aussage (Claim von Audi). Specs „Vorschlag“, Texte „Entwurf“, Zeilen in „Fakten“ durchgestrichen.
- **Objekttitel: Maßgeblich ist der Siebdruck** (`4-01-060_Objekttitel_261027_sl_PROD`). Titel_DE/Titel_EN in Airtable am 11.11. angeglichen; bei einsprachigen Titeln steht der Titel auch in Titel_EN. **Graphic-ID = Nummer im Siebdruck** (1–65). Auch Nr. 38 EN „Nardó“, Nr. 13 EN „wheel-hub“ und Nr. 2 „Einmillionster Volkswagen Stoßstange“ wörtlich wie im Siebdruck übernommen (Björn, 11.11. abends: so ist es abgenommen). Renke informiert.
- **Kapitel 3 umfasst Nr. 14–20** (7 Objekte). Renke hat am 11.11. die 919-Nummern neu zugeordnet: Nr. 14 (Rekuperator) steht in Kapitel 3, Nr. 31 (PCCB) in Kapitel 5. PSCB steht weiter auf Nr. 0 ohne Kapitel. Ersetzt die Angabe „Nr. 14–20 und 31“ weiter unten.
- **„VW Karosseriequalität 1997“ gehört zu Nr. 23** (Golf 4 Klarglasscheinwerfer), laut Renke (Mail 11.11.). Liegt in `Quellen/23_golf4-klarglas/`.
- **Medien-Downloads mit yt-dlp auf Björns MacBook**, nicht mehr JDownloader. Ablauf und Regeln in `docs/MEDIEN_ABLAUF.md`. „Renkes OneDrive“ ist die geteilte Bibliothek „VW_FM-Projectshare/01_Autostadt/Blauer Kubus Medien“; Björn kopiert nach `Medien/_additional_input/<Datum>/`.
- **Dubletten werden nicht gelöscht**, sondern nach `Medien/_additional_input/_dubletten/` verschoben.
- **Testkapitel ist Kundenkapitel 3** („Aus Hybriden wird Motorsport und Diesel"; Stand 11.11.: Nr. 14–20, siehe oben). Nr. 14–19 haben Video, Specs und Texte, Nr. 20 hat noch kein Video. Fehlende Medien werden durch Bilder aus dem Airtable-Feld „Abbildung" ersetzt und in der Vorschau als Platzhalter markiert. Grund: das vollste Kapitel; Alternative wäre Kapitel 2 gewesen.
- **Szenenerkennung ist vollständig gelaufen**: 48 Videos, 2.366 Szenen, davon 1.072 ab 5 s. Ergebnisse liegen auf der Synology unter `Medien/_szenen/`, nicht im Git; die Skripte liegen in `tools/szenen-erkennung/`. Alle Szenen sind Vorschläge.
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

- Texte-Chat: Nr. 17 Race Touareg – Dakar-Sieg 2005 (Jahr, Kurzbeschreibung, Kunden-Text) oder 2009–2011 (Fakten)? Zitat nennt vorerst kein Jahr.
- Texte-Chat: Nr. 31 PCCB hat kein Ich-Zitat; Kunden-Text („Hybrid für die Rennstrecke …") und Kurzbeschreibung passen zum 919 Hybrid, nicht zur Bremse.
- Texte-Chat: Jahr-Feld weicht vom Kunden-Text ab bei Nr. 27 (2012), 34 (2005), 54 (1982 statt 90er). Fakten Nr. 14 „5:19:546" vermutlich 5:19,546; Nr. 22 „Campagniolo" → Campagnolo.
- Texte-Chat: Ich-Zitate noch nicht in die Tabelle Texte übernommen (Typ „Ich-Form", Status „Entwurf").
- Nr. 14: Soll die Rundenzeit der Rekordrunde Nordschleife an die Wand? Rückfrage an Renke (11.11.).
- PSCB steht auf Nr. 0 ohne Kapitel (Renke prüft), Skoda Eiskratzer (Renke entscheidet).
- `_additional_input/111126/audi-tt-cup-2014-footage_2160p.mp4`: Zuordnung offen (Nr. 21?).
- Klartext für V2H, V2L, V2G an der Wand; englische Übersetzungen aller Texte.
- Länge je Kapitel, Codec, Abspielsoftware, Pilot-Ablauf. Ton: Lautsprecherzahl und Pegel, Sounddesign, Ton im Filmfile oder als eigene Datei, Rechte am Originalton.
- Quellen mit zu geringer Auflösung für große Kacheln (Stanley, V10 TDI, Audi A2 und weitere): Ersatz oder Einsatz nur klein.
- `story/Blauer_Kubus_Storyline.md` nennt noch die alte Wandgröße.
