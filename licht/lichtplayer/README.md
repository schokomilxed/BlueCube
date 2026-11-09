# Lichtplayer Blauer Kubus

Spielt die Fach-Beleuchtung (inkl. grober Wellen) als Art-Net oder sACN ab, als Loop, vom Playout-Rechner.
Nur Python 3.8+, keine Zusatzpakete.

## Dateien
- `player.py`    der Player
- `config.json`  Protokoll, Ziel-IP, Loop-Länge, Video-Sync
- `patch.csv`    Fach → Universum / Kanal (hier anpassen, sobald die Hardware feststeht)
- `cues.csv`     Helligkeitsverlauf pro Fach (Zeit in s, Level 0–1), Loop-Länge 272,153 s
- `test_receiver.py`  Mini-Empfänger zum Testen ohne Hardware

## Schnellstart
    python3 player.py --dry-run         Test ohne Senden
    python3 player.py --chase           Fächer einzeln nacheinander (Patch prüfen)
    python3 player.py --all 0.5         alle Fächer 50 %
    python3 player.py                   Cueliste als Loop

## Patch
Standard: Universum 0, Kanal 1–59, ein Kanal pro Fach (mode `dim`). Für RGB-Leuchten `mode` auf `rgb`
setzen (3 Kanäle ab `channel`, Farbe aus `color`). `max_level` begrenzt die Maximalhelligkeit pro Fach.
Ein Universum hat 512 Kanäle, weitere Universen einfach in der Spalte `universe` eintragen.

## Protokoll
`config.json` → `"protocol": "artnet"` (Ziel `artnet.target`, Standard Broadcast, besser die Node-IP)
oder `"sacn"` (Multicast oder Unicast-IP). 40 Bilder/s, Werte linear interpoliert.

## Sync mit dem Film
Loop-Länge des Lichts = 272,153 s = Beats 1–26 des Mockups. Der gerenderte Film muss genau so lang sein.
1. Einfach: Film und Player gleichzeitig starten, beide loopen. Über Stunden driftet das.
2. Sauber (mpv): in `config.json` `video.ipc` auf den mpv-Socket setzen und mpv mit
   `--input-ipc-server=<Pfad>` starten (Windows: `\\.\pipe\mpvsocket`). Der Player liest alle 2 s die
   Filmposition und korrigiert ab 40 ms Abweichung. `video.launch: true` startet mpv gleich mit.
`light_offset_ms` verschiebt das Licht gegenüber dem Film (positiv = Licht früher).
