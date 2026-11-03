# Untarnished UI - QuickLoot IE Patch: 1.1.3 vs 1.2.0, technical differences

1.1.3 is the last release by HotelKosmos (Nexus 140287), built on QuickLoot IE 3.4.1.
1.2.0 is a port of the same five skins onto QuickLoot IE 4.1.3 (Nexus 120075).
Units in the layout tables are twips (1 px = 20 twips). Evidence tags: MEASURED (checked on the files),
INFERRED (follows from the files, not observed in game).

## 1. Why 1.1.3 does not fit QuickLoot IE 4.x

Each style ships a complete `LootMenuIE.swf`. That file is QuickLoot IE's own menu: its ActionScript 2 code and its
sprites, with the skin artwork applied on top. The archive installs it as `interface/LootMenuIE.swf`, so it replaces
the menu that QuickLoot IE 4.1.3 ships.

The code inside every 1.1.3 SWF is QuickLoot IE 3.4.1's code. Its AS2 bytecode (pcode) is identical to the stock
3.4.1 `LootMenuIE.swf` for all five styles (MEASURED). On a 4.1.3 install the menu therefore runs 3.4.1 code against
the 4.1.3 DLL. The QuickLoot IE authors state that 4.0.0 "makes existing reskins incompatible".

Differences between the 3.4.1 menu (what 1.1.3 contains) and the stock 4.1.3 menu (MEASURED, decompiled AS2):

| area | 3.4.1 / 1.1.3 | 4.1.3 |
|---|---|---|
| `LootMenu.getVersion()` | returns 4 | returns 6 |
| stolen / read icons | `stolenIcon`, `readIcon` | `iconStolen`, `iconRead` |
| enchantment icons | `enchantIcon`, `knownEnchantIcon`, `specialEnchantIcon` | `iconEnchant`, `iconEnchantKnown`, `iconEnchantSpecial` |
| best-in-class icon | none | `iconBest` (`data.bestInClass`) |
| artifact icons | `dbmNew`, `dbmFound`, `dbmDisplayed` | `artifactNew`, `artifactFound`, `artifactDisplayed` |
| collection icons | `compNew`, `compFound` | `compNeeded`, `compCollected`, `compDisplayable`, `compDisplayed`, `compOccupied` |
| icon placement | `_x = left + spacing` | corrects for each icon's own bounds offset (`getBounds(this).xMin - _x`) |
| Inventory Injector | `ProcessEntry(data)` on every update | once per entry, guarded by `data.skyui_itemDataProcessed` |
| settings | none | `systemSettings` object with `overrides` applied by `applyOverrides()` at load and on refresh |
| transparency exclusions | matched by clip reference | matched by clip reference or instance name |
| `InfoBar` | rows at `_y = 0` | rows vertically centred |
| `ItemInfo` | text field hidden | text field auto-sized, constraints unscaled, resized on state change |
| `Button` icon | scaled unconditionally | scaled only when the factor is > 0 |

What this means for 1.1.3 on a 4.1.3 install (INFERRED, not tested in game): the rows have no instances under the 4.1.3
names, so the best-in-class, artifact, collection and the renamed stolen/read/enchant icons cannot appear where 4.1.3
expects them. Whether the 4.1.3 DLL also checks the menu's interface version (4 against 6) was not checked.

## 2. What 1.1.3 changed on top of stock 3.4.1 (the skin itself)

Five items, the same set in every style (MEASURED, swf2xml diff against stock 3.4.1):

**Background** (3.4.1 shape 47, inside the background sprite 48):
- stock: layered black fills with an RGBA(18,18,18,178) panel and a 9-slice scaling grid (splitter 460..10460 x 460..6060)
- style 1: one fill, black at alpha 191 (75%), covering the whole 10920 x 7419 area
- styles 2, 3, 4 and 7: one repeating bitmap fill (`fillStyleType` 0x40). Bitmaps are 546 x 372 px for styles 2, 3 and 4, and
  1138 x 774 px for style 5 (`style7` in 1.1.3). The scaling grid is removed, so the bitmap stretches with the panel instead of 9-slicing.

**Row highlight** (3.4.1 shape 34, 10000 x 800): stock is a solid black rectangle. All styles replace it with a 1 px
(20 twips) white outline and no fill. The shape is byte-identical across the five styles.

**Button art**: the import `skyui/buttonart.swf` becomes `skyui/buttonArtDD.swf`. That file is supplied by Untarnished UI
(and by Dear Diary Dark Mode).

**Layout** (placements inside the `LootMenu` sprite, 3.4.1 sprite 56):

| instance | stock 3.4.1 (x, y) | 1.1.3 (x, y) | other change |
|---|---|---|---|
| background | 0, 0 | 0, -1 | y scale 1.0243835 |
| buttonBar | 0, 7420 | 0, 7510 | |
| itemList | 460, 460 | 460, 560 | |
| title | 500, -1060 | 494, -1064 | scale 0.9 |
| weight | 500, 6640 | 494, 6735 | scale 0.9 |
| valueHeader | 7500, 40 | 7500, 140 | |
| weightHeader | 8500, 40 | 8500, 140 | |
| valuePerWeightHeader | 9500, 40 | 9500, 140 | |
| arrowUp | 860, 260 | 860, 360 | |
| arrowDown | 860, 6260 | 860, 6360 | vertical flip kept |
| infoBar | 4860, 6460 | unchanged | |

Nothing else differs: no code, fonts, text fields or icon artwork.

## 3. What 1.2.0 is

Each 1.2.0 SWF is the **stock QuickLoot IE 4.1.3 `LootMenuIE.swf`** with the five items from section 2 applied to it.
All 4.1.3 code and all 4.1.3 icon sprites are kept exactly as shipped. Characters were re-numbered by FFDec between
versions, so they were mapped as follows:

