# AGENTS.md

This file provides guidance to agents when working with code in this repository.

Atölye reposu (Aurora Pay Bobathon). Dokümanlar Türkçe, commit mesajları İngilizce. `services/core` kasıtlı olarak hatalı/güvensiz kod içerir (M2, M5 görevleri): istenmeden düzeltme.

## Komutlar
- Kurulum: `PYTHON=/opt/homebrew/bin/python3.14 ./setup.sh --scanners` (`python3` PATH'te eskiyse `PYTHON` zorunlu; Python 3.10 EOL, kurulmaz).
- Kurulum (Windows / PowerShell): `.\setup.ps1 -Scanners` (Python farklıysa `-Python <yol>`). Windows'ta `python3` Microsoft Store'a yönlendirir: `python` kullanın. Bash betikleri (`*.sh`) PowerShell'de çalışmaz.
- Görev doğrulama (tek görev): `./verify/run.sh m2`. Hepsi: `./verify/run.sh all`. Doğrulayıcı yalnızca sonuca bakar. Windows: `.\verify\run.ps1 m2` / `.\verify\run.ps1 all`.
- Tek test: `.venv/bin/pytest verify/test_m2_incident.py::test_adi -p no:cacheprovider -o addopts=`. Düz `pytest` yalnızca `tests/` altını çalıştırır (`pytest.ini`). Windows: `.venv\Scripts\pytest` (veya `.venv\Scripts\python -m pytest`).
- Kapsam (CI ile aynı): `pytest --cov=services/core --cov-branch --cov-fail-under=85`.
- Güvenlik taraması: `./scripts/scan.sh [--verbose]` (0 = temiz). Windows: `.\scripts\scan.ps1 [--verbose]`. Mantık `scripts/scan.py` içindedir. semgrep `.venv-tools/bin/` (Windows: `.venv-tools\Scripts\`) içindedir, PATH'te değildir; aramayı `.venv-tools` → `.venv` → PATH sırasıyla yapın.
- Lint/format aracı yapılandırılmamış. Mevcut stili koruyun.
- Sunucu: `uvicorn services.core.main:app --host 127.0.0.1` (0.0.0.0 kullanmayın).

## Kod stili ve kurallar (bağlayıcı: `docs/ENGINEERING-HANDBOOK.md`)
- Para: `decimal.Decimal`, `ROUND_HALF_UP`, 2 ondalık. `float` ile para hesabı yok. Ücret tablosu `docs/FEE-POLICY.md`: eşik `1000.00` dahil, düşük oran (%0,25) uygulanır.
- Hatalar tek zarfla döner: `{"error": {"code": "...", "message": "..."}}`. Çıplak `{"detail": ...}`, stack trace veya iç mesaj istemciye gitmez. Kodlar: `VALIDATION_ERROR` 422, `ACCOUNT_NOT_FOUND`/`TRANSFER_NOT_FOUND` 404, `ACCOUNT_ALREADY_EXISTS`/`INSUFFICIENT_FUNDS` 409, `INTERNAL_ERROR` 500 (sabit mesaj: "Beklenmeyen bir hata oluştu").
- Para hareketi atomik: önce doğrula, sonra yaz. `Idempotency-Key` aynı anahtarda ilk yanıtı döner (`store.idempotency`).
- Loglama: `logging` kullanın, `print` yok. PII (ad, IBAN, TCKN, telefon, e-posta, kart) loglanmaz; yalnızca `account_id`, `transfer_id`.
- Güvenlik: sırlar ortam değişkeninden okunur. SQL parametreli olur. Kullanıcı girdisiyle shell komutu yok; dosya adı doğrulanır, `..` yasak. `# nosemgrep` ile susturma kabul edilmez.
- Docker/Terraform: root olmayan kullanıcı, `ADD <url>` yok, gömülü sır yok, `0.0.0.0/0` yok. Bağımlılıklar zafiyetsiz güncel sürümde tutulur.
- Teslimat: dal `feature/<ad>` veya `fix/<ad>`, PR `gh pr create` ile ve `.github/PULL_REQUEST_TEMPLATE.md` doldurularak. CI yeşil olmadan merge yok.

## Testler
- API seviyesinde yazılır: `fastapi.testclient.TestClient`, iç fonksiyonlara bağımlı olmayın.
- Her test dosyasında `@pytest.fixture(autouse=True)` ile `store.reset()` çağrılır. `services/core/store.py::reset()` genel test API'sidir, silmeyin.
- İsim: `test_<davranış>_<koşul>`; Arrange/Act/Assert ayrımı. Her özellik için mutlu yol + negatif durum + sınır değeri.
- `verify/` testleri `from common import ...` kullanır (`verify/common.py`); `verify/` ve `fixtures/` repo kaynak taramalarının dışındadır.

## Yapı
- Servis bellek içidir (`services/core/store.py`, sqlite `:memory:`); kalıcı veritabanı yok.
- M1 yeni servisi `services/limits/main.py` içinde `app` adıyla yazılır; `services/core`'a dokunulmaz, yeni bağımlılık eklenmez (`docs/PRD-limits.md`, `docs/API-SPEC-limits.yaml`).
- `.venv/` ve `.venv-tools/` ayrıdır (semgrep, opentelemetry sürüm çakışması nedeniyle ayrı tutulur).
