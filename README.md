# Blauer Kubus – Future Mobility World (Autostadt Wolfsburg)

Arbeitsstand Atelier Brückner. Inhalt des Repos:

| Ordner | Inhalt |
|---|---|
| `story/` | Storyline (`Blauer_Kubus_Storyline.md`), Momentlisten Kapitel 1–4 (v1, noch alte 4-Kapitel-Struktur), Beispiel-Momentslides |
| `docs/` | `Kundenabfolge_vs_unsere_Momente.pdf`: Abgleich der Kunden-Kapitel 1–8 mit unseren 27 Momenten, offene Punkte |
| `mockup/` | HTML-Mockup Kapitel 2 (Wand, Film, Fach-Licht und Wellen), hier ohne eingebettete Medien |
| `licht/lichtplayer/` | Player für Art-Net/sACN: `cues.csv`, `patch.csv`, `config.json`, README |
| `licht/` | Excel-Cueliste (erste Minute), `Lichtvorschau_Cueliste.html` |
| `licht/tools/` | Pipeline Mockup → Cues: `sample2.js` (Aufzeichnung), `bake.py` (Cues), `cues2.py`, `build_xlsx.py` |
| `tools/overview-pdf/` | Bau-Skripte der Abgleich-PDF |

## Lichtplayer in Kürze
`python3 licht/lichtplayer/player.py --dry-run`, Details in `licht/lichtplayer/README.md`.
Loop-Länge 272,153 s (Beats 1–26 des Mockups); der gerenderte Film muss dieselbe Länge haben.

## Nicht im Repo
Kundendateien (Kapitel_1-8_Abfolge), Kundentexte und Airtable-Export (Base "Exponate") – bewusst nicht eingecheckt.
