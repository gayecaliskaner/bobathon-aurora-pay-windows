# Project Documentation Rules (Non-Obvious Only)
- `docs/ENGINEERING-HANDBOOK.md` tüm değişiklikler için bağlayıcıdır; para kuralları için tek kaynak `docs/FEE-POLICY.md`.
- `missions/` görev kartlarıdır; kabul kriterleri `verify/test_m*.py` içindedir ve yalnızca sonuca bakar.
- `services/core` örnek/üretim kodu değil, görevlerin konusu olan kasıtlı hatalı koddur.
- `services/limits/` henüz yoktur; M1 sırasında yazılır (`docs/PRD-limits.md` + `docs/API-SPEC-limits.yaml` tek kaynak).
- `fixtures/` (olay logu, FraudShield SDK, müşteri verisi) çalışma verisidir; `verify/` kaynak taramalarında hariç tutulur.
- `KATILIMCI-KILAVUZU-WINDOWS.html` katılımcı kılavuzudur; `SESSION-NOTES.md` yerel kurulum sorunlarının kaydıdır.
- `.venv/` (uygulama) ve `.venv-tools/` (semgrep) iki ayrı ortamdır.
