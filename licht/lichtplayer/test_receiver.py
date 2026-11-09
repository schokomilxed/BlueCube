#!/usr/bin/env python3
"""Mini-Empfänger zum Testen: lauscht auf Art-Net (UDP 6454) oder sACN (UDP 5568) und druckt die Kanäle > 0."""
import socket, struct, sys, time
proto = sys.argv[1] if len(sys.argv) > 1 else "artnet"
port = 6454 if proto == "artnet" else 5568
dur = float(sys.argv[2]) if len(sys.argv) > 2 else 5
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(("", port)); s.settimeout(0.5)
t0 = time.time(); n = 0; last = None
while time.time() - t0 < dur:
    try: d, a = s.recvfrom(1024)
    except socket.timeout: continue
    n += 1
    if proto == "artnet":
        assert d[:8] == b"Art-Net\x00" and struct.unpack("<H", d[8:10])[0] == 0x5000, "kein ArtDmx"
        uni = struct.unpack("<H", d[14:16])[0]; ln = struct.unpack(">H", d[16:18])[0]; data = d[18:18+ln]
    else:
        assert d[4:16] == b"ASC-E1.17\x00\x00\x00", "kein sACN"
        uni = struct.unpack(">H", d[113:115])[0]; cnt = struct.unpack(">H", d[123:125])[0]; data = d[126:126+cnt-1]
    last = (uni, len(data), {i+1: v for i, v in enumerate(data) if v})
print("Pakete:", n, "(%.1f/s)" % (n / dur))
if last: print("Universum", last[0], "Länge", last[1], "aktive Kanäle", len(last[2]), dict(list(last[2].items())[:12]))
