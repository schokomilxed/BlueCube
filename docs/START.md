# Blauer Kubus – Start hier

Jeder neue Chat und jede neue Person liest in dieser Reihenfolge:

1. `docs/ARBEITSWEISE.md` — Ziel, Zielwerte, Kapitelnummerierung, Datenmodell, Regeln.
2. `docs/ENTSCHEIDUNGEN.md` — was entschieden wurde und was noch offen ist. Hat bei Widerspruch Vorrang vor älteren Texten.
3. Die Übergabe des eigenen Strangs in `docs/uebergaben/` (Szenen oder Engine).
4. Daten nie aus alten Chats, sondern frisch aus Airtable holen (Base `appd9oVo78FNTrPDd`).

## Was liegt wo

| Ort | Inhalt |
|---|---|
| Git (dieses Repo) | Entscheidungen, Anweisungen, Regeln, Übergaben, Skripte, Engine-Code, Mockups ohne Medien |
| Synology, Ordner „Blue Cube" | Medien (`Medien/Quellen`, `Medien/Clips`, `Medien/_szenen`), Kundendateien, Layout, Story, freigegebene Stände, gerenderte Filme |
| Airtable | Exponate, Medien, Specs, Texte, Szenen, Beats, Interface „Inhalts- & Medienstatus" |

## Pflege

- Neue Entscheidungen oder Regeln trägt der Chat am Ende in `docs/ENTSCHEIDUNGEN.md` ein (Datum, Entscheidung, Grund). Björn committet.
- Ändert sich ein Festwert (Auflösung, Länge, Codec), wird er in `docs/ARBEITSWEISE.md` angepasst und in `ENTSCHEIDUNGEN.md` vermerkt.
- Übergaben in `docs/uebergaben/` werden bei Stand-Änderungen aktualisiert, nicht neu daneben gelegt.

## Nie ins Git

Videos und Bilder, Kundendateien und Kundentexte, Airtable-Exporte, Ergebnisse der Szenenerkennung, Namen und Mailadressen von Ansprechpartnern des Kunden, Zugangsdaten. Das Repo ist nur für Atelier Brückner gedacht und muss privat bleiben.
