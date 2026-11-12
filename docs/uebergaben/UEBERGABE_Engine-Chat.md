# Übergabe an den Chat „Engine"

Projekt: Blauer Kubus (BlueCube). Aufgabe dieses Chats: aus dem Kapitel-2-Mockup eine datengetriebene Film-Engine machen, in der Choreografie, Inhalte und Look entstehen und getestet werden. Erst Plan zeigen, Björn entscheidet, dann bauen.

## Festwerte
- Medienfläche 560 × 300 cm = 7 × 5 Module à 80 × 60 cm. Beamer Panasonic PT-REQ15 (3840 × 2400, 16:10). Render der Medienfläche 3840 × 2057 px. Master 60 fps, abgeleitet 30 fps.
- Ergebnis ist ein vorgerenderter Film (kein HTML in der Installation). Ein Playout-Rechner spielt ihn synchron zu einer Art-Net-Cueliste. Die Loop-Länge des Films muss zur Cueliste passen (im Repo-README genannt: 272,153 s).
- Richtwert ca. 30 s pro Objekt. Ton, Länge je Kapitel, Codec und Playout-Software sind offen.
- 8 Kundenkapitel, 57 Objekte (Kunden-Nr.). Das Kapitel „Fahrdynamik & Sicherheit" im Mockup ist die alte Story-Nummerierung und ist NICHT Kundenkapitel 2. Beides nicht ohne Rückfrage verknüpfen.

## Was existiert
- Ordner `Blue Cube/BentoGridStyle/kapitel2`: `choreo.js` (27 Beats in 6 Momenten, Schritte auf dem 7 × 5-Raster, eine Kachel bewegt sich pro Schritt nur auf einer Achse, Positionen P1–P8, neue Kacheln fahren aus eingeklappten Kanten ein), `film.js` und `film.css` (Bausteine img, vid, quo, nar, lab, fact, gfx, Lesezeit, Canvas-Effekte), `wand-data.js` (Snapshot Wand, Stand 15.10.), `wand.html` (Wand + Licht + Film), `_build.py` (baut eigenständige HTMLs), `tools/validate.js` (prüft die Choreografie).
- Git-Repo `Documents/_GIT/BlueCube` (Spiegel mit docs/, story/, licht/, tools/). `docs/ARBEITSWEISE.md` beschreibt Datenmodell und Regeln.
- Szenenerkennung ist vollständig gelaufen (48 Videos, 2.366 Szenen, davon 1.072 ab 5 s): `Blue Cube/Medien/_szenen/<NN>_<slug>/` (JSON/CSV mit Von/Bis/Dauer, Vorschaubilder). Alles nur Vorschlag, Rechte nicht geprüft.
- Airtable Base `appd9oVo78FNTrPDd`: Exponate `tbl9POWlpNEFKyFlp`, Medien `tblCalNontccPQ6kp`, Specs `tbla9LSViHl9QFMUZ`, Texte `tblA9TC8t8fHNkCYA`, Szenen `tblrZADeAl29MG8tx` (leer), Beats `tbltwL4X66qWyJJsY`. Verknüpfungen immer über Record-IDs.

## Aufgaben in dieser Reihenfolge
1. Engine kurz bewerten (zehn Zeilen): wie sie funktioniert, wo sie für alle 8 Kapitel nicht mehr taugt (z. B. Beats und Inhalte fest in JS, Kapitel-2-Annahmen, Snapshot statt Datenexport).
2. Architektur vorschlagen: Szenen und Beats als JSON pro Kapitel, ein Exportskript Airtable → JSON (Exponate, Specs, Texte, Szenen), Szenenbibliothek mit Clip-ID, Von/Bis, Loop-Länge, geeigneten Kachelgrößen.
3. Mechanik für mehrere gleichzeitig laufende Szenen auf Kacheln verschiedener Größe entwerfen: Kachelrollen, Beat-Regeln, Ruhe gegen Bewegung, Synchronisation der Loops.
4. Testkapitel durchziehen (siehe unten), Vorschau lauffähig im Ordner BentoGridStyle. Bestehende Dateien nicht überschreiben, neue Dateien oder neuer Unterordner.
5. Erst danach: Render-Weg klären (Frame-Export, Codec), Licht und Cueliste anbinden.

