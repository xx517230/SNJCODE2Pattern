# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'CodeDeal.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *

import res_rc

class Ui_MyWindow(object):
    def setupUi(self, MyWindow):
        if not MyWindow.objectName():
            MyWindow.setObjectName(u"MyWindow")
        MyWindow.resize(583, 464)
        self.actSelect = QAction(MyWindow)
        self.actSelect.setObjectName(u"actSelect")
        icon = QIcon()
        icon.addFile(u":/icons/icons/open1.png", QSize(), QIcon.Normal, QIcon.Off)
        self.actSelect.setIcon(icon)
        self.gridLayout_3 = QGridLayout(MyWindow)
        self.gridLayout_3.setObjectName(u"gridLayout_3")
        self.lableStatus = QLabel(MyWindow)
        self.lableStatus.setObjectName(u"lableStatus")

        self.gridLayout_3.addWidget(self.lableStatus, 7, 0, 1, 1)

        self.pBar = QProgressBar(MyWindow)
        self.pBar.setObjectName(u"pBar")
        self.pBar.setValue(0)
        self.pBar.setTextVisible(False)

        self.gridLayout_3.addWidget(self.pBar, 8, 0, 1, 1)

        self.groupBox = QGroupBox(MyWindow)
        self.groupBox.setObjectName(u"groupBox")
        self.gridLayout = QGridLayout(self.groupBox)
        self.gridLayout.setObjectName(u"gridLayout")
        self.editFile = QLineEdit(self.groupBox)
        self.editFile.setObjectName(u"editFile")

        self.gridLayout.addWidget(self.editFile, 0, 0, 1, 1)

        self.tbtnSelect = QToolButton(self.groupBox)
        self.tbtnSelect.setObjectName(u"tbtnSelect")

        self.gridLayout.addWidget(self.tbtnSelect, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)

        self.groupBox_2 = QGroupBox(MyWindow)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setAlignment(Qt.AlignLeading|Qt.AlignLeft|Qt.AlignTop)
        self.gridLayout_2 = QGridLayout(self.groupBox_2)
        self.gridLayout_2.setObjectName(u"gridLayout_2")
        self.rbtnSNJ401 = QRadioButton(self.groupBox_2)
        self.rbtnSNJ401.setObjectName(u"rbtnSNJ401")
        self.rbtnSNJ401.setChecked(True)

        self.gridLayout_2.addWidget(self.rbtnSNJ401, 0, 0, 1, 1)

        self.rbtnSNJ402 = QRadioButton(self.groupBox_2)
        self.rbtnSNJ402.setObjectName(u"rbtnSNJ402")

        self.gridLayout_2.addWidget(self.rbtnSNJ402, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 1)

        self.verticalSpacer = QSpacerItem(20, 40, QSizePolicy.Minimum, QSizePolicy.Expanding)

        self.gridLayout_3.addItem(self.verticalSpacer, 6, 0, 1, 1)

        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName(u"horizontalLayout")
        self.tbtnDo = QToolButton(MyWindow)
        self.tbtnDo.setObjectName(u"tbtnDo")
        self.tbtnDo.setMinimumSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.tbtnDo)

        self.tbtnClose = QToolButton(MyWindow)
        self.tbtnClose.setObjectName(u"tbtnClose")
        self.tbtnClose.setMinimumSize(QSize(25, 25))

        self.horizontalLayout.addWidget(self.tbtnClose)


        self.gridLayout_3.addLayout(self.horizontalLayout, 5, 0, 1, 1)

        self.groupBox_3 = QGroupBox(MyWindow)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.horizontalLayout_2 = QHBoxLayout(self.groupBox_3)
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.chkRead = QCheckBox(self.groupBox_3)
        self.chkRead.setObjectName(u"chkRead")
        self.chkRead.setChecked(True)

        self.horizontalLayout_2.addWidget(self.chkRead)

        self.chkWrite = QCheckBox(self.groupBox_3)
        self.chkWrite.setObjectName(u"chkWrite")
        self.chkWrite.setChecked(True)

        self.horizontalLayout_2.addWidget(self.chkWrite)


        self.gridLayout_3.addWidget(self.groupBox_3, 3, 0, 1, 1)

        self.groupBox_4 = QGroupBox(MyWindow)
        self.groupBox_4.setObjectName(u"groupBox_4")
        self.gridLayout_4 = QGridLayout(self.groupBox_4)
        self.gridLayout_4.setObjectName(u"gridLayout_4")
        self.rbtnOper = QRadioButton(self.groupBox_4)
        self.rbtnOper.setObjectName(u"rbtnOper")
        self.rbtnOper.setChecked(True)

        self.gridLayout_4.addWidget(self.rbtnOper, 0, 0, 1, 1)

        self.rbtnDebug = QRadioButton(self.groupBox_4)
        self.rbtnDebug.setObjectName(u"rbtnDebug")

        self.gridLayout_4.addWidget(self.rbtnDebug, 0, 1, 1, 1)


        self.gridLayout_3.addWidget(self.groupBox_4, 2, 0, 1, 1)


        self.retranslateUi(MyWindow)
        self.tbtnClose.clicked.connect(MyWindow.close)

        QMetaObject.connectSlotsByName(MyWindow)
    # setupUi

    def retranslateUi(self, MyWindow):
        MyWindow.setWindowTitle(QCoreApplication.translate("MyWindow", u"SNJ Code Deal", None))
        self.actSelect.setText(QCoreApplication.translate("MyWindow", u"\u9009\u62e9\u76ee\u5f55", None))
#if QT_CONFIG(tooltip)
        self.actSelect.setToolTip(QCoreApplication.translate("MyWindow", u"\u9009\u62e9\u76ee\u5f55", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(shortcut)
        self.actSelect.setShortcut(QCoreApplication.translate("MyWindow", u"Ctrl+O", None))
#endif // QT_CONFIG(shortcut)
        self.lableStatus.setText("")
        self.groupBox.setTitle(QCoreApplication.translate("MyWindow", u"\u9009\u62e9\u5f85\u70e7\u5f55\u7684fpga\u4e8c\u8fdb\u5236\u6587\u4ef6", None))
        self.tbtnSelect.setText(QCoreApplication.translate("MyWindow", u"\u9009\u62e9", None))
        self.groupBox_2.setTitle(QCoreApplication.translate("MyWindow", u"\u578b\u53f7\u9009\u62e9", None))
        self.rbtnSNJ401.setText(QCoreApplication.translate("MyWindow", u"SNJ401", None))
        self.rbtnSNJ402.setText(QCoreApplication.translate("MyWindow", u"SNJ402/SHX689", None))
        self.tbtnDo.setText(QCoreApplication.translate("MyWindow", u"\u8f6c\u6362", None))
        self.tbtnClose.setText(QCoreApplication.translate("MyWindow", u"\u9000\u51fa", None))
        self.groupBox_3.setTitle(QCoreApplication.translate("MyWindow", u"\u751f\u6210\u8bfb\u5199Pattern\u9009\u9879", None))
        self.chkRead.setText(QCoreApplication.translate("MyWindow", u"Read", None))
        self.chkWrite.setText(QCoreApplication.translate("MyWindow", u"Write", None))
        self.groupBox_4.setTitle(QCoreApplication.translate("MyWindow", u"\u751f\u6210pattern\u6a21\u5f0f(\u4ec5readRom)", None))
        self.rbtnOper.setText(QCoreApplication.translate("MyWindow", u"\u91cf\u4ea7", None))
        self.rbtnDebug.setText(QCoreApplication.translate("MyWindow", u"\u8c03\u8bd5(Debug)", None))
    # retranslateUi

