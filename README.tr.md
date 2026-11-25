> 🚧 **Durum: aktif geliştirme.** Yazarın kullanımında çalışıyor; arayüzler değişebilir.

# Türkçe Model Kataloğu

**Türkçe ile ilgili 190 dil modeli, ses (ASR/TTS), NLP, veri seti ve değerlendirme kaynağının** kaynaklı kataloğu. Her kayıt için bir araştırma kartı var (geliştiricinin iddiası, nasıl eğitildiği, nasıl denenir, bağımsız kanıt, açık sorular, kaynak bağlantıları) ve hepsini gezmek için tek dosyalık, çevrimdışı çalışan bir HTML sayfası.

[jev-teknik-arastirma](https://github.com/KemalG-u/jev-teknik-arastirma) deposundan farkı: o depo tek bir sağlayıcının karar API'si üzerine tek bir yazıdır; bu depo ise Türkçe ile ilgili modellerin, veri setlerinin ve ölçütlerin geniş bir kataloğudur, her kayıt için ayrı araştırma kartı vardır.

English: [README.md](README.md)

> **Anlık görüntü: veriler Ekim 2026'da toplandı; lisanslar ve ölçüm iddiaları yeniden doğrulanmadı.**
> Burada hiçbir model indirilmedi, çalıştırılmadı ve ölçülmedi. Kart, bir kaynağın ne dediğini ve o iddianın ne kadar kontrol edilebildiğini kaydeder; kalite sıralaması değildir.

## Neden var

Türkçe model bilgisi Hugging Face kartlarına, blog yazılarına, makalelere ve şirket sayfalarına dağılmış durumda; aynı ad çoğu zaman birkaç farklı sürümü kapsıyor. Bu proje hepsini tek yerde toplar, modeli ürün, veri seti ve araçtan ayırır ve her iddiayı kaynağına bağlı tutar; böylece neyin kanıt, neyin reklam olduğu görünür.

## Depoda ne var

| Yol | İçerik |
|---|---|
| `sayfalar/TURKCE-MODEL-LABORATUVARI.html` | Üretilmiş, tek dosyalık katalog sayfası (tarayıcıda aç; ağ gerekmez) |
| `sayfalar/turkce-model-laboratuvari.template.html` | Verinin yerleştirildiği sayfa şablonu |
| `arastirma/katalog.json` | Özgün 190 kayıtlık katalog (ad, bağlantı, geliştirici, lisans notu, tarih, eski notlar) |
| `arastirma/tam-tarama/*-sonuc.json` | Sekiz pakette araştırma kartları (`*-girdi.json` paket girdileridir) |
| `arastirma/eleme-kararlari.json` | Etkin görünümden çıkarılan (terk edilmiş/geri çekilmiş) kayıtlar ve yerine konanlar, kanıt bağlantılarıyla |
| `arastirma/depo-kimlikleri.json`, `metin-ilk-tur.json`, `ses-ilk-tur.json` | Sayfa üreticisinin kullandığı depo sürümleri ve ilk tur notları |
| `arastirma/*.py`, `*.js`, `*.cjs` | Üretim ve doğrulama betikleri |

Bu anlık görüntüde kart durumları: 44 belgelenmiş, 88 sınırlı, 5 kimlik/erişim çözülemeyen, 53 model olmayan kaynak (veri seti, araç, makale, ürün). Bunlar araştırma durumudur, performans puanı değildir. Özgün katalog notlarındaki eski A-D etiketleri yazarın önceki kullanım amacına göre dar işe uygunluk etiketidir, genel kalite sırası değildir.

## Hızlı başlangıç

Gezmek için: `sayfalar/TURKCE-MODEL-LABORATUVARI.html` dosyasını tarayıcıda aç.

Sayfayı yeniden üretmek ve doğrulamak (Python 3, sözdizimi denetimi için Node.js):

```bash
python arastirma/sayfa-uret.py      # JSON'dan sayfalar/TURKCE-MODEL-LABORATUVARI.html üretir
python arastirma/sayfa-dogrula.py   # sayım, bağlantı, özgün katalogla eşitlik, JS sözdizimi
```

Bu anlık görüntüde yeniden üretilen sayfa, depodaki sayfayla bayt bayt aynıdır ve `sayfa-dogrula.py` geçer.

`katalog.json` yerine yazarın özgün katalog HTML'sinden çalışmak istersen `MODEL_CATALOG_HTML` ortam değişkenine yolunu ver (içinde `<script id="veri" type="application/json">` bloğu olmalı); doğrulayıcı bu durumda SHA-256 özetini de kontrol eder.

## Gereksinimler

Python 3 (yukarıdaki komutlar için yalnız standart kütüphane) ve Node.js (`sayfa-dogrula.py` sözdizimi denetimi için). Üçüncü taraf paket yok.

## Sınırlar ve doğrulanmamış iddialar

- **Anlık görüntü, canlı değil.** Veriler Ekim 2026'da toplandı. Lisans, çıkış tarihi, ölçüm sayıları ve erişilebilirlik değişmiş olabilir; bu sürümde hiçbiri yeniden doğrulanmadı.
- **Kartlar ölçüm değildir.** Hiçbir model indirilmedi ya da çalıştırılmadı. "Belgelenmiş", kaynakların okunabildiği ve tutarlı olduğu anlamına gelir; modelin iyi olduğu anlamına gelmez.
- **Ham kaynak çıkarımları dahil değil.** Araştırma sırasında kullanılan önbellek sayfa metinleri ve kayıt başına toplama dosyaları bu depodan çıkarıldı (üçüncü taraf içerik; iletişim adresi ve forum kullanıcı adı gibi kişisel veri olabilir). `kaynak-topla.py`, `kaynak-ek.py`, `destek-kaynaklari.py`, `destek-kartlari.py` ve `eleme-uygula.py` bu dosyalara ve ağa ihtiyaç duyar; yöntemin belgesi olarak durur, bu depodan olduğu gibi çalışmaz. Paket girdileri çıkarılan klasörlere göreli yollarla bağlanır.
- **Sayfa yalnız makineyle denetlendi.** Veri denetimleri ve JavaScript sözdizimi geçiyor; gerçek tarayıcıda görsel ve etkileşim kabulü tamamlanmadı (önceki deneme `file://` tarayıcı politikası yüzünden engellendi).
- Özgün katalogdaki bazı notlar (`gerekce` alanı) yazarın eski görev etiketlerini (ör. "YEREL-LM") anar; doğrulayıcı kataloğu özgünle karşılaştırdığı için olduğu gibi bırakıldı.

## Lisans

- Yazarın derlediği veri ve metin (katalog, kartlar, eleme kararları, sayfa metni): [CC BY 4.0](LICENSE-DATA).
- Kod (betikler ve sayfa şablonu/üreticisi): [Apache-2.0](LICENSE).
- Üçüncü taraf modeller, veri setleri ve makaleler hakkındaki bilgi, her kartta listelenen kaynaklardan özetlenmiş ve onlara bağlanmıştır; o eserler kendi lisans ve koşullarında kalır. Bkz. [THIRD-PARTY.md](THIRD-PARTY.md).

## Katkı

Kaynak bağlantılı düzeltmeler issue olarak memnuniyetle karşılanır. Güvenlik bildirimi için [SECURITY.md](SECURITY.md).
