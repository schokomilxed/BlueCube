# Kapitel 2 – Fahrdynamik & Sicherheit · Bento-Film + Wand

HTML-Mockup der Medienfläche im Blauen Kubus: ein Bento-Grid-Film für Kapitel 2 und die Wand A · B · C, deren Fachlicht dem Film folgt.

## Dateien

| Datei | Inhalt |
|---|---|
| `choreo.js` | Choreografie: 27 Beats in 6 Momenten, jeder Beat = Folge von Schritten auf dem 7 × 5-Raster der Medienfläche |
| `film.js` / `film.css` | Film-Engine und Inhalte: Kacheltexte, Bilder, Videos, Lesezeit, Effekte (von beiden Vorschauen genutzt) |
| `wand-data.js` | Airtable-Snapshot der Wand: Raster, Medienfläche, Fluchtwegtür, 59 aktive Exponate mit Fach-ID und Maßen |
| `index.html` | Vorschau nur Film |
| `wand.html` | Vorschau Wand + Licht + Film, mit Zoom von der Medienfläche bis zur ganzen Wand |
| `assets/` | Bilder und Clips des Films; `assets/exponate/<Fach-ID>.jpg` = Airtable-Abbildungen (Vorschaugröße) |
| `_build.py` | baut die eigenständigen Dateien `../BlauerKubus_Kapitel2_Fahrdynamik.html` und `../BlauerKubus_Kapitel2_Wand.html` |
| `tools/validate.js` | prüft die Choreografie rechnerisch (siehe unten) |

Die Vorschauen brauchen einen lokalen Webserver, weil sie Assets nachladen; die gebauten Dateien laufen per Doppelklick.

```bash
python3 -m http.server 8732          # im Ordner BentoGridStyle, dann http://localhost:8732/kapitel2/wand.html
python3 kapitel2/_build.py           # eigenständige HTMLs neu bauen (lädt die Schrift Barlow einmalig von Google Fonts)
node kapitel2/tools/validate.js      # Choreografie prüfen, mit --dump zusätzlich Inhalte pro Beat
```

## Regeln

**Raster.** Die Medienfläche hat 7 × 5 Zellen à 80 × 60 cm (560 × 300 cm), in Wand B Spalten g–m, Reihen 2–6. Im Film ist eine Zelle 240 × 180 px groß. Kacheln dürfen bis auf eine Zelle schrumpfen.

**Bewegung.** Kacheln bewegen sich nur horizontal oder vertikal, nie diagonal, und schieben einander. Neue Kacheln wachsen von einer Kante herein (`f` = eingeklappte Parkposition). In `choreo.js` meinen `P1`–`P8` die Positionen des Grundrasters; alle anderen Namen sind Kacheln, die im jeweiligen Moment neu hereinkommen. Freie Kacheln werden automatisch zugeteilt.

**Tempo.** Die Übergänge dauern 0,85 s pro Schritt. Danach steht der Inhalt nach Lesezeit (etwa 3 Wörter pro Sekunde, 4,5–11 s); `hold` in einem Beat überschreibt das.

**Inhalte.** Nur Exponate, die in Airtable auf „Aktiv“ stehen (Lamborghini Carbonteile und Pushrod-Fahrwerk sind deshalb raus).

**Wand.** 35 × 7 Raster (A 8, B 21, C 6 Spalten). Die oberste und die unterste Reihe sind keine Fächer: Sie werden gezeichnet, aber nie einzeln beleuchtet.

## Licht = Film

Das Wandlicht ist rein grafisch: flache Vollflächen pro Fach bzw. Zelle mit weichem Ein- und Ausblenden, ohne Glows, Lichtkegel oder weiche Felder.

- **Fachlicht.** Jede Kachel, die ein Exponat zeigt, schaltet dessen Fach (Tabelle `LIGHT` in `wand.html`). Die Helligkeit ergibt sich aus Gewicht × Kachelgröße × Einblendung; klappt die Kachel weg, verlischt das Licht. Ein Vollbild gibt einen kurzen Impuls.
- **Bewegungslicht.** Jede Kachelbewegung läuft Zelle für Zelle in die Nachbarfächer weiter, mit leicht zufälliger Deckkraft. Seitwärts tritt die Front auf der Seite der Bewegung aus der Medienfläche; auf/ab füllen sich links und rechts die Reihen, die die Kante überstreicht.
- **Weg zum Highlight.** Kommt ein Exponat neu ins Licht, läuft die Füllung von der Medienfläche bis zu seinem Fach; das Fach geht erst bei Ankunft an. Lichtbrücken (`bridge` im Beat) starten beim Ausgangsexponat.

Bedienung `wand.html`: Leertaste Pause, Pfeile Schritt, `0`–`6` Moment, `+`/`−` oder Mausrad Zoom, `i` Bilder, `n` Invertieren, `h` Leiste aus. Standardmäßig läuft die Testschleife M2; der Knopf schaltet aufs ganze Kapitel.

## Daten aktualisieren

`wand-data.js` ist ein Snapshot aus der Airtable-Base „Blauer Kubus“ (Stand 15.10.2026). Ändern sich Layout, Fach-IDs oder der Aktiv-Status, muss er neu gezogen werden. Der Fußabdruck eines Exponats wird wie in `Layout/kubus-live.html` berechnet: zwei größte Maße + Luft, auf 80 × 60 cm aufgerundet.

## Offen

- Kein Bild im Footage für das 911-Windkanalmodell (Strömungsgrafik), die Formel-E-Bremse (Größenvergleich) und den ESVW 1 (typografisch). In Airtable gibt es ein Foto des 911-Windkanalmodells (`assets/exponate/B-B-5.jpg`).
- Bildrechte des Bugatti-, Audi- und Porsche-Materials ungeklärt, nur intern.
- In Airtable steht beim Bugatti Chiron Rekord als Jahr 2005; der Rekord war 2019.
