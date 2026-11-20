# M2 - Üretim hatası (Bob Shell / CLI)

**Süre:** 20 dk | **Bob özelliği:** **Bob Shell / CLI** (`bob chat`, `bob run`) | **Kontrol:** `python fixtures/incident/repro.py`, sonra `./verify/run.sh m2` (Windows: `.\verify\run.ps1 m2`)

## Durum

SEV-2 açık: müşterilerin parası **iki kez** düşüyor, bazı transferlerde para alıcıya **hiç ulaşmıyor**, bakiyelerde kuruş altı farklar var ve istemciler düzgün bir hata alamıyor.

- [`docs/INCIDENT-2041.md`](../docs/INCIDENT-2041.md): olay kaydı
- [`fixtures/incident/transfer.log`](../fixtures/incident/transfer.log): sunucu logu
- [`fixtures/incident/repro.py`](../fixtures/incident/repro.py): sorunu yeniden üretir (bozukken `1`, düzelince `0` ile çıkar)
- [`docs/FEE-POLICY.md`](../docs/FEE-POLICY.md) ve [`docs/ENGINEERING-HANDBOOK.md`](../docs/ENGINEERING-HANDBOOK.md) bölüm 1-2

Bu görevi IDE sohbetinde değil, **terminalde Bob Shell ile** yürütün.

## Hamle 1 - Teşhis (etkileşimli)

Repo kökünden `bob chat` ile Bob Shell'i başlatın. Bob'a olay kaydını ve logu gösterip **kök nedenleri** bulmasını isteyin. Henüz düzeltmeyin.
Bob'un bulduğu her nedeni `repro.py` çıktısıyla eşleştirin.

## Hamle 2 - Düzeltme (tek seferlik)

Aynı işi bu kez `bob run` ile, **tur ve maliyet sınırı koyarak** yaptırın. Düzeltmelerden sonra `repro.py` ve `pytest` çalıştırın.
Dört şikâyet birbirine benziyor ama **aynı nedene bağlı değil**. Bir düzeltme başkasını bozmasın.

## Kabul kriteri

- `python fixtures/incident/repro.py` çıkış kodu `0`
- `./verify/run.sh m2` içindeki **24 kontrolün tamamı** PASS
- `pytest` hâlâ yeşil

## Keşif noktaları

- `bob --help` ve `bob run --help`: etkileşimli ile tek seferlik çalışma arasındaki fark nedir?
- `--max-turns` ve `--max-cost` ile çalışmayı sınırlayabiliyor musunuz?
- Bob terminalde komut çalıştırmadan önce ne soruyor? Hangi komutlara izin vermek mantıklı, hangilerine asla?
- Bob log dosyasını kendisi mi buldu, siz mi gösterdiniz? Sonuç farkı oldu mu?

> `bob run` tüm araçları **önceden onaylı** çalıştırır; komut başına onay istemez. Bu yüzden sınır koymak önemlidir.
