# M5 - Bob Findings: bulguları görün, Bob'a düzelttirin

**Süre:** 20 dk | **Bob özelliği:** **Bob Findings** paneli, **Fix with Bob**, `.devsecignore` | **Kontrol:** `./verify/run.sh m5` (Windows: `.\verify\run.ps1 m5`)

## Durum

Canlıya çıkış öncesi pentest sonuçları geldi: [`docs/SECURITY-TICKET-317.md`](../docs/SECURITY-TICKET-317.md) bölüm A.
**Tüm maddeler kapanmadan** canlıya çıkış onayı yok. Bulgular kodda ve altyapı dosyalarında:

| # | Bulgu | Nerede |
|---|---|---|
| A1 | Koda gömülü gizli bilgiler | `services/core/` |
| A2 | SQL injection | `services/core/` |
| A3 | Komut enjeksiyonu ve yol gezintisi | `services/core/` |
| A4 | Docker ve Terraform hataları | `deploy/` |
| A5 | Zafiyetli bağımlılıklar | `deploy/worker/` |

## Hamle 1 - Bulguları görün

**Bob Findings** panelini açın (Bob Security / DevSecOps paketi kuruluysa tarama sürekli çalışır, değilse komut paletinden taramayı başlatın).
Bulguları listeleyin ve risklerine göre sıralayın. Kurulu değilse `./scripts/scan.sh --verbose` (Windows: `.\scripts\scan.ps1 --verbose`) aynı bulguları Semgrep ile gösterir.

## Hamle 2 - Düzelttirin

Bir bulguyu seçip **Fix with Bob** deyin. Bob, bulgu ayrıntılarıyla dolu bir görev başlatır. Sonra kalan bulguları toplu seçerek kapatın.
İşiniz bitince `./scripts/scan.sh` (Windows: `.\scripts\scan.ps1`) **0 bulgu** vermeli.

## Kabul kriteri

- `./verify/run.sh m5` içindeki tüm kontroller PASS (tarama 0 bulgu, sızan gizli bilgi yok, SQL ve komut enjeksiyonu kapalı, Dockerfile ve Terraform sağlam, bağımlılıklar yükseltilmiş)
- Mevcut işlevler bozulmadı: geçerli sorgu ve geçerli arşiv adı hâlâ çalışıyor

## Keşif noktaları

- Bulguları bulmak ile düzeltmek aynı araç mı? Findings paneli hangi kısmı yapıyor, Bob hangisini?
- Bob düzeltirken kodu mu siliyor, yoksa kökten mi çözüyor? (Doğrulayıcı kaynakların silinmesini kabul etmez.)
- `# nosemgrep` ile susturmak neden kabul edilmiyor? Gerçek bir yanlış pozitif için doğru yol `.bob/.devsecignore`'dır. Bu bulgulardan hangisi yanlış pozitif olabilir?
- Gizli bilgiyi ortam değişkenine taşıdığınızda eski değer Git geçmişinde kalır mı?
