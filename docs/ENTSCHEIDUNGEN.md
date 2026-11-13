# Entscheidungen und offene Punkte

Neueste zuerst. Format: Datum · Entscheidung · Grund. Entscheidungen trifft Björn.

## Stand 13.11.2026 (Council-Chat)

- **Prinzip V1 statt festem Raster:** Das V1-Grundraster (8 Positionen auf 7 × 5 Modulen) ist der **Ruhepunkt**, in den jeder Teil zurückfaltet; Silhouetten der Objekte, Licht ruht. Die offenen Momente dazwischen sind **dynamisch und richten sich nach dem vorhandenen Footage**: Kachelgröße nach Quellauflösung (Hochskalierung höchstens 2,0), Hoch- oder Querformat nach Bildformat, Zahl der Bildkacheln nach Anzahl guter Szenen, Standzeit länger bei gutem Originalton, Platzhalter klein. Teilungen sind dort erlaubt (Begleit- und Detailkacheln), nicht im Grundraster. Grund: Mehr Teilung im Grundraster bringt nur 80 cm schmale Streifen und keine zusätzlichen textfähigen Kacheln (Vergleich `Blue Cube/BentoGridStyle/engine/v1plus/V1plus_Varianten.png`). Hat ein Teil weniger als 8 Objekte, darf der Generator Grundpositionen zusammenlegen.
- **Film-Teile statt Umnummerieren:** neues Feld „Film-Teil" in Exponate (`fldg0vCqzHoxBVUKB`). Kunden-Nr. und Reihenfolge bleiben, die Kette der Ich-Zitate (Rückbezug nur nach hinten) bleibt intakt. Jeder Film-Teil bekommt ein eigenes Grundraster und einen Untertitel.
  - Kapitel 6: 6.1 Rekordfahrten (Nr. 34–38), 6.2 Motorenkonzepte (39–44), 6.3 Motorsporttechnik für die Serie (45–48). Grund: Titel ist dreiteilig, die Kundenreihenfolge folgt ihm bereits; 15 Objekte am Stück wären zu lang.
  - Kapitel 2: 2.1 Alternative Antriebe (Nr. 5–8), 2.2 Sparsamkeit (9–13). Untertitel in Filmreihenfolge, der Kapiteltitel des Kunden bleibt unverändert. Formel E (Nr. 6) ist Kontrapunkt in 2.1, Lohner-Porsche (Nr. 13) leitet als erster Hybrid zu Kapitel 3 über.
  - Kapitel 1, 3, 4, 5, 7, 8 laufen ungeteilt (4–8 Objekte).
