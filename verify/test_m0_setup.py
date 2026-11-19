"""M0 - Kurulum kontrolleri."""

import importlib
import os
import shutil
import sys

from common import ROOT, run


def test_python_version():
    """Python 3.10 veya uzeri"""
    assert sys.version_info >= (3, 10), f"Python {sys.version_info.major}.{sys.version_info.minor} bulundu, 3.10+ gerekli"


def test_dependencies_installed():
    """Bagimliliklar kurulu (fastapi, pytest, httpx, yaml)"""
    missing = []
    for name in ("fastapi", "pytest", "httpx", "yaml", "pytest_cov"):
        try:
            importlib.import_module(name)
        except ImportError:
            missing.append(name)
    assert not missing, f"eksik paket: {', '.join(missing)}  ->  ./setup.sh calistirin"


def test_core_app_boots():
    """Aurora Core uygulamasi ayaga kalkiyor (/health)"""
    from fastapi.testclient import TestClient

    from services.core.main import app

    response = TestClient(app).get("/health")
    assert response.status_code == 200 and response.json() == {"status": "ok"}, "/health beklenen yaniti vermedi"


def test_repo_has_workshop_files():
    """Gorev dosyalari yerinde (docs, fixtures, deploy)"""
    expected = [
        "docs/PRD-limits.md",
        "docs/API-SPEC-limits.yaml",
        "docs/ENGINEERING-HANDBOOK.md",
        "docs/INCIDENT-2041.md",
        "docs/SECURITY-TICKET-317.md",
        "fixtures/incident/repro.py",
        "fixtures/data/customers.csv",
        "deploy/Dockerfile",
    ]
    missing = [p for p in expected if not (ROOT / p).exists()]
    assert not missing, f"eksik dosya: {', '.join(missing)}"


def test_git_available():
    """Git kurulu ve klasor bir git deposu"""
    assert shutil.which("git"), "git bulunamadi"
    result = run(["git", "rev-parse", "--is-inside-work-tree"])
    assert result.returncode == 0, "bu klasor bir git deposu degil (sablondan olusturdugunuz depoyu klonladiniz mi?)"


def test_semgrep_installed():
    """semgrep kurulu (M5 icin)"""
    # setup.sh / setup.ps1 -Scanners installs semgrep into .venv-tools (same lookup as scripts/scan.py).
    # PATH'e dusmeyin: baska bir klasorun semgrep'i yanlis pozitif verir (Windows dry-run'da goruldu).
    bin_dir, suffix = ("Scripts", ".exe") if os.name == "nt" else ("bin", "")
    candidates = [ROOT / ".venv-tools" / bin_dir / f"semgrep{suffix}", ROOT / ".venv" / bin_dir / f"semgrep{suffix}"]
    if os.name != "nt":
        candidates.append(shutil.which("semgrep"))
    semgrep = next((str(c) for c in candidates if c and os.access(c, os.X_OK)), None)
    ok = semgrep is not None and run([semgrep, "--version"]).returncode == 0
    assert ok, "semgrep yok  ->  ./setup.sh --scanners"


def test_bob_cli_installed():
    """Bob Shell (bob komutu) kurulu (M2 icin)"""
    assert shutil.which("bob"), "'bob' komutu PATH'te yok; facilitator'dan kurulum yonergesini isteyin"
