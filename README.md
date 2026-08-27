# Antalya Ondülasyon ve Kot Aracı (QGIS Plugin)

![QGIS](https://img.shields.io/badge/QGIS-3.0%2B-589632?logo=qgis&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-GPL%20v2-blue.svg)

Antalya ili ve yakın çevresi için Sayısal Yükseklik Modeli (DEM) verileri ile **Türkiye Jeoit Modeli-2020 (TG-20)** esas alınarak hazırlanmış, 45.000 sıklaştırılmış grid noktası üzerinden mikrosaniyeler mertebesinde jeoit ondülasyonu ($N$), ortometrik kot ($H$) ve elipsoit kot ($h$) hesabı yapan QGIS eklentisidir.

---

## 🚀 Temel Özellikler

* **Yüksek Hızlı IDW Enterpolasyonu:** `scipy.spatial.cKDTree` veri yapısı sayesinde haritada tıklanan noktanın en yakın 4 referans noktasını mikrosaniyede bularak ters mesafe ağırlıklı (Inverse Distance Weighting - IDW) enterpolasyon gerçekleştirir.
* **Kapsamlı Jeodezik Çıktılar:**
  * **$N$ (J敘it Ondülasyonu):** TG-20 model tabanlı jeoit yüksekliği (m).
  * **$H$ (Ortometrik Kot):** Fiziksel yeryüzü yükseklik değeri (m).
  * **$h$ (Elipsoit Kot):** GNSS/GPS alıcılarının doğrudan ölçtüğü geometrik yükseklik ($h = H + N$).
* **Akıllı Nokta Yakalama (Snapping):** QGIS'in yerel mıknatıs (snapping) motoruyla tam entegredir. Açık olduğunda boru hatları, parsel sınırları veya mevcut köşe noktalarını (vertex) otomatik olarak yakalar.
* **Otomatik Öznitelik Tablosu:** Sorgulanan tüm noktaları geçici bir bellek (memory) katmanında depolar; `Nokta_Adi` (`tekin_1`, `tekin_2`...), hassas $X, Y$ koordinatları ve teknik yasal bilgilendirme notunu öznitelik tablosuna eksiksiz işler.
* **Kullanıcı Dostu Etkileşim:** Sol tıklama ile nokta üretir, sağ tıklama ile harita aracını otomatik sonlandırır.

---

## 📂 Depo Dosya Yapısı

```text
antalya-kot-araci/
├── data/
│   └── antalya_grid.dat     # Sıkıştırılmış ve şifrelenmiş Antalya referans grid verisi
├── __init__.py              # QGIS eklenti başlatıcı fabrikası
├── main_plugin.py           # Eklenti mantığı, KD-Tree motoru ve harita aracı
├── metadata.txt             # QGIS eklenti yapılandırma ve versiyon bilgileri
├── icon.png                 # QGIS Eklenti Yöneticisi ve menü ikonu (PNG)
├── icon.svg                 # Araç çubuğu vektörel ikonu (SVG)
└── README.md                # Eklenti tanıtım ve kullanım kılavuzu
