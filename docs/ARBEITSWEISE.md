# Blauer Kubus – Arbeitsweise und Übergabe

Stand: 10.11.2026. Gilt für alle Arbeitsstränge (Daten, Szenen, Engine). Wer einen neuen Chat startet, liest zuerst diese Datei und holt Schema und Zeilen frisch aus Airtable, nicht aus alten Chats.

## Ziel

Aus dem Kapitel-2-Mockup (`BentoGridStyle/kapitel2`) wird die Entwicklungsplattform für den ganzen Film: 8 Kundenkapitel, 57 Objekte. Mehrere Szenen aus den Quellvideos laufen gleichzeitig auf Kacheln verschiedener Größe. Die Kacheln klappen auf, schieben sich und falten sich ins Grundraster zurück (Bento-Stil). **Final ist ein gerenderter Film**, das HTML ist Entwicklungs- und Vorschauwerkzeug, keine Dauerinstallation.

## Feste Zielwerte

| Thema | Wert |
|---|---|
| Medienfläche | 5,60 × 3,00 m = 7 × 5 Module à 80 × 60 cm (Wandabwicklung vom 25.8.2026) |
| Projektor | Panasonic PT-REQ15, Ausgabe 3840 × 2400 (16:10) |
| Render-Format | 3840 × 2057 px (Seitenverhältnis der Fläche 28:15, füllt die Breite), ca. 6,9 px/cm, Modul ca. 549 × 411 px |
| Bildrate | 60 fps Master, 30 fps daraus abgeleitet; die Engine rechnet zeitbasiert (Sekunden) |
| Länge | ca. 30 s je Objekt insgesamt |
| Playout | Abspielrechner spielt Film und Art-Net-Cueliste im Gleichlauf; Cues entstehen aus den Beats auf derselben Zeitbasis |
| Loop-Länge Mockup | 272,153 s (Beats 1–26), der gerenderte Film muss dieselbe Länge haben |

Noch offen: Länge je Kapitel, Ton, Codec, Abspielsoftware, Pilotobjekte (früherer Vorschlag Kunden-Nr. 27, 15, 18).

## Kapitelnummerierung

Es gibt zwei Zählungen, nicht verwechseln:

- **Kundenkapitel 1–8** (gilt für Airtable und Film): 1 Historie Aufstieg VW · 2 Sparsamkeit und alternative Antriebe · 3 Aus Hybriden wird Motorsport und Diesel · 4 Qualität, Licht und Digitale Technik · 5 Sicherheit und Bremsen · 6 Rekordfahrten, Motorenkonzepte und Motorsporttechnik für die Serie · 7 Design · 8 Auto von Morgen, Future Concepts.
- **Story-Nummerierung** (alt, 4 Kapitel): „Kapitel 2 · Fahrdynamik & Sicherheit" im Mockup und die Momentlisten in `story/`. Das ist **nicht** Kundenkapitel 2. Verknüpft wird erst nach Rückfrage (Abgleich siehe `docs/Kundenabfolge_vs_unsere_Momente.pdf`).

Objekte werden immer über die **Kunden-Nr. (1–57)** benannt, nicht über Fach-IDs.

## Datenmodell (Airtable, Base `appd9oVo78FNTrPDd`)

| Tabelle | ID | Inhalt |
|---|---|---|
| Exponate | `tbl9POWlpNEFKyFlp` | Kunden-Nr., Kundenkapitel, Fach-ID, Maße, Cluster, Texte, Fakten (Text von Renke) |
| Medien | `tblCalNontccPQ6kp` | ein Clip oder Bild je Zeile: Status, Von/Bis, Quelle, Rechte, Datei lokal, Bildrate, Breite, Höhe |
| Specs | `tbla9LSViHl9QFMUZ` | Zahl, Einheit, Label DE/EN, Quelle, Prüfstatus (Werte mit zwei Dezimalstellen speichern, beim Auslesen je nach Größe runden: 0–100 km/h in 2,25 s, aber 500 kW) |
| Texte | `tblA9TC8t8fHNkCYA` | Typ, DE, EN, Status |
| Szenen | `tblrZADeAl29MG8tx` | Ausschnitt, Von/Bis, Loop, Score, Kachelformat, „nehmen" |
| Beats | `tbltwL4X66qWyJJsY` | Kapitel, Reihenfolge, Register, Dauer, Spot, Kachel-Layout |

