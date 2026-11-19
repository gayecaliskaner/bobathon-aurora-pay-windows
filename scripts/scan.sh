#!/usr/bin/env bash
# Semgrep ile guvenlik taramasi (Mission 5). Cikis kodu: 0 = temiz, 1 = bulgu var, 2 = semgrep yok.
# Kullanim:  ./scripts/scan.sh            (ozet)
#            ./scripts/scan.sh --verbose  (her bulgu)
# Mantik platformdan bagimsiz scripts/scan.py icinde (Windows: .\scripts\scan.ps1).
cd "$(dirname "$0")/.." || exit 1
PY=.venv/bin/python
[ -x "$PY" ] || PY=python3
exec "$PY" scripts/scan.py "$@"
