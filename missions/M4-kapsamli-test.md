# M4 - Kapsamlı test yazımı (kendi modunuzla)

**Süre:** 25 dk | **Bob özelliği:** M3'te yazdığınız **Custom Mode + Rules + Skill**'in değeri | **Kontrol:** `./verify/run.sh m4` (Windows: `.\verify\run.ps1 m4`)

## Durum

Release gate'in ikinci koşulu: `services/core` için **%85 satır kapsamı**. Şu an `tests/` altında yalnızca bir `/health` testi var.
Ekip lideri: "Test sayısı değil, **testlerin gerçekten koruduğu davranış** önemli."

- [`docs/ENGINEERING-HANDBOOK.md`](../docs/ENGINEERING-HANDBOOK.md) bölüm 4
- [`docs/FEE-POLICY.md`](../docs/FEE-POLICY.md): ücret tablosu ve sınır değerleri

## Hamle 1 - Testleri yazdırın

**M3'te yazdığınız moda** geçin ve `services/core` için kapsamlı bir test paketi yazdırın. Mod ve skill'i siz kurduğunuz için
test standardını (API seviyesi, store sıfırlama, sınır değerleri) tekrar anlatmanız gerekmemeli. Gerekiyorsa M3'e dönüp skill'i düzeltin.

## Hamle 2 - Bulunan hataları kapatın

İyi bir sınır değeri veya negatif test **4 gizli hatayı** kendiliğinden ortaya çıkarır. Mod üretim koduna yazamaz, bu yüzden hatayı raporlatın,
sonra **Agent** moduna geçip düzeltin ve düzeltmeyi testle kanıtlayın. Test geçmediğinde önce testin mi, kodun mu yanlış olduğuna el kitabına bakarak karar verin.

## Kabul kriteri

- `./verify/run.sh m4` içindeki **12 kontrolün tamamı** PASS
- En az 25 test, %85 satır kapsamı, ekip standardına uygun
- Testleriniz **bilinçli olarak bozulan kodu yakalıyor** (doğrulayıcı kodu geçici bozar, testler kırmızıya dönmeli)

## Keşif noktaları

- Moddan üretim koduna dokunmasını isteyin. Ne oluyor? Bu bir kısıtlama mı, güvenlik ağı mı?
- Bob hatayla karşılaşınca testi mi gevşetiyor, hatayı mı raporluyor? Skill'inizde bunu söylediniz mi?
- Mutasyon kontrolü FAIL ise hangi davranışı test etmediğinizi çıktıdan okuyabilir misiniz?

## Bonus

`pytest --cov` çıktısını Bob'a yorumlatın: sizce en riskli kapsanmayan davranış hangisi?
