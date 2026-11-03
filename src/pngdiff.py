#!/usr/bin/env python3
"""Max per-channel pixel difference between two non-interlaced 8-bit RGBA PNGs. usage: pngdiff.py a.png b.png"""
import struct, sys, zlib

def load(p):
    d = open(p, "rb").read()
    pos, idat, w = 8, b"", None
    while pos < len(d):
        n, typ = struct.unpack(">I4s", d[pos:pos + 8])
        body = d[pos + 8:pos + 8 + n]
        if typ == b"IHDR":
            w, h, bd, ct, _, _, il = struct.unpack(">IIBBBBB", body)
            assert bd == 8 and ct == 6 and il == 0, (bd, ct, il)
        elif typ == b"IDAT":
            idat += body
        pos += 12 + n
    raw, bpp, stride = zlib.decompress(idat), 4, w * 4
    rows, prev = [], bytearray(stride)
    for y in range(h):
        f, line = raw[y * (stride + 1)], bytearray(raw[y * (stride + 1) + 1:(y + 1) * (stride + 1)])
        for i in range(stride):
            a = line[i - bpp] if i >= bpp else 0
            b = prev[i]
            c = prev[i - bpp] if i >= bpp else 0
            if f == 1: line[i] = (line[i] + a) & 255
            elif f == 2: line[i] = (line[i] + b) & 255
            elif f == 3: line[i] = (line[i] + (a + b) // 2) & 255
            elif f == 4:
                pa, pb, pc = abs(b - c), abs(a - c), abs(a + b - 2 * c)
                line[i] = (line[i] + (a if pa <= pb and pa <= pc else b if pb <= pc else c)) & 255
        rows.append(line); prev = line
    return w, h, rows

a, b = load(sys.argv[1]), load(sys.argv[2])
if a[:2] != b[:2]:
    print("size differs", a[:2], b[:2]); sys.exit(1)
m = max((abs(x - y) for ra, rb in zip(a[2], b[2]) for x, y in zip(ra, rb)), default=0)
print(m)
