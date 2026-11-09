#!/usr/bin/env python3
"""
Lichtplayer Blauer Kubus
Spielt die Fach-Cues (cues.csv) als Art-Net oder sACN ab, loopt und kann sich auf einen
laufenden mpv-Film synchronisieren. Nur Python-Standardbibliothek (Python 3.8+).

  python3 player.py                 Cueliste als Loop abspielen
  python3 player.py --dry-run       nichts senden, nur zeigen was gesendet würde
  python3 player.py --all 0.5       alle Fächer auf 50 % (Anlage testen)
  python3 player.py --chase         Fächer nacheinander kurz anschalten (Patch prüfen)
  python3 player.py --fach A-A-6    ein Fach auf 100 % halten
  python3 player.py --blackout      alle Kanäle 0

Dateien im selben Ordner: config.json, patch.csv, cues.csv
"""
import argparse, bisect, csv, json, os, socket, struct, subprocess, sys, threading, time, uuid

HERE = os.path.dirname(os.path.abspath(__file__))


# ----------------------------------------------------------------------------- Daten
def load_config(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def load_patch(path):
    rows = []
    with open(path, newline="", encoding="utf-8-sig") as f:
        for r in csv.DictReader(f, delimiter=";"):
            fid = (r.get("fach_id") or "").strip()
            if not fid or not (r.get("universe") or "").strip() or not (r.get("channel") or "").strip():
                continue
            mode = (r.get("mode") or "dim").strip().lower()
            col = (r.get("color") or "ffffff").strip().lstrip("#") or "ffffff"
            rows.append(dict(
                fid=fid, universe=int(r["universe"]), channel=int(r["channel"]), mode=mode,
                rgb=tuple(int(col[i:i + 2], 16) / 255.0 for i in (0, 2, 4)),
                max_level=float((r.get("max_level") or "1").replace(",", ".")),
            ))
    return rows


class Cues:
    """Keyframes pro Fach, lineare Interpolation, Zeit in Sekunden."""

    def __init__(self, path):
        tmp = {}
        with open(path, newline="", encoding="utf-8-sig") as f:
            for r in csv.DictReader(f, delimiter=";"):
                tmp.setdefault(r["fach_id"], []).append((float(r["time_s"].replace(",", ".")), float(r["level"].replace(",", "."))))
        self.t, self.v = {}, {}
        for fid, kf in tmp.items():
            kf.sort()
            self.t[fid] = [a for a, _ in kf]
            self.v[fid] = [b for _, b in kf]

    def level(self, fid, t):
        ts = self.t.get(fid)
        if not ts:
            return 0.0
        i = bisect.bisect_right(ts, t)
        if i == 0:
            return self.v[fid][0]
        if i >= len(ts):
            return self.v[fid][-1]
        t0, t1 = ts[i - 1], ts[i]
        v0, v1 = self.v[fid][i - 1], self.v[fid][i]
        return v0 if t1 == t0 else v0 + (v1 - v0) * (t - t0) / (t1 - t0)


# ----------------------------------------------------------------------------- Ausgabe
class ArtNet:
    def __init__(self, cfg):
        c = cfg.get("artnet", {})
        self.target, self.port = c.get("target", "255.255.255.255"), int(c.get("port", 6454))
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.seq = 0

    def packet(self, universe, data):
        n = len(data) + (len(data) & 1)
        data = bytes(data) + b"\x00" * (n - len(data))
        self.seq = self.seq % 255 + 1
        return (b"Art-Net\x00" + struct.pack("<H", 0x5000) + struct.pack(">H", 14) +
                bytes([self.seq, 0]) + struct.pack("<H", universe & 0x7FFF) + struct.pack(">H", n) + data)

    def send(self, universe, data):
        self.sock.sendto(self.packet(universe, data), (self.target, self.port))


class SACN:
    def __init__(self, cfg):
        c = cfg.get("sacn", {})
        self.target, self.port = c.get("target", "multicast"), int(c.get("port", 5568))
        self.priority = int(c.get("priority", 100))
        self.name = c.get("source", "Blauer Kubus")[:63].encode()
        self.cid = uuid.uuid4().bytes
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 4)
        self.seq = 0

    def packet(self, universe, data):
        data = bytes(data)[:512]
        dmp_len = 10 + 1 + len(data)
        frm_len = 77 + dmp_len
        root_len = 22 + frm_len
        self.seq = (self.seq + 1) % 256
        return (struct.pack(">HH", 0x0010, 0) + b"ASC-E1.17\x00\x00\x00" +
                struct.pack(">H", 0x7000 | root_len) + struct.pack(">I", 4) + self.cid +
                struct.pack(">H", 0x7000 | frm_len) + struct.pack(">I", 2) + self.name.ljust(64, b"\x00") +
                bytes([self.priority]) + struct.pack(">H", 0) + bytes([self.seq, 0]) + struct.pack(">H", universe) +
                struct.pack(">H", 0x7000 | dmp_len) + bytes([0x02, 0xA1]) + struct.pack(">HHH", 0, 1, len(data) + 1) +
                b"\x00" + data)

    def send(self, universe, data):
        dest = ("239.255.%d.%d" % (universe >> 8, universe & 255)) if self.target == "multicast" else self.target
        self.sock.sendto(self.packet(universe, data), (dest, self.port))


