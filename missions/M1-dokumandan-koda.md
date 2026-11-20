# M1 - Dokümandan koda

**Süre:** 25 dk | **Bob özelliği:** Plan / Agent modları, `@` ile bağlam, todo listesi | **Kontrol:** `./verify/run.sh m1` (Windows: `.\verify\run.ps1 m1`)

## Durum

Regülatör, canlıya çıkmadan önce müşteri bazlı **transfer limitlerini** ve **işlem dökümünü** zorunlu kıldı.
Bu iş için henüz **tek satır kod yok**. Elinizde yalnızca ürün gereksinimi ve API sözleşmesi var:

- [`docs/PRD-limits.md`](../docs/PRD-limits.md): iş kuralları ve örnek senaryo
- [`docs/API-SPEC-limits.yaml`](../docs/API-SPEC-limits.yaml): uç noktalar ve şemalar

## Hamle 1 - Önce anlayın (Plan modu)

PRD ve API sözleşmesini Bob'a **bağlam olarak** verin (yapıştırmayın). Bob'dan bir uygulama planı çıkarmasını isteyin.
Planı okuyun: PRD'nin bir kuralını atlamış mı?

## Hamle 2 - Sonra yazın (Agent modu)

Onayladığınız planı uygulatın. Hedef: `services/limits/main.py` içinde `app` adlı bir FastAPI uygulaması.
Bellek içi depolama yeterli, yeni bağımlılık eklemeyin, `services/core`'a dokunmayın.

## Kabul kriteri

- `./verify/run.sh m1` içindeki **35 kontrolün tamamı** PASS

## Keşif noktaları

- Önce **anlamak** ile **yazmak** aynı mod olmak zorunda mı?
- Bob'un işi parçalara böldüğünü gösteren **todo listesi** sizin kontrol edebileceğiniz bir yer mi?
- FAIL satırının altındaki açıklama PRD'deki hangi kuralı kaçırdığınızı söyler. Düzeltmeyi o cümleye dayandırın.
