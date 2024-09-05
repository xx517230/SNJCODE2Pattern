from PySide2.QtWidgets import QApplication, QWidget, QFileDialog, QMessageBox
from MyWindow import *


if __name__ == "__main__":
    app = QApplication([])
    window = MyWindow()
    window.show()
    app.exec_()
