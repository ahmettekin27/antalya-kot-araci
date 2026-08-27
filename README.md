# Antalya Ondülasyon ve Kot Aracı (QGIS Eklentisi)

Antalya ili ve yakın çevresi için Sayısal Yükseklik Modeli (DEM) verileri ile Türkiye Jeoit Modeli-2020 (TG-20) esas alınarak hazırlanmış, 45.000 sıklaştırılmış grid noktası üzerinden mikrosaniyeler mertebesinde jeoit ondülasyonu (N), ortometrik kot (H) ve elipsoit kot (h) hesabı yapan QGIS eklentisidir.

---

### Temel Özellikler

- **Yüksek Hızlı IDW Enterpolasyonu:** KD-Tree algoritması sayesinde tıklanan noktanın en yakın 4 referans komşusunu mikrosaniyede bularak ters mesafe ağırlıklı enterpolasyon yapar.
- **Jeodezik Çıktılar:**
  - **N (Jeoit Ondülasyonu):** TG-20 model tabanlı jeoit yüksekliği (metre).
  - **H (Ortometrik Kot):** Fiziksel yeryüzü yükseklik değeri (metre).
  - **h (Elipsoit Kot):** GNSS/GPS alıcılarının ölçtüğü geometrik yükseklik (metre).
- **Akıllı Nokta Yakalama (Snapping):** QGIS mıknatıs aracı açıkken köşe noktalarını (vertex) ve çizgileri otomatik yakalar.
- **Otomatik Öznitelik Tablosu:** Sorgulanan tüm noktaları geçici bir hafıza katmanında depolar; nokta adı, X-Y koordinatları ve teknik yasal notu tabloya işler.
- **Pratik Kullanım:** Sol tıklama ile nokta üretir, sağ tıklama ile aracı otomatik sonlandırır.

---

### Kurulum

**Yöntem 1: GitHub ZIP ile Kurulum**
1. Bu sayfada sağ üstteki yeşil Code butonuna basıp Download ZIP seçeneğine tıklayın.
2. QGIS menüsünden Eklentiler -> Eklentileri Yönet ve Yükle penceresini açın.
3. Sol menüden ZIP'ten Yükle sekmesine gelin.
4. İndirdiğiniz zip dosyasını seçip Eklentiyi Kur butonuna basın.

**Yöntem 2: Manuel Kurulum**
Klasörü işletim sisteminize göre ilgili eklenti dizinine kopyalayın:
- Windows: `%APPDATA%\QGIS\QGIS3\profiles\default\python\plugins\antalya_kot_araci`
- Linux: `~/.local/share/QGIS/QGIS3/profiles/default/python/plugins/antalya_kot_araci`
- macOS: `~/Library/Application Support/QGIS/QGIS3/profiles/default/python/plugins/antalya_kot_araci`

---

### Kullanım Rehberi

1. QGIS araç çubuğundaki Antalya Kot & Ondülasyon Sorgula simgesine tıklayın.
2. Harita üzerinde kotunu öğrenmek istediğiniz herhangi bir noktaya Sol Tıklayın.
3. Bilgi penceresinde X, Y koordinatları ve N, H, h yükseklik değerleri gösterilir, nokta haritaya eklenir.
4. Çıkmak için haritada herhangi bir yere Sağ Tıklayın.

---

### Yasal Uyarı

İşbu eklenti tarafından üretilen değerler, DEM verisi üzerinden hesaplanan Ortometrik Değerler ile Türkiye Jeoit Modeli-2020 (TG-20) esas alınarak sıklaştırılmış noktaların enterpolasyonu ile elde edilmiş yaklaşık değerleri içermektedir; resmi haritacılık ve kadastro işlemlerinde kesin kot değeri yansıtmamaktadır.

---

### Geliştirici ve Lisans

- **Geliştirici:** Ahmet TEKİN
- **Lisans:** GNU General Public License v2.0 (GPL-2.0)
