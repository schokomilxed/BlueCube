#!/usr/bin/env node
/* Prüft die Grid-Choreografie (choreo.js) rein rechnerisch – ohne Browser.
   Aufruf:  node tools/validate.js [pfad/zu/choreo.js] [--dump]
   Geprüft wird pro Beat und Schritt:
   · jede Kachel bewegt sich nur auf EINER Achse (keine Diagonalen)
   · zu keinem Zeitpunkt überlappen sich sichtbare Kacheln (Bewegung wird in 40 Stufen abgetastet)
   · geparkte Kacheln (f) sind beim Parken wirklich eingeklappt
   · nach jedem Beat ist jede der 7 × 5 Zellen genau einmal belegt, nur ganzzahlige Rechtecke
   · keine sichtbare Kachel ohne Inhalt
   · jede Rückfaltung (reg 'ambient') zeigt exakt das Grundraster von Beat 0
   · das Schleifenende sieht exakt aus wie Beat 0 (unsichtbarer Neustart)
   --dump listet zusätzlich pro Beat, welcher Inhalt in welcher Kachelgröße sichtbar ist. */
const path = require('path');
const arg = process.argv.slice(2).find(a => !a.startsWith('--'));
const file = path.resolve(arg || path.join(__dirname, '..', 'choreo.js'));
const dump = process.argv.includes('--dump');
const { COLS, ROWS, SLOTS, P, BEATS, collapsed } = require(file);

const order = Object.keys(P);
const pos = [...Array(SLOTS)].map((_, i) => i < 8 ? P[order[i]].slice() : [COLS, ROWS, COLS, ROWS]);
const content = Array(SLOTS).fill(null);
const L = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ';
const errs = [], E = (bi, m) => errs.push(`Beat ${bi} (${BEATS[bi].t}): ${m}`);
const lerp = (a, b, t) => a.map((v, i) => v + (b[i] - v) * t);
const thin = r => r[2] - r[0] < 1e-9 || r[3] - r[1] < 1e-9;
const look = () => pos.map((r, i) => collapsed(r) ? null : r.join() + '|' + content[i]).filter(Boolean).sort().join(';');

function overlap(rs, bi, si, t) {
  for (let i = 0; i < rs.length; i++) for (let j = i + 1; j < rs.length; j++) {
    const a = rs[i], b = rs[j]; if (thin(a) || thin(b)) continue;
    const ix = Math.min(a[2], b[2]) - Math.max(a[0], b[0]), iy = Math.min(a[3], b[3]) - Math.max(a[1], b[1]);
    if (ix > 1e-6 && iy > 1e-6) { E(bi, `Schritt ${si} t=${t.toFixed(2)}: Überlappung ${L[i]}${JSON.stringify(a)} / ${L[j]}${JSON.stringify(b)}`); return true; }
  }
  return false;
}

let base = null;
BEATS.forEach((b, bi) => {
  b.steps.forEach((st, si) => {
    for (const x of st) if (x.f) {
      if (!collapsed(pos[x.id])) E(bi, `Schritt ${si}: ${x.name} wird aus sichtbarem Zustand ${JSON.stringify(pos[x.id])} geparkt`);
      if (!collapsed(x.f)) E(bi, `Schritt ${si}: Parkposition von ${x.name} ist nicht eingeklappt`);
      pos[x.id] = x.f.slice();
    }
    const from = pos.map(r => r.slice()), to = pos.map(r => r.slice());
    for (const x of st) {
      to[x.id] = x.r.slice();
      const p = from[x.id], dx = p[0] !== x.r[0] || p[2] !== x.r[2], dy = p[1] !== x.r[1] || p[3] !== x.r[3];
      if (dx && dy && (!collapsed(p) || !collapsed(x.r))) E(bi, `Schritt ${si}: ${x.name} bewegt sich diagonal ${JSON.stringify(p)} → ${JSON.stringify(x.r)}`);
    }
    for (let k = 0; k <= 40; k++) if (overlap(from.map((r, i) => lerp(r, to[i], k / 40)), bi, si, k / 40)) break;
    to.forEach((r, i) => pos[i] = r);
  });
  for (const [id, key] of Object.entries(b.c)) content[id] = key;

  const cov = [...Array(ROWS)].map(() => Array(COLS).fill(0));
  pos.forEach((r, i) => {
    if (collapsed(r)) return;
    if (r.some(v => v !== Math.round(v))) E(bi, `${L[i]} liegt nicht im Raster: ${r}`);
    if (!content[i]) E(bi, `${L[i]} ist sichtbar, aber leer: ${JSON.stringify(r)}`);
    for (let y = r[1]; y < r[3]; y++) for (let x = r[0]; x < r[2]; x++) cov[y][x]++;
  });
  cov.forEach((row, y) => row.forEach((n, x) => { if (n !== 1) E(bi, `Zelle ${x},${y} ist ${n}× belegt`); }));

  if (bi === 0) base = look();
  else if (b.reg === 'ambient' && look() !== base) E(bi, 'Rückfaltung weicht vom Grundraster (Beat 0) ab');

  if (dump) console.log(String(bi).padStart(2), b.t.slice(0, 40).padEnd(40),
    pos.map((r, i) => collapsed(r) ? null : `${content[i]}@${r[2] - r[0]}x${r[3] - r[1]}`).filter(Boolean).join('  '));
});
if (look() !== base) errs.push('Schleife: Endzustand sieht anders aus als Beat 0');

if (errs.length) { console.error(errs.join('\n')); process.exit(1); }
console.log(`OK – ${BEATS.length} Beats, ${BEATS.reduce((n, b) => n + b.steps.length, 0)} Schritte, ${COLS}×${ROWS} Raster`);