class DryRun:
    def send(self, universe, data):
        pass


# ----------------------------------------------------------------------------- Video-Takt (mpv IPC)
class MpvClock(threading.Thread):
    """Fragt time-pos von mpv ab (JSON-IPC). Nur lesend, stört den Film nicht."""

    def __init__(self, ipc, interval):
        super().__init__(daemon=True)
        self.ipc, self.interval = ipc, interval
        self.pos, self.stamp, self.ok = None, 0.0, False

    def _open(self):
        if os.name == "nt":
            return open(self.ipc, "r+b", buffering=0), None
        s = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
        s.settimeout(2.0)
        s.connect(self.ipc)
        return s.makefile("rwb", buffering=0), s

    def run(self):
        rid = 0
        while True:
            try:
                f, s = self._open()
                while True:
                    rid += 1
                    t_send = time.perf_counter()
                    f.write((json.dumps({"command": ["get_property", "time-pos"], "request_id": rid}) + "\n").encode())
                    while True:
                        line = f.readline()
                        if not line:
                            raise ConnectionError("mpv closed")
                        msg = json.loads(line)
                        if msg.get("request_id") == rid:
                            break
                    t_recv = time.perf_counter()
                    if msg.get("error") == "success" and msg.get("data") is not None:
                        # Antwort gilt etwa für die Mitte der Anfrage
                        self.pos, self.stamp, self.ok = float(msg["data"]), (t_send + t_recv) / 2, True
                    time.sleep(self.interval)
            except Exception:
                self.ok = False
                time.sleep(1.0)


# ----------------------------------------------------------------------------- Player
def build_frames(patch, level_of, gamma):
    frames = {}
    for p in patch:
        lv = max(0.0, min(1.0, level_of(p["fid"]) * p["max_level"]))
        lv = lv ** gamma if gamma != 1.0 else lv
        buf = frames.setdefault(p["universe"], bytearray(512))
        c = p["channel"] - 1
        if p["mode"] == "rgb":
            for k in range(3):
                if c + k < 512:
                    buf[c + k] = int(round(255 * lv * p["rgb"][k]))
        elif c < 512:
            buf[c] = int(round(255 * lv))
    return frames


def make_output(cfg, dry):
    if dry:
        return DryRun()
    return SACN(cfg) if cfg.get("protocol", "artnet").lower() == "sacn" else ArtNet(cfg)


def run_static(out, patch, cfg, level_of, seconds=None):
    fps = float(cfg.get("fps", 40))
    t_end = None if seconds is None else time.perf_counter() + seconds
    nxt = time.perf_counter()
    try:
        while t_end is None or time.perf_counter() < t_end:
            for u, buf in build_frames(patch, level_of, 1.0).items():
                out.send(u, buf)
            nxt += 1.0 / fps
            time.sleep(max(0.0, nxt - time.perf_counter()))
    except KeyboardInterrupt:
        pass


def run_chase(out, patch, cfg, step=1.0):
    order = [p["fid"] for p in patch]
    fps = float(cfg.get("fps", 40))
    try:
        while True:
            for fid in order:
                print("Fach", fid, flush=True)
                t_end = time.perf_counter() + step
                while time.perf_counter() < t_end:
                    for u, buf in build_frames(patch, lambda f: 1.0 if f == fid else 0.0, 1.0).items():
                        out.send(u, buf)
                    time.sleep(1.0 / fps)
    except KeyboardInterrupt:
        pass


