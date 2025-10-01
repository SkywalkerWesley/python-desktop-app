# Main function
import os
from PyQt5 import QtCore, QtWidgets
from PyQt5.QtWidgets import QApplication

from module1 import LabViewModule1
from module2 import LabViewModule2
from module3 import LabViewModule3


#  Qt auto-scale for each screen (must be set BEFORE creating QApplication)
os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "1")
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)
QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

# Qt 5.14+ only: avoid rounding scale factors (e.g., 1.25 → 1) which can cause layout issues
try:
    QtWidgets.QApplication.setHighDpiScaleFactorRoundingPolicy(
        QtCore.Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
    )
except AttributeError:
    pass

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
    app.exec_()

if __name__ == "__main__":
    main(1)