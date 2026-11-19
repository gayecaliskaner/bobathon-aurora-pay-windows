#!/usr/bin/env python3
"""Semgrep ile guvenlik taramasi (Mission 5). Platformdan bagimsiz (macOS, Linux, Windows).

Cikis kodu: 0 = temiz, 1 = bulgu var, 2 = semgrep calistirilamadi.
Kullanim:  python scripts/scan.py            (ozet)
           python scripts/scan.py --verbose  (her bulgu)
semgrep aramasi: .venv-tools -> .venv -> PATH.
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BIN_DIR = "Scripts" if os.name == "nt" else "bin"
EXE_SUFFIX = ".exe" if os.name == "nt" else ""


def find_semgrep() -> str | None:
    for venv in (".venv-tools", ".venv"):
        candidate = ROOT / venv / BIN_DIR / f"semgrep{EXE_SUFFIX}"
        if candidate.is_file() and os.access(candidate, os.X_OK):
            return str(candidate)
    return shutil.which("semgrep")


def main(argv: list[str]) -> int:
    semgrep = find_semgrep()
    if not semgrep:
        print("semgrep bulunamadi.  ->  ./setup.sh --scanners  (Windows: .\\setup.ps1 -Scanners)")
        return 2

    env = {**os.environ, "PYTHONUTF8": "1", "PYTHONIOENCODING": "utf-8"}
    proc = subprocess.run(
        [semgrep, "--config", "security/semgrep-rules.yml", "--metrics=off", "--disable-version-check", "--quiet", "--json", "services", "deploy"],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", env=env, check=False,
    )
    if proc.returncode != 0 and not proc.stdout.strip():
        print(f"semgrep calistirilamadi (cikis kodu {proc.returncode})")
        return 2

    results = json.loads(proc.stdout).get("results", [])
    by_rule: dict[str, list] = {}
    for r in results:
        by_rule.setdefault(r["check_id"].split(".")[-1], []).append(r)
    if "--verbose" in argv:
        for r in results:
            print(f'{r["path"]}:{r["start"]["line"]}  {r["check_id"].split(".")[-1]}')
    print(f"Semgrep bulgu sayisi: {len(results)}")
    for rule, items in sorted(by_rule.items()):
        print(f"  {len(items):>2}  {rule}")
    return 1 if results else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
