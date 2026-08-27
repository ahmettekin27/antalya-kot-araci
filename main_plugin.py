import os
import math
import numpy as np
from scipy.spatial import cKDTree

from qgis.PyQt.QtGui import QIcon
from qgis.PyQt.QtWidgets import QAction, QMessageBox
from qgis.PyQt.QtCore import QVariant, Qt
from qgis.gui import QgsMapTool, QgsSnapIndicator
from qgis.core import (
    QgsProject,
    QgsFeature,
    QgsGeometry,
    QgsPointXY,
    QgsVectorLayer,
    QgsField,
    QgsPointLocator
)

class SifreliKotMapTool(QgsMapTool):
    def __init__(self, canvas, plugin_instance):
        super().__init__(canvas)
        self.canvas = canvas
        self.plugin = plugin_instance
        self.snap_indicator = QgsSnapIndicator(canvas)
        self.setCursor(Qt.CrossCursor)

    def _get_snapped_match(self, pos):
        snapping_utils = self.canvas.snappingUtils()
        config = QgsProject.instance().snappingConfig()
        snapping_utils.setConfig(config)
        
        if config.enabled():
            return snapping_utils.snapToMap(pos)
        return None

    def canvasMoveEvent(self, mouseEvent):
        match = self._get_snapped_match(mouseEvent.pos())
        if match and match.isValid():
            self.snap_indicator.setMatch(match)
            self.snap_indicator.setVisible(True)
        else:
            self.snap_indicator.setVisible(False)

    def canvasReleaseEvent(self, mouseEvent):
        # 1. Sag tik kontrolu (Eklentiyi devreden cikar)
        if mouseEvent.button() == Qt.RightButton:
            self.plugin.action.setChecked(False)
            self.canvas.unsetMapTool(self)
            return

        # Sadece Sol Tik ile sorgulama yap
        if mouseEvent.button() != Qt.LeftButton:
            return

        match = self._get_snapped_match(mouseEvent.pos())
        if match and match.isValid():
            pt = match.point()
            yakalama_durumu = "Yakalama (Snap) ile"
        else:
            pt = self.toMapCoordinates(mouseEvent.pos())
            yakalama_durumu = "Serbest Tiklama ile"
        
        koor_x = round(pt.x(), 3)
        koor_y = round(pt.y(), 3)

        ondi_n, z_orto, z_elip = self.plugin.idw_hesapla(pt.x(), pt.y())
        
        bilgi_notu = (
            "Isbu noktalar, Ahmet TEKIN tarafindan DEM verisi uzerinden hesaplanan "
            "Ortometrik Degerler ile Turkiye Jeoit Modeli-2020 (TG-20) esas alinarak "
            "siklastirilmis noktalarin enterpolasyonu ile elde edilmis yaklasik degerleri icermektedir; "
            "kesin kot degeri yansitmamaktadir."
        )

        layer = self.plugin.get_or_create_layer()
        mevcut_sayi = layer.featureCount()
        nokta_adi = f"tekin_{mevcut_sayi + 1}"
        
        f = QgsFeature(layer.fields())
        f.setGeometry(QgsGeometry.fromPointXY(pt))
        f.setAttribute("Nokta_Adi", nokta_adi)
        f.setAttribute("Koor_X", koor_x)
        f.setAttribute("Koor_Y", koor_y)
        f.setAttribute("Ondi_N", ondi_n)
        f.setAttribute("Z_Ortometrik", z_orto)
        f.setAttribute("Z_Elipsoid", z_elip)
        f.setAttribute("Not", bilgi_notu)
        
        layer.dataProvider().addFeatures([f])
        layer.updateExtents()
        layer.triggerRepaint()
        
        QMessageBox.information(
            None,
            "Nokta Kot Bilgisi",
            f"Nokta Adi: {nokta_adi} ({yakalama_durumu})\n"
            f"Koordinat:\nX: {koor_x:.3f}\nY: {koor_y:.3f}\n\n"
            f"Ondulasyon (N): {ondi_n:.2f} m\n"
            f"Ortometrik (H): {z_orto:.2f} m\n"
            f"Elipsoit (h): {z_elip:.2f} m\n\n"
            f"Bilgi Notu:\n{bilgi_notu}"
        )

    def deactivate(self):
        self.snap_indicator.setVisible(False)


