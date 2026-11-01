#!/usr/bin/env python3
"""Clean an IPA and optionally retain only explicitly named app extensions."""
import argparse
import json
from pathlib import Path, PurePosixPath
import plistlib
import zipfile


def prepare(source, output, keep=None):
    if source.resolve() == output.resolve():
        raise ValueError("Input and output must differ")
    if output.exists():
        raise ValueError("Output already exists; choose a new path")
    with zipfile.ZipFile(source) as src:
        bad = src.testzip()
        if bad:
            raise ValueError(f"Corrupt ZIP entry: {bad}")
        main = []
        extensions = set()
        for item in src.infolist():
            parts = PurePosixPath(item.filename).parts
            if item.filename.startswith("/") or ".." in parts or "\\" in item.filename:
                raise ValueError("Unsafe ZIP path")
            if len(parts) == 3 and parts[0] == "Payload" and parts[1].endswith(".app") and parts[2] == "Info.plist":
                main.append(item.filename)
        if len(main) != 1:
            raise ValueError("Expected exactly one main Payload/*.app/Info.plist")
        root = main[0].rsplit("/", 1)[0]
        for name in src.namelist():
            parts = PurePosixPath(name).parts
            if len(parts) >= 4 and "/".join(parts[:2]) == root and parts[2] == "PlugIns" and parts[3].endswith(".appex"):
                extensions.add(parts[3][:-6])
        if keep is not None and not keep.issubset(extensions):
            raise ValueError(f"Requested extensions missing: {sorted(keep - extensions)}")
        info = plistlib.loads(src.read(main[0]))
        output.parent.mkdir(parents=True, exist_ok=True)
        try:
            with zipfile.ZipFile(output, "x", zipfile.ZIP_DEFLATED) as dst:
                for item in src.infolist():
                    parts = PurePosixPath(item.filename).parts
                    if any(p == "__MACOSX" or p.startswith("._") for p in parts):
                        continue
                    if len(parts) < 2 or "/".join(parts[:2]) != root:
                        continue
                    if keep is not None and len(parts) >= 4 and parts[2] == "PlugIns" and parts[3].endswith(".appex") and parts[3][:-6] not in keep:
                        continue
                    dst.writestr(item, src.read(item.filename))
            with zipfile.ZipFile(output) as dst:
                assert dst.read(main[0]) == src.read(main[0]), "Main Info.plist changed"
                assert dst.testzip() is None, "Output ZIP corrupt"
        except Exception:
            output.unlink(missing_ok=True)
            raise
    return {"bundle_id": info.get("CFBundleIdentifier"), "version": info.get("CFBundleShortVersionString"),
            "kept_extensions": sorted(extensions if keep is None else keep),
            "removed_extensions": sorted(set() if keep is None else extensions - keep),
            "signed_by_script": False}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("source", type=Path)
    p.add_argument("output", type=Path)
    group = p.add_mutually_exclusive_group()
    group.add_argument("--keep-extension", action="append", help="Repeat exact .appex basename without suffix; default keeps all")
    group.add_argument("--remove-all-extensions", action="store_true", help="Diagnostic/basic package only; disables extension features")
    a = p.parse_args()
    keep = set() if a.remove_all_extensions else (set(a.keep_extension) if a.keep_extension is not None else None)
    try:
        print(json.dumps(prepare(a.source, a.output, keep), ensure_ascii=False, indent=2))
    except (ValueError, OSError, zipfile.BadZipFile, plistlib.InvalidFileException) as e:
        p.exit(1, f"Error: {e}\n")


if __name__ == "__main__":
    main()
