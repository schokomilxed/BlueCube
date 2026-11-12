# Startprompt für den Chat „Texte" (Ich-Zitate)

Projekt: Blauer Kubus (Future Mobility World, Autostadt Wolfsburg, Atelier Brückner). Stand 11.11.2026. Lies zuerst `docs/START.md`, `docs/ARBEITSWEISE.md` und `docs/ENTSCHEIDUNGEN.md`, falls das Repo erreichbar ist. Die Regeln unten gelten auch ohne Repo. Daten holst du frisch aus Airtable (Base `appd9oVo78FNTrPDd`), nie aus alten Chats.

## Aufgabe
Für jedes Exponat entsteht ein Ich-Zitat: das Exponat spricht in der ersten Person. Es kommt in das Feld **STORY_ICH** (Tabelle Exponate, `tbl9POWlpNEFKyFlp`, Feld `fldmTdbyuUAD7LAuk`, mehrzeiliger Text, derzeit leer). Inhaltlicher Schwerpunkt ist der **Kunden-Text**. Das Zitat muss zum Kundenkapitel und zu den anderen Objekten dieses Kapitels passen und die **Fakten** berücksichtigen.

## Quellen je Objekt (alle in Exponate, wenn nicht anders genannt)
- Kunden-Nr. (`fldzsWZxMEDFYXZ2y`), Titel_DE (`fldmissWfXINStxRr`), Name, Jahr, Kurzbeschreibung, Objektinformation.
- **Kunden-Text** (`fldXaLiUCltBSjPiM`): Hauptquelle für Inhalt und Haltung.
- **Fakten** (`flddAaF2bldW5Fs9V`, Text von Renke): durchgestrichene Zeilen sind bereits in Specs oder Texte übernommen, bleiben aber als Quelle gültig. Dazu die Tabellen **Specs** (`tbla9LSViHl9QFMUZ`) und **Texte** (`tblA9TC8t8fHNkCYA`, Typ Aussage) des Objekts.
- **Kundenkapitel** (`fld5l8gYt6ywMZ031`) und die anderen Mitglieder dieses Kapitels (Kunden-Nr., Titel, Kunden-Text). Filter über das Kundenkapitel, Namen und Nummern frisch lesen.
- **Story — Ausschlüsse** (`fldPEPVoj40sh3aaP`): Begriffe, die nicht vorkommen dürfen. Ein Punkt „." heißt leer.

## Duktus
Vorbild ist das Feld „Story-Baustein (AI) v2" (`fldEOYlj1p8nfOoiE`). Es liefert je Objekt Charakterzug, Konflikt, Ich-Form-Zitat und Beziehung. Der Prompt dieses Feldes ist per API nicht lesbar, Björn kann ihn zeigen. Von dort übernimmst du den Ton, nicht die Struktur. Beispiele:
- ID. R (Nr. 15): „Ich fahre schneller als alle vor mir – und tue es lautlos. Wo anderen die Luft ausgeht, ziehe ich erst richtig an."
- V10 TDI (Nr. 19): „Man erwartete vom Diesel Bescheidenheit – ich lieferte 750 Newtonmeter. Ich habe bewiesen, dass Kraft und Kraftstoffsparen in einem einzigen Block Platz haben."
- Audi Magnetic Ride (Mockup): „Ich fühle jede Unebenheit, bevor du sie spürst. Ein Magnetfeld genügt, und aus weich wird straff – ich bin das Fahrwerk, das mit dir mitdenkt."
- Audi Procon-Ten (Mockup): „Wenn es kracht, ziehe ich mich zurück – nicht aus Feigheit, sondern aus Kalkül."

## Regeln für das Zitat
- Ein Zitat je Objekt, Deutsch, 1–2 Sätze, etwa 15–35 Wörter (Lesezeit auf der Kachel ca. 3 Wörter pro Sekunde, 4,5–11 s).
- Das Exponat spricht. Die Erzählerin ist ein eigener Texttyp und kommt hier nicht vor.
- Zahlen und Behauptungen nur aus Kunden-Text, Fakten oder Specs. Nichts erfinden, keine Superlative ohne Beleg dort.
- Kein Werbepathos. Haltung, Spannung oder Gegensatz tragen das Zitat.
- Das Zitat gehört zum Kapitelthema und steht nicht doppelt im Kapitel: Satzanfänge, Bilder und Motive zwischen den Objekten eines Kapitels variieren (nicht überall „Man erwartete …, ich …").
- Ausschlüsse beachten.

## Vorgehen
1. Zuerst kurz einen Plan zeigen und höchstens zwei Fragen stellen. Björn entscheidet.
2. **Test: Kundenkapitel 3** („Aus Hybriden wird Motorsport und Diesel"), Objekte Nr. 14–20 und 31. Zuerst Nr. 15 und Nr. 19 als Entwurf zeigen und abnehmen lassen, weil dort ein Story-Baustein zum Vergleich vorliegt, dann den Rest des Kapitels.
3. Je Objekt eine Zeile: Kunden-Nr., Titel, tragender Satz aus Kunden-Text oder Fakten, Zitat.
4. In STORY_ICH schreiben erst nach Björns OK. Vorhandenen Inhalt vorher lesen, nichts überschreiben.
5. Danach auf Wunsch in die Tabelle Texte übernehmen: Typ „Ich-Form", Herkunft „KI-Entwurf", Status „Entwurf", Übersetzung EN „fehlt", Text-ID „<Nr> · Ich-Form", Exponat-Link über die Record-ID. Englisch folgt später getrennt.
6. Dann die übrigen Kapitel, jeweils mit Entwurf zur Abnahme.

## Regeln
- Deutsch, kurz und konkret. Plan vor dem Bauen.
- Objekte mit Kunden-Nr. benennen, nicht mit Fach-ID. Kundenkapitel 1–8, nicht die alte Story-Nummerierung.
- Nichts Bestehendes überschreiben oder löschen. Link-Felder nur über Record-IDs schreiben. Feldtypen lassen sich über die API nicht ändern.
- Kundenmaterial vertraulich. Texte bleiben „Entwurf", bis Björn oder der Kunde freigibt.
- Neue Entscheidungen am Ende in `docs/ENTSCHEIDUNGEN.md` eintragen, Björn committet.

## Hinweis zum Datenstand
Die Story-Bausteine in Airtable sind als veraltet markiert und können vom Kunden-Text abweichen. Der Kunden-Text hat Vorrang. Kunden-Nr. 31 steht in Airtable derzeit als „schnellste Nürburgring-Rundenzeit der Geschichte" (Kapitel 3); Namen und Nummern vor dem Schreiben frisch prüfen.

## Stand 12.11.2026
- STORY_ICH ist für alle Objekte mit Kunden-Text gefüllt (Nr. 0–57 außer Nr. 31). Kapitel 3 abgenommen, Rest Entwurf zur Abnahme durch Björn.
- Neue Regeln (Quellen, Kausalität, Rückbezug nur nach hinten) stehen in `docs/ENTSCHEIDUNGEN.md` unter 12.11.2026 und gelten zusätzlich zu den Regeln oben.
- Kapitel 3 umfasst nur Nr. 14–20; Nr. 31 (PCCB) gehört zu Kapitel 5 (siehe ENTSCHEIDUNGEN 11.11.).
- Nächste Schritte: Abnahme der übrigen Kapitel, dann Übernahme in die Tabelle Texte, dann Englisch.

