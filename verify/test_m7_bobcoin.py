"""M7 - Bobcoin ve analytics: tuketimi olc, siniri ayarla, yorumla (reports/)."""

import json
import re

from common import ROOT

RUN_JSON = ROOT / "reports" / "bob-run.json"
NOTES = ROOT / "reports" / "bobcoin-notes.md"


def _read_json_text(path) -> str:
    """UTF-8 (BOM'lu/BOM'suz) ve UTF-16 (Windows PowerShell 5.1 '>' yonlendirmesi) dosyalarini okur."""
    raw = path.read_bytes()
    if raw.startswith((b"\xff\xfe", b"\xfe\xff")):
        return raw.decode("utf-16", errors="replace")
    return raw.decode("utf-8-sig", errors="replace")


def _json_documents(text: str):
    """Tek bir JSON belgesi veya satir basina bir JSON (stream-json) kabul eder."""
    try:
        return [json.loads(text)]
    except json.JSONDecodeError:
        return [json.loads(line) for line in text.splitlines() if line.strip()]


def test_bounded_run_output_saved():
    """reports/bob-run.json: 'bob run --format json' ciktisi gecerli JSON"""
    assert RUN_JSON.exists(), "reports/bob-run.json yok -> bob run --format json ... > reports/bob-run.json"
    text = _read_json_text(RUN_JSON).strip()
    assert len(text) >= 50, "cikti cok kisa; bob run gercekten calisti mi?"
    try:
        docs = _json_documents(text)
    except json.JSONDecodeError as exc:
        raise AssertionError(f"gecerli JSON degil ({exc.msg}); '--format json' kullandiniz mi?") from None
    assert docs, "JSON belgesi yok"


def test_notes_have_real_numbers():
    """reports/bobcoin-notes.md: Bobcoin rakamlari ve kaynaklari (portal / Bobalytics) yazilmis"""
    assert NOTES.exists(), "reports/bobcoin-notes.md yok"
    text = NOTES.read_text(encoding="utf-8", errors="replace")
    low = text.lower()
    assert len(text.strip()) >= 200, "notlar cok kisa (en az ~200 karakter)"
    assert "bobcoin" in low, "'Bobcoin' gecmiyor"
    assert re.search(r"\d+([.,]\d+)?", text), "hicbir rakam yok; gordugunuz degerleri yazin"
    assert any(w in low for w in ("bobalytics", "admin", "portal", "dashboard")), "rakamlari nereden okudugunuzu yazin (portal / Bobalytics)"


def test_notes_explain_budget_decision():
    """Notlar bir butce karari iceriyor (--max-cost / --max-turns / oneri)"""
    low = NOTES.read_text(encoding="utf-8", errors="replace").lower() if NOTES.exists() else ""
    assert any(w in low for w in ("max-cost", "max-turns", "limit", "sinir", "butce", "bütçe", "oneri", "öneri")), (
        "notlarda bir butce/sinir onerisi yok (ornegin: 'bu is icin --max-cost 0.5 yeterli')"
    )
