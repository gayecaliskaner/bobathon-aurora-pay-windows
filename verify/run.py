#!/usr/bin/env python3
"""Aurora Pay - gorev dogrulayici.

Kullanim (repo kokunden):
    ./verify/run.sh m1        tek gorev           (Windows: .\\verify\\run.ps1 m1)
    ./verify/run.sh all       tum gorevler (ozet tablo)

Dogrulayici Bob'a ne yazdiginiza bakmaz; yalnizca SONUCA bakar.
"""

from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
MISSIONS = {
    "m0": ("M0 Kurulum", "test_m0_setup.py"),
    "m1": ("M1 Dokumandan koda", "test_m1_limits.py"),
    "m2": ("M2 Uretim hatasi (Bob Shell)", "test_m2_incident.py"),
    "m3": ("M3 Kendi custom mode'um", "test_m3_standards.py"),
    "m4": ("M4 Kapsamli test", "test_m4_tests.py"),
    "m5": ("M5 Bob Findings", "test_m5_findings.py"),
    "m6": ("M6 Bob guvenlik farklari", "test_m6_security.py"),
    "m7": ("M7 Bobcoin ve analytics", "test_m7_bobcoin.py"),
    "m8": ("M8 GitHub teslimat", "test_m8_delivery.py"),
}

if os.name == "nt":
    os.system("")  # Windows konsolunda ANSI renk (VT) destegini acar
GREEN, RED, YELLOW, DIM, RESET = "\033[32m", "\033[31m", "\033[33m", "\033[2m", "\033[0m"
if not sys.stdout.isatty() or os.environ.get("NO_COLOR"):
    GREEN = RED = YELLOW = DIM = RESET = ""


class Collector:
    def __init__(self) -> None:
        self.docs: dict[str, str] = {}
        self.rows: list[tuple[str, str, str]] = []  # (status, title, detail)

    def pytest_itemcollected(self, item):  # noqa: N802
        doc = (item.function.__doc__ or item.name).strip().splitlines()[0]
        self.docs[item.nodeid] = doc

    def pytest_runtest_logreport(self, report):  # noqa: N802
        title = self.docs.get(report.nodeid, report.nodeid)
        if report.when == "call" and report.passed:
            self.rows.append(("PASS", title, ""))
        elif report.skipped:
            reason = report.longrepr[2] if isinstance(report.longrepr, tuple) else str(report.longrepr)
            self.rows.append(("SKIP", title, reason.replace("Skipped: ", "")))
        elif report.failed:
            detail = ""
            crash = getattr(report.longrepr, "reprcrash", None)
            if crash is not None:
                detail = crash.message.replace("AssertionError: ", "").splitlines()[0]
            self.rows.append(("FAIL", title, detail))


def run_mission(key: str) -> dict:
    label, filename = MISSIONS[key]
    collector = Collector()
    print(f"\n=== {label} ===")
    started = time.time()
    code = pytest.main(
        [str(ROOT / "verify" / filename), "-q", "-p", "no:cacheprovider", "-W", "ignore", "--no-header", "-o", "addopts="],
        plugins=[collector],
    )
    grouped: dict[str, dict] = {}
    for status, title, detail in collector.rows:
        g = grouped.setdefault(title, {"PASS": 0, "FAIL": 0, "SKIP": 0, "detail": ""})
        g[status] += 1
        if status in ("FAIL", "SKIP") and not g["detail"]:
            g["detail"] = detail
    for title, g in grouped.items():
        status = "FAIL" if g["FAIL"] else ("SKIP" if g["SKIP"] else "PASS")
        color = {"PASS": GREEN, "FAIL": RED, "SKIP": YELLOW}[status]
        n = g["PASS"] + g["FAIL"] + g["SKIP"]
        suffix = f" ({g['PASS']}/{n})" if n > 1 else ""
        print(f"{color}[{status}]{RESET} {title}{suffix}")
        if g["detail"]:
            print(f"       {DIM}-> {g['detail']}{RESET}")
    passed = sum(1 for r in collector.rows if r[0] == "PASS")
    failed = sum(1 for r in collector.rows if r[0] == "FAIL")
    skipped = sum(1 for r in collector.rows if r[0] == "SKIP")
    total = len(collector.rows)
    if failed == 0 and total > 0 and code in (0, 5):
        verdict = "PASS" if skipped == 0 else "PASS*"
    else:
        verdict = "FAIL"
    color = GREEN if verdict.startswith("PASS") else RED
    extra = f" ({skipped} manuel)" if skipped else ""
    print(f"\n{color}{label}: {verdict}{RESET}  {passed}/{total} kontrol{extra}  [{time.time() - started:.1f}s]")
    return {"mission": key, "verdict": verdict, "passed": passed, "failed": failed, "skipped": skipped, "total": total}


def main(argv: list[str]) -> int:
    if len(argv) != 1 or (argv[0] != "all" and argv[0] not in MISSIONS):
        print("Kullanim: ./verify/run.sh [m0|m1|m2|m3|m4|m5|m6|m7|m8|all]   (Windows: .\\verify\\run.ps1 ...)")
        return 2
    keys = list(MISSIONS) if argv[0] == "all" else [argv[0]]
    results = [run_mission(k) for k in keys]

    out_dir = ROOT / ".verify"
    out_dir.mkdir(exist_ok=True)
    existing = {}
    results_file = out_dir / "results.json"
    if results_file.exists():
        existing = json.loads(results_file.read_text())
    for r in results:
        existing[r["mission"]] = r
    results_file.write_text(json.dumps(existing, indent=2))

    if len(results) > 1:
        print("\n=== OZET ===")
        for r in results:
            color = GREEN if r["verdict"].startswith("PASS") else RED
            print(f"{color}{r['verdict']:<6}{RESET} {MISSIONS[r['mission']][0]:<26} {r['passed']}/{r['total']}")
    return 0 if all(r["verdict"].startswith("PASS") for r in results) else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
