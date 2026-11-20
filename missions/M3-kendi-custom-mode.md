# M3 - Kendi custom mode'unuzu yazın (Mode + Rules + Skill)

**Süre:** 20 dk | **Bob özelliği:** **Custom Mode**, **Rules**, **Skills** | **Kontrol:** `./verify/run.sh m3` (Windows: `.\verify\run.ps1 m3`)

## Durum

M2'yi bitirdiniz ama code review'da ekip lideri aynı yorumu üçüncü kez yazdı: "Bob yine el kitabını çiğnedi."
Bob her yeni sohbette **sıfırdan başlıyor**. Ekibin tek kaynağı [`docs/ENGINEERING-HANDBOOK.md`](../docs/ENGINEERING-HANDBOOK.md).

Hedef, **tek bir persona** kurmak: yalnızca test yazan ve çalıştıran bir **QA Engineer**. Bu mod kendi kurallarını ve kendi skill'ini yanında taşır.

## Hamle 1 - Modu yazın

`.bob/custom_modes.yaml` içinde yeni bir mod tanımlayın (bir mod tanımı, sıfırdan **sizin** yazdığınız bir persona):
test yazar ve çalıştırır, ama **`tests/` dışındaki hiçbir dosyayı değiştiremez**. Modu seçip üretim koduna yazdırmayı deneyin: engellenmeli.

## Hamle 2 - Kurallar ve skill

Modun iki şeyi kendiliğinden bilmesini sağlayın:

- **Rules:** El kitabındaki para, hata, loglama ve güvenlik standartları (`.bob/rules/` tüm modlar için, `.bob/rules-<mod-slug>/` yalnızca bu mod için).
- **Skill:** Test yazma adımları tek bir tekrar kullanılabilir prosedür olsun (`.bob/skills/<ad>/SKILL.md`). Bob ilgili isteği görünce kendisi devreye alsın.

## Kabul kriteri

- `./verify/run.sh m3` içindeki **11 kontrolün tamamı** PASS
- Yeni bir sohbette el kitabını **hiç anmadan** bir şey sorduğunuzda Bob kuralı kendisi uyguluyor
- Mod, üretim koduna yazma denemesinde **engelleniyor**

## Keşif noktaları

- Bob Settings'teki **Modes** sekmesi veya `bob --mode <slug>` ile Shell'de modu seçin. Hangi alanlar zorunlu?
- Rule, skill ve mode farkı: biri her zaman yüklenir, biri ilgili istekte devreye girer, biri kimlik ve yetki tanımlar. Hangisi hangisi?
- "Dosya düzenleyebilir" ile "yalnızca şu dosyaları düzenleyebilir" aynı şey değil. Mod ayarında bunu nasıl ifade edersiniz?
- Proje düzeyi ile kullanıcı düzeyi: hangi dosya repoya girer, ekip arkadaşınız görür mü?

## Dikkat

Sessiz hatalar yaygındır: yanlış yazılmış klasör adı veya geçersiz yetki grubu **hata vermez**, yalnızca yok sayılır.
YAML dosyasında kıvrık tırnak ve uzun tire gibi ASCII dışı karakterler kullanmayın. `verify` çıktısı nerede takıldığınızı gösterir.