def run_loop(out, patch, cues, cfg, start_at=0.0, max_seconds=None, verbose=True):
    loop_s = float(cfg["loop_s"])
    fps = float(cfg.get("fps", 40))
    gamma = float(cfg.get("gamma", 1.0))
    offset = float(cfg.get("light_offset_ms", 0)) / 1000.0
    vcfg = cfg.get("video", {})
    proc, clock = None, None
    if vcfg.get("launch"):
        proc = subprocess.Popen(vcfg["command"])
    if vcfg.get("ipc"):
        clock = MpvClock(vcfg["ipc"], float(vcfg.get("resync_s", 2.0)))
        clock.start()
    max_drift = float(vcfg.get("max_drift_ms", 40)) / 1000.0
    t_start = time.perf_counter() - start_at
    last_loop, last_sync, nxt, t_run0 = -1, 0.0, time.perf_counter(), time.perf_counter()
    try:
        while True:
            now = time.perf_counter()
            if max_seconds is not None and now - t_run0 > max_seconds:
                break
            # Takt vom Film übernehmen, wenn er bekannt ist und abweicht
            if clock and clock.ok and clock.stamp != last_sync:
                last_sync = clock.stamp
                film_t = (clock.pos + (now - clock.stamp)) % loop_s
                mine = (now - t_start) % loop_s
                d = (film_t - mine + loop_s / 2) % loop_s - loop_s / 2
                if abs(d) > max_drift:
                    t_start -= d
                    if verbose:
                        print("Sync: %+.0f ms Korrektur (Film %.2f s)" % (d * 1000, film_t), flush=True)
            t = (now - t_start + offset)
            loop_no = int(t // loop_s)
            tl = t % loop_s
            if loop_no != last_loop:
                last_loop = loop_no
                if verbose:
                    print("Loop %d gestartet (%s)" % (loop_no + 1, time.strftime("%H:%M:%S")), flush=True)
            for u, buf in build_frames(patch, lambda f: cues.level(f, tl), gamma).items():
                out.send(u, buf)
            nxt += 1.0 / fps
            slp = nxt - time.perf_counter()
            if slp > 0:
                time.sleep(slp)
            else:
                nxt = time.perf_counter()
    except KeyboardInterrupt:
        pass
    finally:
        if proc:
            proc.terminate()


def main():
    ap = argparse.ArgumentParser(description="Lichtplayer Blauer Kubus (Art-Net / sACN)")
    ap.add_argument("--config", default=os.path.join(HERE, "config.json"))
    ap.add_argument("--patch", default=os.path.join(HERE, "patch.csv"))
    ap.add_argument("--cues", default=os.path.join(HERE, "cues.csv"))
    ap.add_argument("--dry-run", action="store_true", help="nichts senden")
    ap.add_argument("--all", type=float, metavar="LEVEL", help="alle Fächer auf LEVEL (0–1) halten")
    ap.add_argument("--fach", metavar="ID", help="ein Fach auf 100 %% halten")
    ap.add_argument("--chase", action="store_true", help="Fächer nacheinander einzeln anschalten")
    ap.add_argument("--blackout", action="store_true")
    ap.add_argument("--start-at", type=float, default=0.0, help="Loop bei Sekunde X beginnen")
    ap.add_argument("--seconds", type=float, help="nach X Sekunden beenden (Test)")
    a = ap.parse_args()

    cfg = load_config(a.config)
    patch = load_patch(a.patch)
    if not patch:
        sys.exit("patch.csv enthält keine Zeilen mit Universum und Kanal.")
    out = make_output(cfg, a.dry_run)
    print("Protokoll %s, %d Fächer gepatcht, %s" % (cfg.get("protocol", "artnet"), len(patch), "DRY-RUN" if a.dry_run else "sende"))
    if a.blackout:
        run_static(out, patch, cfg, lambda f: 0.0, seconds=a.seconds or 1.0)
    elif a.all is not None:
        run_static(out, patch, cfg, lambda f: a.all, seconds=a.seconds)
    elif a.fach:
        run_static(out, patch, cfg, lambda f: 1.0 if f == a.fach else 0.0, seconds=a.seconds)
    elif a.chase:
        run_chase(out, patch, cfg)
    else:
        cues = Cues(a.cues)
        print("Cues für %d Fächer, Loop %.2f s" % (len(cues.t), cfg["loop_s"]))
        run_loop(out, patch, cues, cfg, start_at=a.start_at, max_seconds=a.seconds)


if __name__ == "__main__":
    main()
