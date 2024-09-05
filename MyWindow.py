from PySide2.QtWidgets import QWidget, QFileDialog, QMessageBox
from PySide2.QtCore import QStandardPaths
from Ui_CodeDeal import Ui_MyWindow
from SNJCodeConverter import *


class MyWindow(QWidget, Ui_MyWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("SNJ401 烧录文件转换")
        self.tbtnSelect.setDefaultAction(self.actSelect)
        self.tbtnSelect.clicked.connect(self.selectFile)
        self.tbtnDo.clicked.connect(self.convertCodeFile)
        self.tbtnClose.clicked.connect(self.close)

    def selectFile(self):
        desktopPath = QStandardPaths.writableLocation(QStandardPaths.DesktopLocation)
        filePath, _ = QFileDialog.getOpenFileName(
            self,
            "选择文件",
            desktopPath,
            "文本文件 (*.txt);;烧录文件 (*.fpga);;所有文件 (*)",
        )
        if filePath:
            self.editFile.setText(str(filePath).replace("/", "\\"))
            self.pBar.setEnabled(True)
            return
        MessageBox = QMessageBox()
        MessageBox.critical(self, "警告", "选择的文件路径为空,请重新选择!!!")

    def convertCodeFile(self):
        filePath = self.editFile.text()
        if not filePath:
            MessageBox = QMessageBox()
            MessageBox.critical(self, "警告", "请先选择需要转换的文件!!!")
            return
        SNJCodeConverter(filePath)
