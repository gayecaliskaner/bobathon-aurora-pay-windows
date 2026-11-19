# Project Coding Rules (Non-Obvious Only)
- `services/core` kasıtlı olarak hatalı/güvensiz (float para, PII log, SQL/komut enjeksiyonu, gömülü sırlar). Görev dışında dokunmayın; dokunursanız `docs/ENGINEERING-HANDBOOK.md` kurallarına uyun.
- Düzeltmelerde `store.reset()` (`services/core/store.py`) silinmemeli; doğrulayıcı testler kullanır.
- Güvenlik bulgularını `# nosemgrep` ile susturmayın; `./scripts/scan.sh` 0 bulgu vermeli.
- `verify/` testlerini zayıflatmayın veya sonuca göre değiştirmeyin (tek istisna: kurulum ortamı uyumu, bkz. `SESSION-NOTES.md`).
- Tek test: `.venv/bin/pytest verify/<dosya>.py::<test> -p no:cacheprovider -o addopts=` (düz `pytest` yalnızca `tests/` çalıştırır). Windows: `.venv\Scripts\pytest ...`.
- semgrep `.venv-tools/bin/semgrep` içindedir, PATH'te değildir (Windows: `.venv-tools\Scripts\semgrep.exe`; tarama için `.\scripts\scan.ps1`).
- Windows/PowerShell: `*.sh` betikleri çalışmaz; karşılıkları `.\setup.ps1`, `.\verify\run.ps1`, `.\scripts\scan.ps1`. `python3` yerine `python` kullanın.
- Bağımlılık sürümü seçerken güvenlik kuralı: EOL/zafiyetli sürüm önerilmez (Python 3.10 dahil).
