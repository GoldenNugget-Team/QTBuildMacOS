"""Exercise the shared Qt modules without opening a desktop window."""
import PySide6
import shiboken6
from PySide6.QtCore import QByteArray, qVersion
from PySide6.QtGui import QColor, QImage, QPainter
from PySide6.QtNetwork import QNetworkAccessManager
from PySide6.QtSvg import QSvgRenderer
from PySide6.QtWidgets import QApplication, QLabel

app = QApplication([])
assert PySide6.__version__ == shiboken6.__version__ == qVersion() == "6.12.0"
label = QLabel("GoldenNugget-Team")
label.resize(200, 40)
image = QImage(label.size(), QImage.Format.Format_ARGB32)
image.fill(QColor("transparent"))
label.render(image)
renderer = QSvgRenderer(QByteArray(
    b'<svg xmlns="http://www.w3.org/2000/svg" width="10" height="10">'
    b'<rect width="10" height="10" fill="red"/></svg>'
))
assert renderer.isValid()
painter = QPainter(image)
renderer.render(painter)
painter.end()
network = QNetworkAccessManager()
app.processEvents()
print("QT_SMOKE_OK")