| item | 3.4.1 id | 4.1.3 id |
|---|---|---|
| background shape | DefineShape3 47 | DefineShape3 50 |
| background sprite (scaling grid owner) | 48 | 51 |
| row highlight shape | DefineShape 34 | DefineShape 37 |
| `LootMenu` sprite | 56 | 59 |
| background bitmap (styles 2/3/4/5) | 79 / 80 / 81 / 82 | 200 (unused in 4.1.3, whose highest id is 81) |

The stock background and highlight shapes are structurally identical in 3.4.1 and 4.1.3 (same bounds, record counts and
colours), so the 1.1.3 replacements drop in unchanged.

**Layout in 1.2.0** (the 1.1.3 offsets applied to the 4.1.3 menu):

| instance | stock 4.1.3 | 1.2.0 | note |
|---|---|---|---|
| background | 20, 0 | 20, -1, y scale 1.0243835 | 4.1.3 places the background at x = 20; kept |
| buttonBar, itemList, title, weight, headers, arrows | as 3.4.1 | as 1.1.3 | the 4.1.3 stock values equal the 3.4.1 stock values |
| infoBar | 3000, 6600 | 3000, 6600 | 4.1.3 moved it from 4860, 6460; 1.1.3 never moved it, so the 4.1.3 placement is kept |

The 4.1.3 `LootMenu` code moves `weight`, `infoBar`, `buttonBar` and `arrowDown` relative to their authored positions,
and resizes the background from its authored height. That logic is unchanged from 3.4.1, so the authored offsets behave
as they did in 1.1.3 (READ, from the decompiled code).

## 4. Verification (MEASURED)

| check | result |
|---|---|
| AS2 bytecode (pcode) of each 1.2.0 SWF vs stock 4.1.3 | identical, all 5 styles (checked before the clipped-fill fix, which changes no code) |
| AS2 bytecode of each 1.1.3 SWF vs stock 3.4.1 | identical, all 5 styles |
| toolchain no-op: stock 4.1.3 through `swf2xml` + `xml2swf` with no edit | byte-identical SWF |
| renders of all sprites not touched by the port (128 per style) vs stock 4.1.3 | pixel-identical, all 5 styles |
| rendered `LootMenu` sprite, 1.2.0 vs 1.1.3 | styles 3, 4: max channel difference 6/255; styles 1, 2, 7: about 50 px differ, the two scroll arrows, which stay at x = 860 while 4.1.3 moved the background 1 px right |
| package contents vs 1.1.3 archive | 5 SWFs, `fomod/info.xml` and the preview images changed; style 5 moved from `style7` to `style5`; `ModuleConfig.xml` unchanged; `QLIE-LICENSE.md`, `docs/` and `source/` added at the archive root (the installer does not install them) |

Not verified: behaviour in game. The SWFs were read back with FFDec, the same tool that wrote them; the bytecode and
pixel comparisons are the checks that do not depend on trusting that read-back.

## 5. Known limitations

- Built against QuickLoot IE 4.1.3 only. Other 4.x versions were not checked.
- The preview images in the installer are new screenshots taken on QuickLoot IE 4.1.3.
- Not addressed from the 1.1.3 comments: misaligned first/last rows. 4.1.3's own `InfoBar`/`ListItemRenderer` changes
  may affect it; not tested.

### Fixed: dark line on the right edge of styles 2 and 5
The 1.1.3 background bitmaps use a repeating, smoothed fill (`fillStyleType` 0x40). Each bitmap covers the panel exactly
once (546 px x 20 twips = 10920 twips), but with smoothing the renderer blends each edge pixel with the opposite edge.
The bitmaps' edge opacity (MEASURED, mean alpha per column):

| style | left column | right column | result of wrapping |
|---|---|---|---|
| 2 | 191 | 0 | dark line on the right edge |
| 3 | 0 | 0 | none |
| 4 | 0 | 0 | none |
| 5 (`style7` in 1.1.3) | 98 | 0 | dark line on the right edge |

Top and bottom rows match in every style, so there is no vertical seam. 1.2.0 switches the fill to clipped, smoothed
(0x41), which clamps the edge pixels instead of wrapping. That is the only change in the SWFs of styles 2 to 5 (one
attribute each, MEASURED). FFDec renders of the background shape, last column alpha before -> after: style 2 at zoom 1.5,
31 -> 0; style 5 at zoom 3 and 4, 14 and 23 -> 0 (MEASURED in FFDec's renderer; not yet checked in game).

## 6. Rebuilding from source

See [BUILDING.md](../BUILDING.md) in the repository: `python3 build.py --fetch-ffdec` downloads JPEXS FFDec 26.4.0
(`ffdec_26.4.0.zip`, sha256 `56ce960aeafc7caf034e2052ba49f878a883f7c7ca690da6eeffca9587b5e4b9`), rebuilds the five SWFs
from the vendored inputs, checks them against the released hashes and packs the FOMOD zip. Per style it runs:

```sh
FFDEC="java -jar /path/to/ffdec.jar"
$FFDEC -swf2xml <QuickLoot IE 4.1.3>/Interface/LootMenuIE.swf stock413.xml
$FFDEC -swf2xml <1.1.3 archive>/interface/styleN/LootMenuIE.swf styleN.xml
python3 src/build_style.py stock413.xml styleN.xml outN.xml
$FFDEC -xml2swf outN.xml interface/styleN/LootMenuIE.swf
```

`src/build_style.py` holds the id mapping and the list of transplanted items. `src/swfmap.py`, `src/shapediff.py` and
`src/pngdiff.py` are the inspection and comparison helpers used for section 4.
