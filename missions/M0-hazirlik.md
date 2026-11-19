# M0 - Hazırlık ve "Merhaba Bob"

**Süre:** 10 dk | **Bob özelliği:** Mod seçici, `@` bağlamı | **Kontrol:** `./verify/run.sh m0`

## Durum

Aurora Bank'ın Instant Pay ekibine bu sabah katıldınız. İlk iş: repoyu açın ve Bob'un projeyi nasıl gördüğünü anlayın.

## Hamle 1 - Repoyu kur

Facilitator'ın paylaştığı GitHub **template repo**dan **kendi hesabınızda** bir kopya oluşturun, klonlayın ve `./setup.sh --scanners` çalıştırın (Windows/PowerShell: `.\setup.ps1 -Scanners`; doğrulama `.\verify\run.ps1 m0`).
Klasörü Bob'da açın (IDE'de klasörü açın, Shell'de klasörün içinden başlatın).

## Hamle 2 - Bob'a sorun

Bob'a bu projenin ne olduğunu **kendi cümlelerinizle** sordurun ve cevabı dokümanlarla karşılaştırın.
Aynı soruyu iki farklı modda sorup farkı gözlemleyin.

## Kabul kriteri

- `./verify/run.sh m0` tüm kontrollerde PASS
- Bob'un `services/core` içinde kaç uç nokta olduğunu söylediğini kodda kendiniz doğruladınız

## Keşif noktaları

- Sohbet kutusunun yanındaki **mod seçici**: her modun neye izin verdiğine bakın.
- Sohbet alanına `@` yazınca ne oluyor?
- Takılırsanız facilitator'dan kademeli ipucu isteyin.
