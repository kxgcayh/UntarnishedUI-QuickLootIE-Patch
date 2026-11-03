# Building from source

Back to [README.md](README.md). The technical notes are in [docs/TECHNICAL.md](docs/TECHNICAL.md).

This repository holds everything the build reads: the stock QuickLoot IE 4.1.3 menu and the five 1.1.3 style SWFs
(in `vendor/`), the transplant script, the FOMOD and the preview images. You need only Python, Java and FFDec, and
the build can download FFDec itself.

## Platforms

Tested: macOS (arm64), Python 3.15, OpenJDK 27. Expected to work, but not run:

- **Windows:** run `python build.py` from `cmd` or PowerShell (no `bash` or `zip` needed).
- **Linux:** needs `python3` and a Java runtime.

## What you need

| Tool | Where it comes from |
|---|---|
| Python 3 | [python.org](https://www.python.org/downloads/); standard library only |
| Java runtime | any current JRE or JDK, for example [Adoptium Temurin](https://adoptium.net/); `java` must be on `PATH` |
| JPEXS FFDec 26.4.0 | downloaded by `--fetch-ffdec`, or by hand from the [26.4.0 release](https://github.com/jindrapetrik/jpexs-decompiler/releases/tag/version26.4.0) (`ffdec_26.4.0.zip`, sha256 `56ce960aeafc7caf034e2052ba49f878a883f7c7ca690da6eeffca9587b5e4b9`) |

[FFDec](https://github.com/jindrapetrik/jpexs-decompiler) is an open-source Flash decompiler. The build uses its
`-swf2xml` and `-xml2swf` commands to turn a SWF into editable XML and back. **You only need it to rebuild the
patch.** To just use the patch, install the FOMOD zip and skip this file.

The build looks for `ffdec.jar` in this order:

1. `FFDEC_JAR`, if set;
2. `tools/ffdec/ffdec.jar` in this repository, where `--fetch-ffdec` puts it.

`--fetch-ffdec` downloads `ffdec_26.4.0.zip` from the FFDec GitHub release, checks its SHA-256 and refuses it if the
hash differs. Other FFDec versions may write different SWFs; the build then warns (see below).

## Run

```
python3 build.py --fetch-ffdec   # first run: downloads FFDec, then builds and packages
python3 build.py                 # later runs
python3 build.py --skip-build    # repackage the SWFs already in build/pkg (after changing images, docs or fomod)
```

Output: `dist/Quickloot IE - Untarnished UI Patch 1.2.0.zip` (version from `fomod/info.xml`). Intermediate files are
in `build/`.

What the script does:

1. Checks every file in `vendor/` against `inputs.sha256`.
2. Converts the stock 4.1.3 menu and each 1.1.3 style to XML with FFDec.
3. Runs `src/build_style.py` per style: copies the five things the 1.1.3 skin changed (background shape and bitmap,
   row highlight, `LootMenu` layout, button art import, scaling grid) onto the 4.1.3 XML.
4. Converts the result back to `build/pkg/interface/styleN/LootMenuIE.swf`.
5. Compares the five SWFs with `expected.sha256`, the hashes of the released 1.2.0 build.
6. Packs the FOMOD zip: `fomod/`, `images/`, `interface/`, plus `QLIE-LICENSE.md`, `docs/` and `source/` (not installed).

The build stops if:
- a file in `vendor/` is missing or differs from `inputs.sha256`;
- Java or FFDec cannot be found, or the FFDec download has the wrong hash;
- an FFDec or `build_style.py` step fails (for example, an element the script expects is missing).

It only warns if a built SWF differs from `expected.sha256`. That is expected after you change `build_style.py`, and
otherwise means a different FFDec version.

The result is deterministic: the same inputs give byte-identical SWFs, and the zip uses fixed timestamps, so the
same files give a byte-identical zip. You can compare your zip's SHA-256 with the released one.

## Building one style by hand

```
java -jar tools/ffdec/ffdec.jar -swf2xml vendor/qlie-4.1.3/LootMenuIE.swf stock413.xml
java -jar tools/ffdec/ffdec.jar -swf2xml vendor/untarnished-1.1.3/style1/LootMenuIE.swf style1.xml
python3 src/build_style.py stock413.xml style1.xml out1.xml
java -jar tools/ffdec/ffdec.jar -xml2swf out1.xml LootMenuIE.swf
```

## Changing the patch

- What is copied from the 1.1.3 skin, and the character id mapping between 3.4.1 and 4.1.3: the constants at the top
  of `src/build_style.py` (`BG_*`, `HL_*`, `MENU_*`, `GRID_NEW`, `BITMAP_ID`, `LAYOUT_NAMES`). See
  [docs/TECHNICAL.md](docs/TECHNICAL.md) sections 2 and 3.
- Porting to a newer QuickLoot IE: replace `vendor/qlie-4.1.3/LootMenuIE.swf`, update `inputs.sha256`, and check the
  ids with `src/swfmap.py` (lists characters and sprite placements of an XML dump). `src/shapediff.py` lists the
  tags that differ between two dumps. `src/pngdiff.py` compares two PNG renders.
- The installer: `fomod/ModuleConfig.xml` and `fomod/info.xml`, both UTF-16 like the 1.1.3 originals. Keep the
  encoding when editing.
- Preview images: `images/styleN.jpg`, 1600 px wide JPEG.
- After an intended change to the SWFs, update `expected.sha256` from `build/pkg/interface/`.

## Repository layout

```
build.py              Build, checks and packaging
src/                  build_style.py (the transplant) and the inspection helpers
vendor/               The input SWFs, unmodified (sources and terms in vendor/README.md)
inputs.sha256         Hashes of the files in vendor/
expected.sha256       Hashes of the released 1.2.0 SWFs
fomod/                FOMOD info.xml and ModuleConfig.xml shipped in the zip
images/               Installer preview images
docs/                 CHANGELOG and TECHNICAL notes
README.md             What the patch does, install, credits
BUILDING.md           This file
LICENSE               GNU GPL v3
tools/                FFDec, from --fetch-ffdec (not tracked)
build/, dist/         Generated (not tracked)
```
