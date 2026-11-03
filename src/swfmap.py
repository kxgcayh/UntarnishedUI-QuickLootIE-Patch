#!/usr/bin/env python3
"""Summarise an FFDec swf2xml dump: exported names, sprites, and what each sprite places (char id, instance name, matrix).

usage: python3 -I swfmap.py file.xml
"""
import sys
import xml.etree.ElementTree as ET

root = ET.parse(sys.argv[1]).getroot()
tags = root.find("tags")

names = {}
for t in tags:
    if t.get("type") == "ExportAssetsTag":
        ids = [i.text for i in t.find("tags")] if t.find("tags") is not None else []
        nm = [i.text for i in t.find("names")] if t.find("names") is not None else []
        names.update(dict(zip(ids, nm)))

kinds = {}
for t in tags:
    cid = t.get("characterId") or t.get("spriteId")
    if cid:
        kinds[cid] = t.get("type")


def place(t):
    m = t.find("matrix")
    mat = ""
    if m is not None:
        mat = "tx=%s ty=%s sx=%s sy=%s" % (m.get("translateX"), m.get("translateY"), m.get("scaleX", "1"), m.get("scaleY", "1"))
    return "%s id=%s depth=%s name=%s %s" % (t.get("type").replace("Tag", ""), t.get("characterId"), t.get("depth"), t.get("name"), mat)


for t in tags:
    ty = t.get("type")
    if ty in ("DefineSpriteTag",):
        cid = t.get("spriteId")
        print("SPRITE %s  export=%s  frames=%s" % (cid, names.get(cid), t.get("frameCount")))
        sub = t.find("subTags")
        if sub is None:
            continue
        for s in sub:
            if s.get("type", "").startswith("PlaceObject"):
                cc = s.get("characterId")
                print("    place %s  [%s %s]" % (place(s), kinds.get(cc), names.get(cc)))
    elif ty.startswith("DefineShape") or ty.startswith("DefineEditText") or ty.startswith("DefineText") or ty.startswith("DefineFont"):
        print("%s %s" % (ty, t.get("shapeId") or t.get("characterID") or t.get("fontId") or t.get("characterId")))