## Testkapitel (von Björn bestätigt)
Kundenkapitel 3 „Aus Hybriden wird Motorsport und Diesel", 7 Objekte (Nr. 14–20; Nr. 31 ist laut Renke nach Kapitel 5 gewandert, siehe ENTSCHEIDUNGEN 11.11.): Nr. 14 Porsche 919 Rekuperator, 15 ID. R, 16 RS Q e-tron, 17 Race Touareg, 18 Stanley, 19 V10 TDI haben Video, Specs und Texte. Nr. 20 (1.9 TDI) hat Bilder, Specs, Texte und ein Video ohne Tonspur und ohne Schnitte (eine Szene). Etwa 3,5 Minuten Film bei 30 s je Objekt.
Platzhalter für fehlende Medien: die Bilder aus dem Feld „Abbildung" in Exponate (Anhänge, alle Objekte haben 2–5 Stück). Sie gelten überall, wo eine Szene fehlt. Platzhalter im Film sichtbar kennzeichnen (z. B. Rahmen oder Marker in der Vorschau), damit sie nicht für Endmaterial gehalten werden. Nicht jedes Bild trägt eine große Kachel: Dateinamen deuten auf kleine Quellen hin (z. B. 650 × 433 px bei Nr. 14), Auflösung prüfen.
Fach-IDs der sieben Objekte für die Lichtanbindung (Stand 11.11.): 14 B-U-2, 15 B-R-3, 16 B-Q-5, 17 C-F-5, 18 B-F-4, 19 C-A-3, 20 C-C-3. Ein Fachtausch bei Nr. 20 ist bei Renke angefragt, deshalb frisch aus Airtable lesen.
Zahlen: Airtable vom 11.11.2026, gezählt wurden verknüpfte Zeilen, nicht deren Freigabe.

## Ton (vorläufige Richtung, Stand 11.11.2026)
- Im Raum gibt es Ton, Annahme Stereo. Richtung: Ambient-Bett je Kapitel oder Register, Effekte zu den Kachel-Übergängen und gelegentlich Originalton aus den Clips. Kein gesprochenes Zitat-Gespräch im Kern; als spätere Ergänzung für einzelne Momente denkbar.
- Die Engine leitet Effekt-Cues aus den Beat-Schritten ab (gleiche Zeitbasis wie Bild und Art-Net-Licht). Pro Szene ein Schalter „Originalton" (ja/nein, Pegel); es ist höchstens eine Szene gleichzeitig hörbar, die übrigen werden abgesenkt.
- 47 von 48 Quellvideos haben eine Tonspur (Stereo-AAC), das 1.9-TDI-Video nicht. Der Originalton ist nicht geprüft (Musik, Sprecher) und rechtlich nicht geklärt. Beim Trimmen der Clips den Ton behalten.
- Offen: Lautsprecherzahl und Pegel, nahtloser Ambient-Loop auf die Filmlänge, Ton im Filmfile oder als eigene Datei im Playout, wer das Sounddesign macht.

## Regeln
- Deutsch, kurz und konkret. Plan vor dem Bauen.
- Nichts Bestehendes überschreiben. Das Cowork-Artifact „blauer-kubus-layout" nicht ohne Björns Freigabe ändern.
- Kundenmaterial vertraulich. Rechte-Feld nicht gepflegt: Szenen nur als Vorschlag, nie als freigegeben. Im Testfilm intern kennzeichnen.
- Objekte mit Kunden-Nr. benennen, nicht mit Fach-ID.
- Zwei Stimmen: Exponate sprechen in Ich-Form, die Erzählerin setzt Klammern.
- Ergebnisse als lauffähige Dateien im Ordner, nicht nur als Code im Chat.

## Offen, nicht in diesem Chat lösen
Renkes Antworten zu vier Fakten-Zeilen, PCCB/PSCB-Nummerierung, Nr. 14 Kundenkapitel, Skoda Eiskratzer, XL1-Leistung in PS oder kW, Klartext für V2H/V2L/V2G, englische Übersetzungen der Texte, Ton.


## Stand 12.11.2026 abends (ersetzt Abweichendes oben)
- Plan bis zur Eröffnung 30.11.: `docs/PLAN_Eroeffnung.md`. V1+ statt Mosaik, „ein Ort für Bewegung", Generator für alle Kapitel, Engine ist einzige Zeitquelle (Loop-Länge 272,153 s ist keine Vorgabe mehr).
- Render-Weg erprobt: `Blue Cube/BentoGridStyle/engine/tools/render.py` (Headless Chrome, Bild für Bild, 3840 × 2058, Teile parallel und verlustfrei zusammensetzbar). 2057 px ist ungerade und für H.264/H.265 4:2:0 ungeeignet.
- **`cut_clips.py` verwirft bisher den Ton.** Clips künftig mit Ton schneiden (AAC/WAV beibehalten, neue Dateien, Bestehendes nicht überschreiben). Nr. 15: Kandidaten aus Quelle 3 (siehe Szenen-Übergabe).
- Ton-Test Kapitel 3: `Blue Cube/BentoGridStyle/engine/_ton_test/` (KI-Bett + KI-Übergänge aus den Beat-Schritten, Originalton nur beim Hero, Bett währenddessen −9 dB). Klänge aus dem ElevenLabs-Free-Plan sind mit `_TEST_free` markiert und dürfen nicht in den Master. Rückmeldung Björn: Weg stimmt; Bewegungen zu vorsichtig vertont, nur der erste Schritt eines Beats klingt. Nächste Version: jeder Schritt mit Klang, Akzent auf der Ankunft; Bett und Effekte aus dem Originalton eines Hero-Exponats des Kapitels abgeleitet (Kapitel 3: ID. R, Übergang zu Diesel offen).
