#!/usr/bin/env python3
"""Transplant one Untarnished UI style's artwork onto the stock QuickLoot IE 4.1.3 menu.

Works on FFDec swf2xml dumps. The code and the new 4.1.3 icon sprites are never touched; only what the
original patch changed relative to stock 3.4.1 is copied:
  - background shape   3.4.1 DefineShape3 47  -> 4.1.3 shape 50 (+ bitmap fill for styles 2/3/4/5)
  - row highlight      3.4.1 DefineShape  34  -> 4.1.3 shape 37
  - LootMenu layout    3.4.1 sprite 56 placements -> 4.1.3 sprite 59 (same instance names)
  - button art import  skyui/buttonart.swf -> the patch's URL
  - background scaling grid removed where the patch has none (styles 2, 3, 4 and 5)
  - background bitmap fill switched from repeating to clipped (fixes the dark right edge on styles 2 and 5)

usage: build_style.py stock413.xml style_N.xml out.xml
"""
import copy
import sys
import xml.etree.ElementTree as ET

BG_OLD, BG_NEW = "47", "50"
HL_OLD, HL_NEW = "34", "37"
MENU_OLD, MENU_NEW = "56", "59"
GRID_NEW = "51"  # character the 4.1.3 DefineScalingGridTag belongs to (the background sprite)
BITMAP_ID = "200"  # free in 4.1.3 (highest used id is 81)
LAYOUT_NAMES = ["background", "buttonBar", "itemList", "title", "weight",
                "valueHeader", "weightHeader", "valuePerWeightHeader", "arrowUp", "arrowDown"]


def tags_of(root):
    return root.find("tags")


def find(tags, typ, **attr):
    for i, t in enumerate(tags):
        if t.get("type") == typ and all(t.get(k) == v for k, v in attr.items()):
            return i, t
    raise SystemExit("missing %s %r" % (typ, attr))


def find_shape(tags, cid):
    for i, t in enumerate(tags):
        if t.get("type", "").startswith("DefineShape") and t.get("shapeId") == cid:
            return i, t
    raise SystemExit("missing shape %s" % cid)


def sprite_places(sprite):
    return {p.get("name"): p for p in sprite.find("subTags") if p.get("name")}


def main(base_p, style_p, out_p):
    base = ET.parse(base_p)
    style = ET.parse(style_p)
    bt, st = tags_of(base.getroot()), tags_of(style.getroot())

    # 1. shapes
    for old, new in ((BG_OLD, BG_NEW), (HL_OLD, HL_NEW)):
        _, src = find_shape(st, old)
        i, dst = find_shape(bt, new)
        if src.get("type") != dst.get("type"):
            raise SystemExit("shape %s -> %s changes tag type %s -> %s" % (old, new, src.get("type"), dst.get("type")))
        rep = copy.deepcopy(src)
        rep.set("shapeId", new)
        bt[i] = rep

    # 2. bitmap fill (styles 2/3/4/5): add the bitmap under a free id and repoint the fill
    bg_i, bg = find_shape(bt, BG_NEW)
    fills = [f for f in bg.iter("item") if f.get("type") == "FILLSTYLE" and f.get("bitmapId")]
    for f in fills:
        old_bmp = f.get("bitmapId")
        _, bmp = next((i, t) for i, t in enumerate(st) if t.get("type", "").startswith("DefineBits") and t.get("characterID", t.get("characterId")) == old_bmp)
        nb = copy.deepcopy(bmp)
        key = "characterID" if nb.get("characterID") else "characterId"
        nb.set(key, BITMAP_ID)
        f.set("bitmapId", BITMAP_ID)
        # the bitmap covers the panel exactly once; a repeating fill (0x40) wraps the left edge into the right edge
        # under smoothing, the dark line on styles 2 and 5. Clipped (0x41, still smoothed) clamps the edges instead.
        if f.get("fillStyleType") == "64":
            f.set("fillStyleType", "65")
        bt.insert(bg_i, nb)  # definition must precede its first use

    # 3. LootMenu layout
    _, smenu = next((i, t) for i, t in enumerate(st) if t.get("type") == "DefineSpriteTag" and t.get("spriteId") == MENU_OLD)
    _, bmenu = next((i, t) for i, t in enumerate(bt) if t.get("type") == "DefineSpriteTag" and t.get("spriteId") == MENU_NEW)
    sp, bp = sprite_places(smenu), sprite_places(bmenu)
    for n in LAYOUT_NAMES:
        m = copy.deepcopy(sp[n].find("matrix"))
        if n == "background":
            m.set("translateX", bp[n].find("matrix").get("translateX"))  # 4.1.3 sits the background at x=20
        m.set("nTranslateBits", "16")
        old = bp[n].find("matrix")
        idx = list(bp[n]).index(old)
        bp[n].remove(old)
        bp[n].insert(idx, m)

    # 4. button art import
    _, s_imp = find(st, "ImportAssets2Tag")
    _, b_imp = find(bt, "ImportAssets2Tag")
    b_imp.set("url", s_imp.get("url"))

    # 5. scaling grid: removed by the patch for the bitmap styles (2, 3, 4 and 5)
    s_grids = [t for t in st if t.get("type") == "DefineScalingGridTag"]
    b_grids = [t for t in bt if t.get("type") == "DefineScalingGridTag" and t.get("characterId") == GRID_NEW]
    if not s_grids:
        for g in b_grids:
            bt.remove(g)

    base.write(out_p, encoding="UTF-8", xml_declaration=True)


if __name__ == "__main__":
    main(*sys.argv[1:4])
