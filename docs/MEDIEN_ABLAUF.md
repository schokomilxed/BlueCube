# Medien: Beschaffung, Download, Ablage

Stand 11.11.2026. Gilt für den Daten-Strang. Inhalte (Videos, Links-Listen, Logs) liegen auf der Synology, nicht im Git.

## Wo was liegt (Synology, `Blue Cube/Medien`)

| Ort | Inhalt |
|---|---|
| `Quellen/<NN>_<slug>/` | Originale, NN = Kunden-Nr. Unterordner `_original/` für Ausgangsformate (.mov, .wmv), wenn eine MP4-Kopie daneben liegt |
| `Clips/<NN>_<slug>/` | getrimmte Ausschnitte (Von/Bis aus Airtable) |
| `_szenen/<NN>_<slug>/` | Ergebnisse der Szenenerkennung (fps, breite, hoehe je Video) |
| `_additional_input/` | unsortierte Lieferungen von Renke, bis zur Zuordnung |
| `youtube/` | Link-Listen `_links_JJJJ-MM-TT*.txt` und Lauf-Skripte je Download-Lauf (Protokoll) |
| `_jobs.tsv`, `_download_log.txt`, `_JDownloader_*.txt` | Protokoll des Laufs vom 09.11.2026 (alter Ablauf, nur noch Archiv) |

## Ablauf

1. **Links kommen von Renke** in Airtable (Exponate, Feld „Media Links“, Bilder in „Bilder-Medien“) oder per OneDrive („siehe OneDrive“).
   - „Renkes OneDrive“ = geteilte Bibliothek auf Björns Mac: `~/Library/CloudStorage/OneDrive-SharedLibraries-AtelierBruecknerGmbH/Nils Scheffler ATELIER BRÜCKNER - VW_FM-Projectshare/01_Autostadt/Blauer Kubus Medien`. Björn kopiert neue Dateien von dort nach `Medien/_additional_input/<Datum>/`; zugeordnet wird erst danach.
2. **Einlesen:** Automation „Media Links einlesen (KI)“ legt Medien-Zeilen an (Status neu bzw. URL fehlt). Sie liest nur Media Links, nicht Bilder-Medien; Bild-Zeilen legt der Daten-Chat an. Der Abgleich ignoriert Leerzeichen und Zeilenumbrüche, zeigt ohne Link „kein Link – nichts einzulesen“ und springt erst 10 Minuten nach der letzten Änderung auf „neu einlesen“ (vorher „geändert – wartet 10 min“). Erst dann läuft die Automation.
3. **Direkte Dateien ermitteln:** VW-Newsroom- und Audi-Seiten liefern je Seite eine direkte MP4 (meist 720p, `og:video`). Diese URL geht in die Link-Liste. Originale in voller Auflösung (.mov) nur auf Wunsch.
4. **Download** mit yt-dlp auf Björns MacBook (Daten-Chat startet ihn über „Control your Mac“):
   - Werkzeug `~/bin/yt-dlp` (Update: `~/bin/yt-dlp -U`), nicht die Homebrew-Version. `export PATH=$HOME/bin:/opt/homebrew/bin:$PATH` (ffmpeg, deno).
   - Einstellungen `~/Movies/yt-dlp/yt-dlp.conf` (MP4 bis 1080p, Metadaten/Kapitel eingebettet, bei Fehlern weiter).
   - Link-Liste `youtube/_links_JJJJ-MM-TT.txt`, eine URL pro Zeile, `#` für Kommentare (Kunden-Nr., Quellseite).
   - YouTube: `-o '%(title)s [%(id)s].%(ext)s'`. Direkte Dateien: `-o '%(title)s.%(ext)s'` (Dateiname bleibt wie beim Anbieter).
   - Ziel je Objekt mit `-P Quellen/<NN>_<slug>`, immer `--no-overwrites`.
   - Lange Läufe über osascript brechen nach ca. 30 s ab: mit `nohup … > ~/Movies/yt-dlp/last_run.log 2>&1 &` starten, Log in kurzen Abständen prüfen.
5. **Airtable nachziehen:** Status „heruntergeladen“, „Datei lokal“ relativ zu `Medien`, Bildrate, Breite, Höhe (ffprobe). Unter ca. 2200 px Breite im Kommentar „nur klein“ vermerken.
6. **Trimmen** nach Von/Bis → `Clips/`, Status „getrimmt“.
7. **Bericht an Björn:** Tabelle Nr. · Titel · Größe, fehlgeschlagene Links.

## Regeln

- Bot-Prüfung oder Anmeldung bei YouTube nicht umgehen (keine Cookies, keine Tricks): als „blockiert“ markieren, Björn fragen.
- SSL-/Zertifikatsfehler nicht mit `--no-check-certificates` abschalten, erst Björn fragen.
- Originalformate (.wmv, .mov) behalten; MP4-Kopie nur zusätzlich.
- Nichts löschen oder überschreiben. Dubletten nach `_additional_input/_dubletten/`.
- Heruntergeladen heißt nicht freigegeben. Rechte sind nicht geprüft.