Das Feld „Fakten" (früher „Sicherheitskommentar", Text von Renke) wird getrennt in **Specs** (Zahlen), **Texte** (Aussagen) und **Interna** (Beschaffungsnotizen, gehören nicht an die Wand).

Medien-Status: neu, URL fehlt, geprüft, heruntergeladen, getrimmt, freigegeben, verworfen, in Quelle entfernt. Eine Automation („Media Links einlesen (KI)") legt neue Zeilen nur aus Media Links an und fasst manuell angelegte Zeilen nicht an.

## Dateien (Synology, Ordner „Blue Cube")

- `Medien/Quellen/<NN>_<slug>/` Originale, `Medien/Clips/<NN>_<slug>/` getrimmt. NN ist die Kunden-Nr., der Slug beschreibt das Objekt (z. B. `14_919-rekuperator`).
- Pfade in Airtable („Datei lokal") sind relativ zu `Medien`.
- Neue, noch unsortierte Lieferungen liegen in `Medien/_additional_input/`.
- Weitere Ordner: `Layout`, `Story`, `inputRenke`, `freigegebene Stände`.

## Wer arbeitet wo

| Strang | Arbeitet in | Liest |
|---|---|---|
| Daten | Airtable | Pfade im Medien-Ordner |
| Szenen | Synology (Quellen, Clips) und Airtable | nichts aus Git |
| Engine | dieses Repo | Airtable (Schema, freigegebene Szenen) |

- **Daten:** Specs-/Aussagen-Trennung, Kundentexte importieren, Englisch ergänzen, Medien pflegen.
- **Szenen:** Szenenerkennung, KI-Bewertung gegen Exponat und Text, 2–3 Kandidaten à 5–10 s je Objekt, Freigabe in Airtable.
- **Engine:** Szenen und Beats als JSON je Kapitel statt von Hand in JS, Kachelmechanik (Rollen, Ruhe/Bewegung, Loop-Synchronisation), Kapitel 2 als Regressionstest, Render und Art-Net-Cueliste.

Pipeline: Szenenerkennung → KI-Bewertung → Vorauswahl → Freigabe in Airtable → Build → Pilot mit drei Objekten → Rollout auf alle Kapitel.

## Regeln

- Nichts Bestehendes überschreiben. Das Cowork-Artifact „blauer-kubus-layout" nicht ohne Freigabe ändern.
- Szenen sind Vorschläge, nicht freigegeben, solange das Rechte-Feld nicht gepflegt ist.
- Kundenmaterial vertraulich behandeln. Kundendateien, Kundentexte und Airtable-Exporte werden nicht eingecheckt (siehe `README.md`).
- Videos gehören nicht ins Repo. Die Engine bekommt Clips über die Pfade aus Airtable.
- Vor dem Bauen einen Plan zeigen, Entscheidungen trifft Björn.

## Bekannte Altlasten

- `story/Blauer_Kubus_Storyline.md` nennt noch die alte Wandgröße, die Momentlisten haben noch die alte 4-Kapitel-Struktur.
- Airtable-Zuordnung offen: PCCB/PSCB (Kunden-Nr. 31 ist PSCB, Renke korrigiert die Nummern), Nr. 14 Rekuperator ohne Kundenkapitel, Skoda Eiskratzer, „VW Karosseriequalität 1997". Vier Dateien liegen noch unsortiert in `Medien/_additional_input/`.
