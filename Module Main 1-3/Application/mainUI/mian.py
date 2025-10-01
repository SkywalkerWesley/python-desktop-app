# Main function
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication

from module1 import LabViewModule1
from module2 import LabViewModule2
from module3 import LabViewModule3
DESIGN_W, DESIGN_H = 2560, 1440

os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "0")  # disable auto if we’re forcing our own factor
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)
try:
    QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
except AttributeError:
    pass


try:
    _tmp_app = QtWidgets.QApplication([])
    primary = _tmp_app.primaryScreen()
    avail = primary.availableGeometry()
    scale = min(avail.width() / DESIGN_W, avail.height() / DESIGN_H)
    scale = max(0.75, min(scale, 2.0))
    _tmp_app.quit()
    del _tmp_app
except Exception:
    scale = 1.0

os.environ["QT_SCALE_FACTOR"] = f"{scale:1.0f}"
os.environ["QT_FONT_DPI"] = "96"

def main(args):
    app = QApplication([])
    screen = app.primaryScreen()
    size = screen.availableGeometry()
    match args:
        case 1:
            labView = LabViewModule1(size.width(), size.height(), app)
        case 2:
            labView = LabViewModule2(size.width(), size.height(), app)
        case 3:
            labView = LabViewModule3(size.width(), size.height(), app)
        case _:
            labView = LabViewModule1(size.width(), size.height(), app)
    # Start reasonably sized on the current screen; global scale already applied
    try:
        # 94% of available area, for example
        target_w = int(size.width() * 0.94)
        target_h = int(size.height() * 0.94)
        labView.resize(target_w, target_h)
        labView.move(size.left() + (size.width() - target_w)//2,
                     size.top() + (size.height() - target_h)//2)
    except Exception:
        pass

    app.exec_()

if __name__ == "__main__":
    main(1)