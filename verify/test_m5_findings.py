"""M5 - Bob Findings: SEC-317 A (koda ve altyapiya dair bulgular). Semgrep + Bob Findings paneli."""

import re
import sys

import pytest
from common import ROOT, SECRET_VALUES, read_text, run, source_files
from fastapi.testclient import TestClient

from services.core import config, store
from services.core.main import app

_source_files = source_files


@pytest.fixture
def client():
    store.reset()
    yield TestClient(app, raise_server_exceptions=False)
    store.reset()


# ---- A. Kod ve altyapi bulgulari -------------------------------------------


def test_semgrep_reports_zero_findings():
    """Semgrep taramasi 0 bulgu veriyor (./scripts/scan.sh)"""
    scan = ROOT / "scripts" / "scan.py"
    result = run([sys.executable, str(scan)])
    if result.returncode == 2:
        pytest.fail("semgrep calistirilamadi -> ./setup.sh --scanners", pytrace=False)
    count = re.search(r"bulgu sayisi:\s*(\d+)", result.stdout)
    assert result.returncode == 0, f"{count.group(1) if count else '?'} bulgu kaldi -> ./scripts/scan.sh --verbose"


def test_no_nosemgrep_suppressions():
    """Bulgular '# nosemgrep' ile susturulmamis"""
    offenders = [str(p.relative_to(ROOT)) for p in _source_files(".py", ".tf", ".yml", ".yaml") if "nosemgrep" in read_text(p)]
    assert not offenders, f"susturma bulundu: {offenders}"


def test_no_secrets_left_in_repo():
    """Bilinen gizli degerler repoda yok (kod, Dockerfile, Terraform)"""
    leaks = []
    for path in _source_files():
        if path.suffix in {".pyc", ".csv"} or path.stat().st_size > 500_000 or ".bob" in path.parts or "docs" in path.parts:
            continue
        text = read_text(path)
        leaks += [f"{path.relative_to(ROOT)}: {s[:12]}..." for s in SECRET_VALUES if s in text]
    assert not leaks, f"gizli bilgi hala duruyor: {leaks[:3]}"


def test_secrets_are_read_from_environment(monkeypatch):
    """Gizli bilgiler ortam degiskeninden okunuyor (os.environ)"""
    source = read_text("services/core/config.py")
    assert "os.environ" in source or "os.getenv" in source, "config.py ortam degiskeni kullanmiyor"
    monkeypatch.setenv("AURORA_API_KEY", "from-env-123")
    monkeypatch.setenv("AURORA_JWT_SECRET", "jwt-from-env-123")
    import importlib

    reloaded = importlib.reload(config)
    try:
        values = [str(getattr(reloaded, n, "")) for n in dir(reloaded) if n.isupper()]
        assert any("from-env-123" in v for v in values), "ortam degiskeni degeri config'e yansimiyor (AURORA_API_KEY)"
    finally:
        monkeypatch.undo()
        importlib.reload(config)


def test_sql_injection_is_closed(client):
    """SQL injection kapali: ' OR '1'='1 tum kayitlari getirmiyor"""
    client.post("/accounts", json={"id": "A", "owner_name": "Alice", "iban": "TR1", "balance": 1000})
    client.post("/accounts", json={"id": "B", "owner_name": "Bob", "iban": "TR2", "balance": 0})
    client.post("/transfers", json={"from_account": "A", "to_account": "B", "amount": 10})
    legit = client.get("/reports/transfers", params={"owner": "Alice"})
    assert legit.status_code == 200 and len(legit.json()) == 1, "mesru sorgu artik calismiyor (islevi bozmayin)"
    attack = client.get("/reports/transfers", params={"owner": "x' OR '1'='1"})
    assert attack.json() == [], f"injection calisiyor: {len(attack.json())} kayit sizdi"


