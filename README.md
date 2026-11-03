# Untarnished UI - QuickLoot IE 4.x Patch

HotelKosmos's five [Untarnished UI](https://www.nexusmods.com/skyrimspecialedition/mods/140287) skins for
[QuickLoot IE](https://www.nexusmods.com/skyrimspecialedition/mods/120075), rebuilt on the QuickLoot IE 4.1.3 loot menu.

The original patch (1.1.3) was made for QuickLoot IE 3.4.1 and has no public source. This repository holds the 1.2.0
port, the inputs it is built from, and the scripts that rebuild the release archive from them.

---

## Technical Overview

### Why 1.1.3 does not fit QuickLoot IE 4.x
Each style ships a complete `LootMenuIE.swf`, which replaces QuickLoot IE's own menu. The code inside every 1.1.3 SWF
is QuickLoot IE 3.4.1's: its AS2 bytecode is identical to the stock 3.4.1 menu. QuickLoot IE 4.0 rewrote parts of the
menu and made older reskins incompatible:

| area | 3.4.1 / 1.1.3 | 4.1.3 |
|---|---|---|
| `LootMenu.getVersion()` | 4 | 6 |
| stolen / read icons | `stolenIcon`, `readIcon` | `iconStolen`, `iconRead` |
| enchantment icons | `enchantIcon`, `knownEnchantIcon`, `specialEnchantIcon` | `iconEnchant`, `iconEnchantKnown`, `iconEnchantSpecial` |
| best-in-class icon | none | `iconBest` |
| artifact icons | `dbmNew`, `dbmFound`, `dbmDisplayed` | `artifactNew`, `artifactFound`, `artifactDisplayed` |
| collection icons | `compNew`, `compFound` | `compNeeded`, `compCollected`, `compDisplayable`, `compDisplayed`, `compOccupied` |

### How the port works
The skin itself is only artwork. Against stock 3.4.1, the 1.1.3 SWFs change five things and no code: the background
shape (and its bitmap fill for styles 2, 3, 4 and 5), the row highlight outline, the `LootMenu` layout offsets, the button
art import (`skyui/buttonArtDD.swf`), and the background's scaling grid.

`src/build_style.py` starts from the **stock QuickLoot IE 4.1.3** `LootMenuIE.swf` and copies exactly those items
across, mapping the character ids that changed between versions. All 4.1.3 code and icon sprites stay as shipped.

Checks (details in [docs/TECHNICAL.md](docs/TECHNICAL.md)):
- AS2 bytecode of every built SWF is identical to stock 4.1.3.
- Stock 4.1.3 through the toolchain with no edit comes out byte-identical.
- All 128 sprites the port does not touch render pixel-identical to stock, in every style.

---

## Compatibility

| Mod | Version | Status |
| :--- | :--- | :--- |
| QuickLoot IE | 4.1.3 | Built and checked against this version |
| QuickLoot IE | other 4.x | Not checked |
| QuickLoot IE | 3.x | Use the original 1.1.3 patch instead |

### Prerequisites
- [QuickLoot IE](https://www.nexusmods.com/skyrimspecialedition/mods/120075) 4.1.3 and its requirements (SKSE, SkyUI, ...).
- Untarnished UI or Dear Diary Dark Mode. Either provides `interface/skyui/buttonArtDD.swf`, which the skins load.

---

## Installation

### Via Mod Manager (Recommended)
1. Download `Quickloot IE - Untarnished UI Patch 1.2.0.zip` from the releases.
2. Install it with MO2 or Vortex and pick a style in the installer.
3. Let it overwrite QuickLoot IE, so its `interface/LootMenuIE.swf` wins.

Do not install it alongside the original 1.1.3 patch. It conflicts with any other QuickLoot IE reskin.

### Manual Installation
Copy `interface/styleN/LootMenuIE.swf` for the style you want to `Data/interface/LootMenuIE.swf`.

| installer choice | folder |
|---|---|
| Style 1 | `style1` |
| Style 2 | `style2` |
| Style 3 | `style3` |
| Style 4 | `style4` |
| Style 5 | `style5` |

---

## Building from Source

Anyone can rebuild the release from this repository: it holds the input SWFs, and the build downloads its one tool.
With Python 3 and Java installed:

```
git clone https://github.com/kxgcayh/UntarnishedUI-QuickLootIE-Patch.git
cd UntarnishedUI-QuickLootIE-Patch
python3 build.py --fetch-ffdec
```

The build checks that the five SWFs are byte-identical to the released ones and writes
`dist/Quickloot IE - Untarnished UI Patch 1.2.0.zip`. Details, other platforms and how to change the patch:
[BUILDING.md](BUILDING.md).

---

## Known Issues
- Not fixed from the 1.1.3 comments: a dark line on the right edge of styles 2 and 5.
- Misaligned first/last rows were reported on 1.1.3; QuickLoot IE 4.1.3's own `InfoBar` changes may affect this.

---

## Credits & License

- **HotelKosmos**: the original [Untarnished UI QuickLoot IE patch](https://www.nexusmods.com/skyrimspecialedition/mods/140287) and all five skins.
- **AtomCrafty**: the reskin the original patch was based on; co-author of QuickLoot IE.
- **Miss Corruption, AtomCrafty and Faen**: [QuickLoot IE](https://www.nexusmods.com/skyrimspecialedition/mods/120075), whose menu this file contains.
- **Untarnished UI** by its author, for the button art the skins use.
- **kxgcayh** (Nexus: kautsaralbaa): port to QuickLoot IE 4.1.3, build scripts and release packaging.

QuickLoot IE is licensed under the GNU GPL v3, and every SWF here is a modified QuickLoot IE menu, so this project is
released under the same license. See [LICENSE](LICENSE). The original patch's Nexus permissions allow modification,
release of fixes and asset use; not for sale.
