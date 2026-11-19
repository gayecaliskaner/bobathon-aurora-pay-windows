# M7 - Bobcoin, Bob Admin ve Bobalytics: harcamayı görün

**Süre:** 15 dk | **Bob özelliği:** **Bobcoin** tüketimi, **Bob Admin** portalı, **Bobalytics**, `--max-cost` | **Kontrol:** `./verify/run.sh m7`

## Durum

Ekip lideri Bob'u tüm ekibe açmak istiyor ama CFO soruyor: "Bu iş bize kaça mal oluyor, nereden izleyeceğiz?"
Bu görev kod değil, **ölçüm ve karar** görevi.

## Hamle 1 - Sınırlı bir iş çalıştırın ve ölçün

Küçük bir işi (ör. `services/core`'daki bir modülü açıklatmak) Bob Shell ile **maliyet ve tur sınırı koyarak**, çıktıyı JSON alarak çalıştırın:

```bash
bob run --format json --max-cost <bobcoin> --max-turns <n> "<küçük bir iş>" > reports/bob-run.json
```

Windows PowerShell 5.1'de `>` yönlendirmesi dosyayı UTF-16 yazabilir. Bunun yerine `bob run --format json ... | Out-File -Encoding utf8 reports\bob-run.json` kullanın (doğrulayıcı UTF-8 ve UTF-16'yı kabul eder, diğer araçlar için UTF-8 daha güvenlidir).

Çıktıdaki `stats` bölümünde işin kaç tur sürdüğüne ve ne kadar tüketildiğine bakın. Aynı işi sınırı değiştirerek bir kez daha deneyin.

## Hamle 2 - Portaldan ve Bobalytics'ten okuyun, karar yazın

Bob Admin portalında (`bob.ibm.com/admin`) kendi **kalan bakiyenize ve kullanım detayına** bakın.
Yetkiniz varsa **Bobalytics**'te **Metrics** sekmesine (Adoption, Bob factor, Bobcoin spend) ve **Insights**'a bakın.
Yetkiniz yoksa facilitator ekranını paylaşır. Gördüklerinizi `reports/bobcoin-notes.md` dosyasına yazın:

- Gördüğünüz **rakamlar** ve nereden okuduğunuz (portal / Bobalytics)
- Bu iş için hangi `--max-cost` / `--max-turns` değerini **öneriyorsunuz** ve neden

## Kabul kriteri

- `./verify/run.sh m7` içindeki tüm kontroller PASS (`reports/bob-run.json` geçerli JSON, `reports/bobcoin-notes.md` gerçek rakamlar ve bir bütçe önerisi içeriyor)

## Keşif noktaları

- Bobcoin neye göre tükeniyor? Uzun bir sohbetle yeni açılmış bir sohbet arasında fark var mı?
- MCP sunucuları ve büyük bağlam harcamayı nasıl etkiler?
- Bobalytics'te **Bob factor** neyi ölçüyor? Bu metrik sizi neden ikna ederdi ya da etmezdi?
- Admin olarak bir kullanıcıya harcama limiti koymak ile her çalıştırmaya `--max-cost` koymak aynı şey mi?

> Sunumda gösterilen verileri paylaşmadan önce anonimleştirin.