@pytest.mark.parametrize("filename", ["x; touch PWNED", "$(touch PWNED)", "../../etc/evil", "a b"])
def test_command_injection_and_traversal_are_closed(client, filename, tmp_path):
    """Komut enjeksiyonu ve yol gezintisi kapali (gecersiz dosya adi reddedilir)"""
    marker = ROOT / "PWNED"
    marker.unlink(missing_ok=True)
    response = client.post("/reports/archive", json={"filename": filename})
    try:
        assert not marker.exists(), "komut calisti: PWNED dosyasi olustu"
        assert response.status_code == 422, f"gecersiz dosya adi 422 ile reddedilmeli, {response.status_code} geldi"
        assert response.json().get("error", {}).get("code") == "VALIDATION_ERROR"
    finally:
        marker.unlink(missing_ok=True)


def test_archive_still_works_for_valid_name(client):
    """Gecerli dosya adiyla arsivleme hala calisiyor"""
    (ROOT / "archives").mkdir(exist_ok=True)
    target = ROOT / "archives" / "q1-2025.tgz"
    target.unlink(missing_ok=True)
    response = client.post("/reports/archive", json={"filename": "q1-2025"})
    try:
        assert response.status_code == 200 and response.json()["exit_code"] == 0, response.text
        assert target.exists(), "arsiv dosyasi olusmadi"
    finally:
        target.unlink(missing_ok=True)


def test_dockerfile_is_hardened():
    """Dockerfile: root degil, ADD <url> yok, imajda gizli bilgi yok"""
    text = read_text("deploy/Dockerfile")
    users = re.findall(r"^\s*USER\s+(\S+)", text, re.M | re.I)
    assert users and users[-1].lower() not in ("root", "0"), "konteyner root olmayan kullanici ile calismali (USER)"
    assert not re.search(r"^\s*ADD\s+https?://", text, re.M | re.I), "ADD <url> kullanilmamali"
    assert not re.search(r"^\s*(ENV|ARG)\s+\w*(TOKEN|SECRET|PASSWORD|KEY)", text, re.M | re.I), "imaja gizli bilgi gomulmus"
    assert "CMD" in text or "ENTRYPOINT" in text, "konteyner baslatma komutu silinmis"


def test_terraform_is_hardened():
    """Terraform: dunyaya acik kural, public bucket, sifresiz/acik DB ve acik parola yok"""
    text = read_text("deploy/terraform/main.tf")
    assert "0.0.0.0/0" not in text, "0.0.0.0/0 hala var"
    assert "public-read" not in text, "bucket herkese acik"
    assert not re.search(r"storage_encrypted\s*=\s*false", text), "depolama sifreleme kapali"
    assert not re.search(r"publicly_accessible\s*=\s*true", text), "veritabani internete acik"
    assert not re.search(r'^\s*password\s*=\s*"', text, re.M), "acik metin parola var (degisken kullanin)"
    assert "aws_db_instance" in text and "aws_security_group" in text, "kaynaklar silinmis; duzeltin, silmeyin"


def test_vulnerable_dependencies_upgraded():
    """deploy/worker/requirements.txt: bilinen zafiyetli surumler yukseltilmis"""
    text = read_text("deploy/worker/requirements.txt").lower()
    minimums = {"requests": (2, 31), "pyyaml": (5, 4), "jinja2": (3, 1), "urllib3": (1, 26, 18)}
    problems = []
    for pkg, minimum in minimums.items():
        line = next((ln for ln in text.splitlines() if ln.strip().startswith(pkg)), None)
        if line is None:
            problems.append(f"{pkg} silinmis")
            continue
        version = re.search(r"(?:==|>=|~=)\s*(\d+(?:\.\d+)*)", line)
        if not version:
            problems.append(f"{pkg}: surum belirtilmemis")
            continue
        parts = tuple(int(x) for x in version.group(1).split("."))
        if parts < minimum[: len(parts)] or parts[:1] < minimum[:1]:
            problems.append(f"{pkg} {version.group(1)} hala zafiyetli (en az {'.'.join(map(str, minimum))})")
    assert not problems, "; ".join(problems)

