# M8 - GitHub'a teslim: dal, commit, push, PR

**Süre:** 15 dk | **Bob özelliği:** Bob ile **Git iş akışı** (commit mesajı, push, Pull Request) | **Kontrol:** `./verify/run.sh m8` (Windows: `.\verify\run.ps1 m8`)

## Durum

İş bitti. Şimdi ekibin kuralıyla teslim zamanı: [`docs/ENGINEERING-HANDBOOK.md`](../docs/ENGINEERING-HANDBOOK.md) bölüm 6.
Template'ten oluşturduğunuz **kendi GitHub reponuz** (M0) hedef.

## Hamle 1 - Dal ve commit'ler

Bob'a `feature/<kısa-ad>` veya `fix/<kısa-ad>` adında bir dal açtırın. Bugüne kadarki işinizi **anlamlı birkaç commit** halinde kaydettirin
(görev başına bir commit önerilir; mesajlar İngilizce ve ne yaptığını anlatan tek cümle). Çalışma dizini temiz kalmalı.

## Hamle 2 - Push ve Pull Request

Bob'a dalı `origin`'e push ettirin ve **Pull Request** açtırın. Başlık ve açıklamayı Bob, değişikliklere bakarak yazsın;
[`.github/PULL_REQUEST_TEMPLATE.md`](../.github/PULL_REQUEST_TEMPLATE.md) doldurulsun, işaretleyebildiğiniz kutuları işaretleyin.
Bob ilk PR'da GitHub yetkilendirmesi isteyebilir. `gh` kuruluysa onay penceresi olmadan açabilir.

## Kabul kriteri

- `./verify/run.sh m8` içindeki kontroller PASS: feature/fix dalı, temiz çalışma dizini, en az 3 anlamlı commit, dal `origin`'de, açık PR
- `gh` kurulu değilse PR ve CI kontrolleri **manuel** (SKIP) görünür: PR sayfasını facilitator'a gösterin
- PR üzerindeki CI (testler + Semgrep) yeşil

## Keşif noktaları

- Bob `git push` ve `gh pr create` öncesi sizden onay istedi mi? Hangi komutlara "bu görev için onayla" demek mantıklı?
- Commit'leri tek tek mi, hepsini birden mi kaydettirdiniz? Hangisi PR incelemesini kolaylaştırır?
- CI kırmızıysa nedeni Bob'a loglarla birlikte gösterip düzelttirebilir misiniz?
- Push edilen dosyalar arasında olmaması gereken bir şey var mı? (`.bobignore` ve gizli bilgiler)
