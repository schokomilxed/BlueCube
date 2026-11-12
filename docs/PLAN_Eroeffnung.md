# Plan bis zur Eröffnung · Blauer Kubus

Stand 12.11.2026 abends. Von Björn freigegeben. Eröffnung **Montag, 30.11.2026**.

## Grundsätze
- **Generieren statt choreografieren.** Ein Generator belegt die Bewegungsvorlagen A/B/C (V1) je Objekt aus Airtable. Handarbeit nur bei Szenenwahl und Ausnahmen. Grund: Kundeninhalte kommen spät und ändern sich; jede Änderung ist dann nur ein neuer Lauf.
- **Engine ist die einzige Zeitquelle.** Bild, Lichtliste (aus `spot`/Fach-ID je Beat + Tabelle Fächer, nur „ok") und Ton-Cues werden aus ihr erzeugt. Die bisherige Loop-Länge 272,153 s (Beats 1–26 des alten Mockups) ist keine Vorgabe mehr.
- **V1+ statt Mosaik.** V1-Grundraster mit 2–3 zusätzlichen Unterteilungen (Vorschlag: P2 und P6, optional P8 je in 2×2 + 1×2).
- **Ein Ort für Bewegung.** Höchstens 1 Hero-Video + 1 kleiner Begleit-Clip gleichzeitig, übrige Kacheln Standbild, Text oder Zahl. Grund: Mehrere parallele Szenen wirkten im Test wie Chaos, nicht wie Vielfalt.
- Kleinste Textkachel 2×2, Halbmodule nur für Bild oder Ruhe. Hochskalierung höchstens 2,0, darüber nur kleine Kachel oder stilisiert.
- **Inhaltlicher Stopp Mo 23.11.** Was fehlt, läuft als gekennzeichneter Platzhalter oder Typo-Kachel.

## Zeitplan
| Tag | Was | Ergebnis |
|---|---|---|
| Do 12.11. | Render-Durchstich Kapitel 3 (V1) in Zielauflösung | erledigt, siehe unten |
| Fr 13.11. | V1+-Raster festlegen, Kapitel 3 bereinigen (7 Objekte, Nr. 20 auf C-D-5) | Raster entschieden |
| Mo 16.11. | Generator `make_kapitel.py` für alle Kapitel, Airtable-Export per Skript, Lichtliste aus der Engine | 8 Kapitel als Vorschau mit Platzhaltern |
| Di 17.11. | KI-Vorauswahl 2–3 Szenen je restlichem Objekt in Airtable; Ton entscheiden | Freigabeliste |
| Mi 18.11. | Test 1:1 (WhiteCube) mit Kapitel 3; Szenenfreigabe durch Björn | Raster und Regeln final |
| Do–Fr 19.–20.11. | Clips schneiden, alle Kapitel bauen; beim Kunden: Rechteliste (Clip, Quelle, URL), Lichtpatch/Hardware; Playout-Rechner, Codec, Player festlegen | Gesamtvorschau |
| Mo 23.11. | Inhaltlicher Stopp, Abnahme-Video an den Kunden | Feedback bis Mi |
| Di–Mi 24.–25.11. | Korrekturen, Gesamtrender kapitelweise über Nacht, Test auf Playout-Rechner mit Lichtplayer | Master v1 |
| Do–Fr 26.–27.11. | Vor Ort: Projektion auf Medienfläche ausrichten, Lichtpatch, Sync-Test über Stunden | läuft vor Ort |
| Sa–So 28.–29.11. | Puffer, einzelne Kapitel neu rendern | Master final |
| Mo 30.11. | Eröffnung | |

## Render-Durchstich 12.11. (Ergebnis)
- Weg: Headless Chrome (Playwright) lädt `preview.html`, pro Bild `ENGINE.seek(t)`, wartet auf dekodierte Videobilder, Screenshot 1680 × 900 × Faktor 2,2857 → ffmpeg H.264.
- Kapitel 3 V1 (Stand 11.11., noch mit Nr. 31): 286 s, 8.582 Bilder bei 30 fps, in 4 Teilen gerendert und verlustfrei zusammengesetzt. Keine hängenden Videobilder.
- Tempo: 0,17–0,32 s pro Bild auf 2 Kernen; zwei Teile parallel ≈ 18 min für das Kapitel. Hochrechnung Gesamtfilm (~30 min): ca. 2 h bei 30 fps, ca. 4 h bei 60 fps auf vergleichbarer Hardware. Teile sind unabhängig, also auf mehrere Rechner verteilbar.
- **Befund: 2057 px Höhe ist ungerade.** H.264/H.265 mit 4:2:0 brauchen gerade Maße. Test mit 3840 × 2058 (eine schwarze Zeile unten). Festwert klären: 2058 oder 2056 px, Lage auf dem Beamerbild (2400 px hoch) beim Einrichten festlegen.
- Offen: Schrift lädt online (für Render lokal einbetten), Interpolation 25 → 30/60 fps, Codec für den Playout-Rechner.

## Offen / zu klären
- Termin Abnahme durch den Kunden.
- Wer liefert Lichthardware und Patch, wer macht Ton/Sounddesign.
- Rechtebestätigung für alle verwendeten Szenen (inkl. Originalton).
