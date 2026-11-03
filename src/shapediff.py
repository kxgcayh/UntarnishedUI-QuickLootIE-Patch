#!/usr/bin/env python3
"""List top-level tags (by character id) whose XML differs between two swf2xml dumps. usage: shapediff.py a.xml b.xml"""
import sys, hashlib
import xml.etree.ElementTree as ET

def load(p):
    d = {}
    for i, t in enumerate(ET.parse(p).getroot().find("tags")):
        cid = t.get("shapeId") or t.get("characterID") or t.get("spriteId") or t.get("fontId")
        key = (t.get("type"), cid) if cid else (t.get("type"), "idx%d" % i)
        d[key] = ET.tostring(t)
    return d

a, b = load(sys.argv[1]), load(sys.argv[2])
for k in sorted(set(a) | set(b), key=str):
    if a.get(k) != b.get(k):
        print("CHANGED" if k in a and k in b else ("ADDED" if k in b else "REMOVED"), k, len(a.get(k, b"")), len(b.get(k, b"")))