- **Nr. 41 Corrado-Heckspoiler bleibt in 6.2** und grätscht als Figur zwischen die Motoren, mit Rückbezug auf die Spoiler von Veyron und Chiron. Ich-Zitat neu (DE/EN, Status Entwurf): „Kurz dazwischen: Was nützen all die Zylinder, wenn die Kraft nicht auf der Straße bleibt? …"
- **Grundraster-Familie statt einem Layout** (Björn: „A will ich absolut nicht"): V1 (6–8 Objekte, eher hohe Formate), D (6–8 Objekte, eher breite Formate, waagrecht geteilt), V1-groß (4–5 Objekte). Auswahl per Regel aus Anzahl und Format der Herobilder, innerhalb eines Film-Teils gleich, Override in Airtable möglich. Belegung der Kacheln automatisch nach Bildformat und Auflösung. Ansicht: `Blue Cube/BentoGridStyle/engine/v1plus/Grundraster_Familie.png`.
- **Freie Kachel im Ruhezustand trägt den Kapitel- bzw. Teiltitel als Text.**
- **Die Medienfläche erzählt die Geschichte zum Exponat, sie zeigt nicht das Exponat noch einmal** (Pokal, Bremsscheibe, Spoiler stehen im Regal; auf der Wand z. B. der Chiron). Neue Felder in Exponate: „Herobild" (Anhang, `fldMiuEiBQK9DP8eu`), „Herobild geprüft" (Checkbox), „Herobild-Hinweis" (Warnung). Vorschläge für Nr. 1–4, 14–20, 34–38 eingetragen, Björn prüft; 10 davon unter 1920 px oder mit besserem Motiv nachzuliefern (Hinweisfeld).
- Offen: Untertitel-Texte DE/EN für 2.1, 2.2, 6.1–6.3 brauchen die Abnahme des Kunden.

### Nachtrag 13.11.2026 (Council-Chat, nachmittags)
- **Render-Fassungen:** Arbeitsfassungen 1920 breit, **30 fps**, mit Ton (`tools/render.py … --rw 1920`). 4K (3840, Vorgabe ohne `--rw`) nur zu Meilensteinen: 1:1-Test 18.11., inhaltlicher Stopp 23.11., Master; dazu einzelne 4K-Standbilder kritischer Momente.
- **Renderzeit:** Engpass ist das Springen in den Clips (seek), nicht die Pixelzahl. Nächster Schritt: Clips vorab in Einzelbilder zerlegen; größere Renders auf dem Mac (mehr Kerne).
- **Ton v2 (Kapitel 3, Test):** Jeder Schritt klingt (Zug über die Schrittdauer + Akzent bei Ankunft), Pegel nach bewegter Fläche; Akzente bei Öffnen, Vollbild, Rückfaltung. Klangthema aus dem ID.R-Originalton (Drone im Bett + Signatur am Kapitelanfang). Originalton nur beim größten Clip ≥ 4×3, nur Motor/Umgebung laut Klassifikator. Alle KI-Klänge `_TEST_free`, nicht für den Master.
- **Herobild:** Vorschläge für alle übrigen Objekte in Airtable eingetragen, „Herobild geprüft“ bleibt bei Björn.

## Stand 12.11.2026 (Council-Chat, abends)

- **Eröffnung 30.11.2026.** Zeitplan, Grundsätze und offene Klärungen in `docs/PLAN_Eroeffnung.md`. Inhaltlicher Stopp 23.11.
- **V1+ statt Mosaik:** V1 als Grundlage mit 2–3 zusätzlichen Unterteilungen. Grund: Mosaik überzeugt nicht.
- **Ein Ort für Bewegung:** höchstens 1 Hero-Video und 1 Begleit-Clip gleichzeitig. Grund: viele parallele Szenen wirken chaotisch, nicht vielfältig.
- **Generieren statt choreografieren:** alle Kapitel aus einem Generator mit den V1-Vorlagen und Airtable-Daten. Grund: Kundendaten kommen spät und ändern sich; das war von Anfang an der Grund für den generativen Ansatz.
- **Engine ist die einzige Zeitquelle** für Bild, Licht und Ton-Cues; die 272,153 s des Lichtplayers sind keine Vorgabe mehr.
- **Render-Durchstich bestanden:** Kapitel 3 V1 in 3840 × 2058 bei 30 fps, ca. 19 min Renderzeit. Befunde im Plan. Offen: Höhe 2057 ist für H.264/H.265 ungerade, Festwert in ARBEITSWEISE auf 2058 (oder 2056) ändern – Björn entscheidet.

## Stand 12.11.2026 (Texte-Chat, Nacht 11./12.11.)

- **Ich-Zitate (Feld STORY_ICH in Exponate) für alle Objekte mit Kunden-Text geschrieben**: 57 Zitate, Nr. 0–57 außer Nr. 31. Kapitel 3 (Nr. 14–20) ist von Björn abgenommen, alle anderen sind Entwürfe zur Abnahme. Übersicht mit Szenen-Kandidaten als PDF auf der Synology: `Claude outputs/BlauerKubus_Ich-Zitate_Szenen_2026-11-11.pdf` (enthält Kundentexte, daher nicht im Git).
- **Regel Quellen:** Zahlen, Rekorde und Superlative nur aus Kunden-Text, Fakten oder Specs. Allgemein bekannter, unstrittiger Kontext darf als Bild hinein, aber ohne Zahl. Grund: Björn will etwas Spielraum, aber keine erfundenen Belege.
- **Regel Kausalität:** Keine Ursache-Wirkung-Behauptung, die nicht in einer Quelle steht. Grund: „dünne Bergluft" am Pikes Peak ist Fakt, dass Verbrenner deshalb langsamer waren, ist eine Behauptung (Nr. 15).
- **Regel Rückbezug:** Ein Zitat darf auf ein anderes Objekt anspielen, aber nur auf eines, das vorher erscheint (Reihenfolge Kunden-Nr., über Kapitelgrenzen erlaubt), als Antwort darauf. Das frühere Objekt wird dabei nicht kleiner gemacht. Grund: Jede Kachel muss auch ohne die späteren verständlich sein. Ändert sich die Reihenfolge im Film, Bezüge neu prüfen.
- **Nr. 15 ID. R:** Zitat „Man wollte wissen, wozu ein Elektroantrieb im Motorsport fähig ist …" statt einer Variante mit Rückbezug auf den 919, weil die den 919 abwertete.
- **Duktus:** Vom alten Prompt des Felds „Story-Baustein (AI) v2" übernommen: organisatorische Vermerke sind kein Inhalt, Ausschlüsse gelten hart, bei zu wenig Quelle „(zu wenig recherchiert)". Nicht übernommen: freie Nutzung von Allgemeinwissen für Zuspitzung, Charakterzug/Konflikt/Beziehung.
- **STORY_ICH heißt jetzt STORY_ICH_DE** (Feld-ID unverändert `fldmTdbyuUAD7LAuk`), neues Feld **STORY_ICH_EN** (`fld60CyTcXBwYhkIQ`) mit englischer Fassung aller 57 Zitate (Entwurf von Claude, britisches Englisch, metrische Einheiten, „PS" beim Veyron beibehalten). 12.11. abends. Grund: Kunde nimmt DE und EN zusammen im Interface ab. Skripte bitte über Feld-ID, nicht über den Namen lesen.
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
- **Hubraum immer in cm³ (13.11.):** Gerundete Angaben bekommen „ca.“, z. B. Race Touareg „ca. 2.500 cm³“ (Kunde nannte 2,5 l). Alle 49 Specs von Björn am 13.11. auf „geprüft“ gesetzt.
- **Nr. 20 1.9 TDI, echte Maße von Renke (13.11.):** 33 × 30 × 38 cm, passt in Fach 58.
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
