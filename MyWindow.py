from PySide2.QtWidgets import QWidget, QFileDialog, QMessageBox
from PySide2.QtCore import QStandardPaths
from Ui_CodeDeal import Ui_MyWindow
from SNJ401ReadRom import readRom
from SNJ401WriteRom import writeRom


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
            "烧录文件 (*.fpga);;所有文件 (*)",
        )
        if filePath:
            self.editFile.setText(str(filePath).replace("/", "\\"))
            self.pBar.setEnabled(True)
            return
        MessageBox = QMessageBox()
        MessageBox.critical(self, "警告", "选择的文件路径为空,请重新选择!!!")

    def convertCodeFile(self):
        fileSize = 0
        debugFlag = False
        filePath = self.editFile.text()

        if not filePath:
            MessageBox = QMessageBox()
            MessageBox.critical(self, "警告", "请先选择需要转换的文件!!!")
            return
        if self.rbtnSNJ401.isChecked():
            fileSize = 128 * 1024
        else:
            fileSize = 52 * 1024
        if self.rbtnDebug.isChecked():
            debugFlag = True
        else:
            debugFlag = False
        if self.chkRead.isChecked():
            readRom(filePath, fileSize, debugFlag)
        if self.chkWrite.isChecked():
            writeRom(filePath, fileSize)
