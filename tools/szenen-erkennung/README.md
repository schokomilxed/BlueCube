# Szenenerkennung

Automatische Schnitterkennung über die Quellvideos (Medien/Quellen auf der Synology). Ergebnisse sind Vorschläge, keine Freigaben. Die Ergebnisse selbst (JSON, Vorschaubilder) gehören nicht ins Git, nur diese Skripte.

Voraussetzung: Python 3, ffmpeg/ffprobe, `pip install scenedetect` (getestet mit 0.7.3, OpenCV 5.0.0).

Ablauf, in dieser Reihenfolge:
1. `driver.py [Sekunden]` — zerlegt jedes Video in 600-s-Stücke und ruft `detect.py` (PySceneDetect, ContentDetector Schwelle 27, Mindestlänge 0,5 s) auf. Bricht nach dem Zeitbudget ab und macht beim nächsten Aufruf weiter (Zwischenstand in `~/sd/work`).
2. `merge.py` — fügt die Stücke zusammen und schreibt je Video `<Name>.szenen.json` und `.csv` nach `Medien/_szenen/<NN>_<slug>/`.
3. `thumbs.py [Sekunden]` — Mittelbild jeder Szene ab 5 s nach `_szenen/.../thumbs/`.

Hinweis: Pfade sind auf den Aufbau `~/mnt/Blue Cube/Medien` und das Arbeitsverzeichnis `~/sd` eingestellt. Die Skripte legen nur neue Dateien an und verändern keine Quellvideos.
Grenzen: harte Schnitte werden zuverlässig erkannt, Überblendungen und Kamerafahrten nicht.
