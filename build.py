#!/usr/bin/env python3
"""Build the Untarnished UI - QuickLoot IE 4.x Patch (see README.md, BUILDING.md, docs/TECHNICAL.md).

Each style is the stock QuickLoot IE 4.1.3 LootMenuIE.swf with the original 1.1.3 patch's artwork applied by
src/build_style.py. FFDec converts the SWFs to XML and back.
Usage: python3 build.py                 (checks inputs, builds the 5 SWFs, packages the FOMOD zip)
       python3 build.py --fetch-ffdec   (first downloads FFDec 26.4.0 into tools/ffdec and checks its hash)
       python3 build.py --skip-build    (packages the SWFs already in build/pkg/interface)
Needs: python3, java, FFDec 26.4.0 (FFDEC_JAR, tools/ffdec/ffdec.jar, or --fetch-ffdec). See BUILDING.md.
"""
import hashlib, os, pathlib, shutil, subprocess, sys, urllib.request, zipfile

HERE = pathlib.Path(__file__).resolve().parent
BUILD = HERE / "build"
PKG = BUILD / "pkg"
STYLES = [1, 2, 3, 4, 5]
STOCK = "vendor/qlie-4.1.3/LootMenuIE.swf"

FFDEC_URL = "https://github.com/jindrapetrik/jpexs-decompiler/releases/download/version26.4.0/ffdec_26.4.0.zip"
FFDEC_SHA256 = "56ce960aeafc7caf034e2052ba49f878a883f7c7ca690da6eeffca9587b5e4b9"
FFDEC_DIR = HERE / "tools" / "ffdec"

# archive layout: (path in zip, source); folders are added as their own entries, as in the 1.1.3 archive
STATIC = [("QLIE-LICENSE.md", "LICENSE"), ("docs/CHANGELOG.md", "docs/CHANGELOG.md"),
          ("docs/TECHNICAL.md", "docs/TECHNICAL.md"), ("fomod/info.xml", "fomod/info.xml"),
          ("fomod/ModuleConfig.xml", "fomod/ModuleConfig.xml")]
STATIC += [(f"source/{p.name}", f"src/{p.name}") for p in sorted((HERE / "src").glob("*.py"))]
STATIC += [(f"images/style{n}.jpg", f"images/style{n}.jpg") for n in STYLES]
ZIP_TIME = (2026, 11, 3, 0, 0, 0)  # fixed, so the same files always give the same zip


def sha(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def read_sums(name):
    return {n.strip(): h for h, n in (line.split(None, 1) for line in (HERE / name).read_text().splitlines() if line.strip())}


def check_inputs():  # the vendored SWFs must be exactly the files the patch was written against
    for name, want in read_sums("inputs.sha256").items():
        p = HERE / name
        if not p.is_file():
            sys.exit(f"missing input {name}")
        if sha(p) != want:
            sys.exit(f"{name} differs from inputs.sha256; restore it with git checkout -- {name}")
    print("inputs match inputs.sha256")


def fetch_ffdec():
    jar = FFDEC_DIR / "ffdec.jar"
    if jar.is_file():
        return
    FFDEC_DIR.mkdir(parents=True, exist_ok=True)
    z = FFDEC_DIR / "ffdec_26.4.0.zip"
    print(f"downloading {FFDEC_URL}")
    urllib.request.urlretrieve(FFDEC_URL, z)
    if sha(z) != FFDEC_SHA256:
        z.unlink()
        sys.exit("downloaded FFDec does not match the expected SHA-256; not using it")
    with zipfile.ZipFile(z) as zf:
        zf.extractall(FFDEC_DIR)
    z.unlink()
    print(f"FFDec 26.4.0 in {FFDEC_DIR}")


def ffdec_cmd():
    if not shutil.which("java"):
        sys.exit("java not found. Install a Java runtime (BUILDING.md).")
    jar = pathlib.Path(os.environ.get("FFDEC_JAR") or FFDEC_DIR / "ffdec.jar")
    if not jar.is_file():
        sys.exit(f"FFDec not found at {jar}. Run with --fetch-ffdec, or set FFDEC_JAR (BUILDING.md).")
    return ["java", "-jar", str(jar)]


def run(cmd):
    r = subprocess.run(cmd, cwd=HERE, stdout=subprocess.DEVNULL)
    if r.returncode:
        sys.exit(f"failed ({r.returncode}): {' '.join(map(str, cmd))}")


def build_swfs():
    ffdec = ffdec_cmd()
    xml = BUILD / "swfxml"
    for d in (xml, PKG):  # only the build's own folders; build/ may hold other work
        shutil.rmtree(d, ignore_errors=True)
    xml.mkdir(parents=True)
    run(ffdec + ["-swf2xml", STOCK, str(xml / "stock413.xml")])
    for n in STYLES:
        print(f"style {n}")
        out = PKG / "interface" / f"style{n}" / "LootMenuIE.swf"
        out.parent.mkdir(parents=True)
        run(ffdec + ["-swf2xml", f"vendor/untarnished-1.1.3/style{n}/LootMenuIE.swf", str(xml / f"style{n}.xml")])
        run([sys.executable, "-I", "src/build_style.py", str(xml / "stock413.xml"), str(xml / f"style{n}.xml"),
             str(xml / f"out{n}.xml")])
        run(ffdec + ["-xml2swf", str(xml / f"out{n}.xml"), str(out)])


def check_outputs():  # a different FFDec or a changed build_style.py gives different SWFs; say so, but go on
    same = True
    for name, want in read_sums("expected.sha256").items():
        p = PKG / name
        if not p.is_file():
            sys.exit(f"missing build/pkg/{name}; run without --skip-build")
        if sha(p) != want:
            same = False
            print(f"warning: {name} differs from the released 1.2.0 build", file=sys.stderr)
    if same:
        print("all SWFs byte-identical to the released build")


def package():
    info = (HERE / "fomod/info.xml").read_bytes().decode("utf-16")  # UTF-16, as in the 1.1.3 installer
    version = info.split("<Version>")[1].split("</Version>")[0].strip()
    files = STATIC + [(f"interface/style{n}/LootMenuIE.swf", str(PKG / f"interface/style{n}/LootMenuIE.swf")) for n in STYLES]
    dist = HERE / "dist"
    dist.mkdir(exist_ok=True)
    out = dist / f"UntarnishedUI-QuickLootIE-Patch-{version}.zip"
    dirs = set()
    with zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zf:
        for arc, src in files:
            parts = arc.split("/")[:-1]
            for i in range(1, len(parts) + 1):
                d = "/".join(parts[:i]) + "/"
                if d not in dirs:
                    dirs.add(d)
                    zd = zipfile.ZipInfo(d, ZIP_TIME)
                    zd.external_attr = (0o40755 << 16) | 0x10  # unix dir mode + MS-DOS directory flag
                    zf.writestr(zd, b"")
            zi = zipfile.ZipInfo(arc, ZIP_TIME)
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            zf.writestr(zi, (HERE / src).read_bytes())
    print(f"{out.relative_to(HERE)}\nsha256 {sha(out)}")


def main(args):
    unknown = set(args) - {"--fetch-ffdec", "--skip-build"}
    if unknown or "-h" in args:
        sys.exit(__doc__)
    check_inputs()
    if "--fetch-ffdec" in args:
        fetch_ffdec()
    if "--skip-build" not in args:
        build_swfs()
    check_outputs()
    package()


if __name__ == "__main__":
    main(sys.argv[1:])
