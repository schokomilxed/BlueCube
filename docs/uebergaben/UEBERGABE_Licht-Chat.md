# Übergabe an den Chat _LICHT · Blauer Kubus

Stand 19.11.2026, von Main. Gilt zusammen mit dem Projekt-Dokument `claude/STAND.md` (bei Widerspruch gilt STAND.md).

## Auftrag
_LICHT verantwortet das Regal-Licht synchron zum Film:
- Cue-Listen aus dem Engine-Stand rechnen (je Arbeitsfassung und am Ende final),
- Lichtplayer und Patch pflegen,
- Licht-Unterlagen für Medienpartner und Lichtintegratoren (Regal-Abwicklung PDF, Cue-Excel, README, Übergabe-PDF).

Entscheidungen zur Lichtgestaltung trifft Björn (über Main). Engine-Dateien (`engine/tools/kino.py`, `build/`, `kapitel/`) nur lesen, Änderungen als „→ Antrag an Engine“ ins Logbuch.

## Regeln (gültig)
- **Ein Kanal je Fach, alle 65 Fächer.** Medienwand ohne Kanal. Ein Fach über mehrere Module leuchtet als Ganzes.
- **6 Fächer ohne Exponat** (B-A-6, B-D-5, B-N-2, B-R-4, C-B-5, C-C-3) laufen wie normale Fächer, aber **ohne Solo-Highlight**. Bewegungslicht und „Weg zum Highlight“ gehen durch sie hindurch. Eigene Zufallsfolge mit Seed `1000 + Kapitelindex`, damit das übrige Licht unverändert bleibt.
- **Ebene 1 Exponatlicht:** EIN 0,8 s (S-Kurve auf 100 %), AUS 1,2 s auf 0 %.
- **Ebene 2 Bewegungslicht:** Impulse 0,18 / 0,14 / 0,65 s, nur auf Wand B neben der Medienwand.
- Die Ebenen werden **HTP** gemischt.
- Ausgabe: 40 Hz, lineare Interpolation; 8 bit (`dim`) oder 16 bit (`dim16`: Grob auf `channel`, Fein auf `channel+1`).
- **Kapitelstarts = Σ(Dauer − 1)**: zwischen den Kapiteln liegt 1 s Kreuzblende (`uebergaenge.py`). Die Kino-Fassung (24 fps, 16.11.) hat eigenes Timing, ihre Cues bleiben getrennt.
- **Der Film ist die Uhr.** Der Player folgt mpv über IPC (`time-pos` alle 2 s, Korrektur ab 40 ms). `light_offset_ms` gleicht Latenz aus.

## Eingänge aus der Engine
- `engine/build/cues_0N_gen.json`: Spot-Cues je Kapitel (`typ` ein/aus, `spot` = Fach).
- `engine/build/moves_0N_gen.json`: Bewegungen je Kapitel, daraus die Wellen.
- `engine/data/gen/faecher.json`: Fachgeometrie (Wand, Spalte, Reihe, b, h, leer).
- `engine/tools/kino.py`: Lichtlogik (`lichtplan`, `wellen`, `regal`, Konstanten `EIN`, `AUS`, `SW`, Medienfläche `MO`). Gehört der Engine.
- Kapitellängen bzw. `kapitelstarts.txt` der jeweiligen Arbeitsfassung.

## Werkzeuge (`Blue Cube/lichtplayer/tools/`, seit 19.11.)
- `events.py`: rechnet `events.json` (Spots und Wellen über den ganzen Film), Test-3-Timing (`DURS` im Kopf).
- `events_kino24.py`: dasselbe für die Kino-Fassung (16.11.).
- `mk_player.py`: aus `events.json` die Cue-CSV (`time_s;fach_id;level`) und die Config.
- `mk_xlsx.py`: erzeugt die Cue-Liste als Excel.
- `mk_pdf.py`: erzeugt die Regal-Abwicklung als PDF. Schrift Barlow liegt in `fonts/`.
- `mk_uebergabe.py`: das Übergabe-PDF an den Medienpartner vom 18.11.
- `player_dim16.py`: Player mit Modus `dim16`. Das Original `lichtplayer/player.py` (4.11.) ist unverändert.
- `README_uebergabe_2026-11-18.md`: README aus dem Partnerpaket.

**Achtung:** Die Pfade in den Skripten zeigen noch auf den Container (`/mnt/user-data/uploads/Blue Cube/…`, `/home/claude/…`). Beim ersten Lauf auf echte Pfade bzw. Argumente umstellen. Die Skripte laufen mit numpy (events), openpyxl (xlsx) und reportlab (pdf).

## Dateien in `Blue Cube/lichtplayer/`
- `patch_2026-11-17.csv`: Platzhalter, Universum 0, Kanal 1–65. Fächer 60–65 sind die ohne Exponat.
- Kino-Fassung: `cues_film_2026-11-16.csv` und `config_film_2026-11-16.json`, dazu `README_film.md`.
- Test-3-Timing (= Partnerpaket 18.11.): `cues_film_test3_2026-11-18.csv` (64 720 Stützpunkte, Loop 1955,900 s) und `config_film_test3_2026-11-18.json`.
- `doku/`: Regal-Abwicklung und Cue-Excel.
- Der Stand vom 4.11. (nur Kapitel-2-Loop) ist unverändert.

## Wer hat was bekommen
- **Medienpartner (18.11., Björn verschickt):** `~/Movies/BlueCube_Kino/BlauerKubus_Uebergabe_Film_Licht_2026-11-18.zip`, Film Test 3 stereo plus Licht auf Test-3-Timing.
- **Steffen (19.11.):** dasselbe Paket, dazu als Referenz die Kino-Datei `Film_kino_4096x2160_24_h265_bewegungslicht_stereo_v2.mp4`.

## Offene Punkte
- Kanalplan, Universen, Ziel-IP, Art-Net oder sACN: Rückmeldung der Integratoren abwarten.
- 8 oder 16 bit (bei 16 bit den Patch neu nummerieren).
- Latenz von Projektor und Dimmer (`light_offset_ms`).
- Grundlicht, Leuchtmittel und Farbtemperatur, Helligkeit des Bewegungslichts.
- Verhalten bei Neustart und Schleife.
- **Endgültige Cues** nach dem inhaltlichen Stopp am 23.11., aus demselben Datenstand wie der Endmaster (3840 × 2057, 60 fps). Format und Spalten bleiben gleich.

## Erste Aufgabe: Cues für HD-Test 4
- Film: `engine/render_tests/test4/Film_test4_1920_mitTon.mp4` (59 984 Bilder bei 30 fps = 1999,47 s). Kapitelstarts in `render_tests/test4/kapitelstarts.txt`.
- Kapitel: `kapitel/0N_grp.json`; Cues in `render_tests/test4/cues/cues_0N_gen.json`.
- Bewegungsdaten: prüfen, ob `moves_0N` zu den `0N_grp`-Kapiteln existieren. Wenn nicht, „→ Antrag an Engine“ (moves-Export für Test 4).
- Ausgabe als neue Dateien `cues_film_test4_2026-11-xx.csv` und `config_film_test4_….json`. Nichts überschreiben.
- Gegenprobe: Spots je Kapitel gegen die Cue-Zahl, Länge gegen die Filmdauer, Stichprobe im Film.
