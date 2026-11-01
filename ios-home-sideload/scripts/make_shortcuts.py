#!/usr/bin/env python3
"""Generate native LiveContainer Launch App shortcuts from private device metadata."""
import argparse
import html
import json
from pathlib import Path
import plistlib
import re
import shutil
import subprocess
import tempfile
from urllib.parse import quote, urlencode
import uuid
import unicodedata


def require_string(obj, key):
    value = obj.get(key)
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"Missing/non-string {key}")
    return value


def generate(config, output, sign=False):
    extension = require_string(config, "extension_bundle_id")
    team = require_string(config, "team_id")
    intent = require_string(config, "intent_identifier")
    parameter = require_string(config, "parameter_name")
    scheme = config.get("scheme", "livecontainer")
    if not isinstance(scheme, str) or not re.fullmatch(r"[A-Za-z][A-Za-z0-9+.-]*", scheme):
        raise ValueError("Invalid URL scheme")
    apps = config.get("apps")
    if not isinstance(apps, list) or not apps:
        raise ValueError("apps must be a nonempty array")
    if sign and shutil.which("shortcuts") is None:
        raise ValueError("Apple shortcuts CLI not found; sign on a Mac")
    planned = []
    slugs = set()
    filenames = set()
    for app in apps:
        slug = require_string(app, "slug")
        if not re.fullmatch(r"[a-z0-9][a-z0-9-]*", slug) or slug in slugs:
            raise ValueError("Use unique lowercase filename-safe slugs")
        slugs.add(slug)
        name = require_string(app, "name")
        if any(c in name for c in '/\\:') or any(ord(c) < 32 for c in name) or len(name.encode("utf-8")) > 220:
            raise ValueError("App display name is not a safe download filename")
        filename = unicodedata.normalize("NFC", name).casefold()
        if filename in filenames:
            raise ValueError("App names must be unique for download filenames")
        filenames.add(filename)
        icon = None
        if app.get("icon_path"):
            icon = Path(require_string(app, "icon_path")).expanduser().resolve()
            if not icon.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
                raise ValueError("icon_path must contain an original PNG image")
        folder = require_string(app, "bundle_folder")
        if "/" in folder or "\\" in folder or not folder.endswith(".app"):
            raise ValueError("bundle_folder must be the installed guest .app folder name")
        container = require_string(app, "container_id")
        uuid.UUID(container)  # This helper targets verified standard local UUID containers.
        url = f"{scheme}://livecontainer-launch?" + urlencode({"bundle-name": folder, "container-folder-name": container})
        workflow = {
            "WFWorkflowClientVersion": "3036.0.4", "WFWorkflowClientRelease": "18.0",
            "WFWorkflowMinimumClientVersion": 900, "WFWorkflowMinimumClientVersionString": "900",
            "WFWorkflowName": name,
            "WFWorkflowIcon": {"WFWorkflowIconStartColor": 4282601983, "WFWorkflowIconGlyphNumber": 61440},
            "WFWorkflowTypes": [], "WFWorkflowInputContentItemClasses": [], "WFWorkflowImportQuestions": [],
            "WFWorkflowActions": [{
                "WFWorkflowActionIdentifier": "is.workflow.actions.appintentexecution",
                "WFWorkflowActionParameters": {
                    "AppIntentDescriptor": {"TeamIdentifier": team, "BundleIdentifier": extension,
                                            "Name": "Launch App", "AppIntentIdentifier": intent},
                    parameter: url,
                },
            }],
        }
        planned.append((slug, name, workflow, icon))
    if any((output / f"{name}{suffix}").exists() for _, name, _, _ in planned for suffix in (".shortcut", ".png")) or (output / "index.html").exists():
        raise ValueError("Output files exist; use a fresh output directory")
    output.mkdir(parents=True, exist_ok=True)
    # Validate all metadata before creating files. Never put credential data in config.
    created = []
    try:
        with tempfile.TemporaryDirectory(prefix="lc-shortcuts-") as temp:
            for slug, name, workflow, icon in planned:
                raw = Path(temp) / f"{slug}.shortcut"
                raw.write_bytes(plistlib.dumps(workflow, fmt=plistlib.FMT_BINARY))
                target = output / f"{name}.shortcut"
                created.append(target)
                if sign:
                    subprocess.run(["shortcuts", "sign", "--mode", "anyone", "--input", str(raw), "--output", str(target)],
                                   check=True, capture_output=True, text=True, timeout=180)
                else:
                    shutil.copyfile(raw, target)
                if not target.is_file() or target.stat().st_size == 0:
                    raise ValueError("Shortcut generation produced an empty file")
                if icon:
                    image = output / f"{name}.png"
                    created.append(image)
                    shutil.copyfile(icon, image)
        cards = []
        for _, name, _, icon in planned:
            label = html.escape(name)
            shortcut_name = quote(f"{name}.shortcut", safe="")
            picture = ""
            if icon:
                image_name = quote(f"{name}.png", safe="")
                picture = (f'<img src="{image_name}" alt="{label}">'
                           f'<a href="{image_name}" download="{label}.png">下載原始 App 圖示</a>')
            cards.append(f'<section><h2>{label}</h2>{picture}'
                         f'<a href="{shortcut_name}" download="{label}.shortcut">下載「{label}」捷徑</a></section>')
        links = "".join(cards)
        notice = "下載後打開檔案，確認加入捷徑。先測試一個。" if sign else "未簽署測試檔，請在 Mac 使用 --sign 重新產生後再匯入手機。"
        page = ('<!doctype html><html lang="zh-Hant"><meta charset="utf-8">'
                '<meta name="viewport" content="width=device-width,initial-scale=1"><title>App 直啟捷徑</title>'
                '<style>body{font:18px -apple-system,sans-serif;max-width:480px;margin:auto;padding:24px;line-height:1.6}'
                'a{display:block;padding:16px;margin:12px 0;background:#edf3fc;border-radius:12px}'
                'section{padding:20px;margin:20px 0;border:1px solid #ddd;border-radius:20px}'
                'img{width:96px;height:96px;border-radius:20px}h2{font-size:23px}</style>'
                f'<h1>App 直啟捷徑</h1><p>{notice}</p>{links}'
                '<p>加入主畫面與選原圖示，仍需在手機的捷徑分享選單操作一次。</p></html>')
        (output / "index.html").write_text(page, encoding="utf-8")
    except Exception:
        for target in created:
            target.unlink(missing_ok=True)
        raise
    return len(planned)


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--config", type=Path, required=True)
    p.add_argument("--output-dir", type=Path, required=True)
    p.add_argument("--sign", action="store_true", help="Use Apple shortcuts sign --mode anyone on Mac")
    a = p.parse_args()
    try:
        count = generate(json.loads(a.config.read_text(encoding="utf-8")), a.output_dir, a.sign)
        print(f"Generated {count} {'signed' if a.sign else 'unsigned'} Launch App shortcuts and index.html")
    except (ValueError, OSError, subprocess.SubprocessError) as e:
        p.exit(1, f"Generation failed: {e}\n")


if __name__ == "__main__":
    main()
