# Main function
from PyQt5.QtWidgets import QApplication

from module1 import LabViewModule1
from module2 import LabViewModule2
from module3 import LabViewModule3



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