class AntalyaKotPlugin:
    def __init__(self, iface):
        self.iface = iface
        self.canvas = iface.mapCanvas()
        self.action = None
        self.map_tool = None
        self.hedef_layer = None
        
        self.tree = None
        self.matris = None
        self.xor_key = b"KorkuteliSulama2026AntalyaOndulasyonGizliKey"

    def initGui(self):
        plugin_dir = os.path.dirname(__file__)
        icon_path_svg = os.path.join(plugin_dir, "icon.svg")
        icon_path_png = os.path.join(plugin_dir, "icon.png")
        
        if os.path.exists(icon_path_svg):
            icon = QIcon(icon_path_svg)
        elif os.path.exists(icon_path_png):
            icon = QIcon(icon_path_png)
        else:
            icon = QIcon()

        self.action = QAction(icon, "Antalya Kot & Ondulasyon Sorgula (Sag Tik: Iptal)", self.iface.mainWindow())
        self.action.setCheckable(True)
        self.action.triggered.connect(self.toggle_tool)

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("&Antalya Altyapi Araclari", self.action)
        
        self.veriyi_yukle()

    def unload(self):
        if self.action:
            self.iface.removePluginMenu("&Antalya Altyapi Araclari", self.action)
            self.iface.removeToolBarIcon(self.action)

    def veriyi_yukle(self):
        data_path = os.path.join(os.path.dirname(__file__), "data", "antalya_grid.dat")
        if not os.path.exists(data_path):
            return
            
        with open(data_path, "rb") as f:
            sifreli_baytlar = bytearray(f.read())

        key_len = len(self.xor_key)
        for i in range(len(sifreli_baytlar)):
            sifreli_baytlar[i] ^= self.xor_key[i % key_len]

        self.matris = np.frombuffer(sifreli_baytlar, dtype=np.float32).reshape(-1, 5)
        self.tree = cKDTree(self.matris[:, 0:2])

    def idw_hesapla(self, x, y, k=4):
        if self.tree is None:
            return 0.0, 0.0, 0.0
            
        mesafeler, indeksler = self.tree.query([x, y], k=k)
        total_w, sum_n, sum_h, sum_elip = 0.0, 0.0, 0.0, 0.0
        
        for dist, idx in zip(mesafeler, indeksler):
            row = self.matris[idx]
            n_val, h_val, elip_val = row[2], row[3], row[4]
            
            if dist == 0:
                return round(float(n_val), 2), round(float(h_val), 2), round(float(elip_val), 2)
                
            w = 1.0 / (dist ** 2)
            total_w += w
            sum_n += n_val * w
            sum_h += h_val * w
            sum_elip += elip_val * w
            
        return (
            round(float(sum_n / total_w), 2),
            round(float(sum_h / total_w), 2),
            round(float(sum_elip / total_w), 2)
        )

    def get_or_create_layer(self):
        katman_adi = "Sorgulanan_Grid_Noktalari"
        proje_katmanlari = QgsProject.instance().mapLayersByName(katman_adi)
        
        istenen_alanlar = [
            QgsField("Nokta_Adi", QVariant.String, len=50),
            QgsField("Koor_X", QVariant.Double, len=15, prec=3),
            QgsField("Koor_Y", QVariant.Double, len=15, prec=3),
            QgsField("Ondi_N", QVariant.Double, len=10, prec=2),
            QgsField("Z_Ortometrik", QVariant.Double, len=10, prec=2),
            QgsField("Z_Elipsoid", QVariant.Double, len=10, prec=2),
            QgsField("Not", QVariant.String, len=300)
        ]

        if proje_katmanlari:
            self.hedef_layer = proje_katmanlari[0]
            mevcut_alanlar = [f.name() for f in self.hedef_layer.fields()]
            eklenecekler = [f for f in istenen_alanlar if f.name() not in mevcut_alanlar]
            if eklenecekler:
                pr = self.hedef_layer.dataProvider()
                pr.addAttributes(eklenecekler)
                self.hedef_layer.updateFields()
            return self.hedef_layer

        crs_authid = self.canvas.mapSettings().destinationCrs().authid()
        self.hedef_layer = QgsVectorLayer(f"Point?crs={crs_authid}", katman_adi, "memory")
        pr = self.hedef_layer.dataProvider()
        pr.addAttributes(istenen_alanlar)
        self.hedef_layer.updateFields()
        QgsProject.instance().addMapLayer(self.hedef_layer)
        
        return self.hedef_layer

    def toggle_tool(self, checked):
        if checked:
            if self.map_tool is None:
                self.map_tool = SifreliKotMapTool(self.canvas, self)
            self.canvas.setMapTool(self.map_tool)
        else:
            if self.map_tool:
                self.canvas.unsetMapTool(self.map_tool)
