import globals
import os
from PyQt5 import QtCore, QtGui, QtWidgets

class ThumbListWidget(QtWidgets.QListWidget):

    def __init__(self):
        super().__init__()
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dragMoveEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(QtCore.Qt.CopyAction)
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        files = [u.toLocalFile() for u in event.mimeData().urls() if
                 u.toLocalFile().split(".")[-1] in globals.supportedtypes]
        self.addItems(files)

class Ui_Form(QtWidgets.QWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName("self")
        self.resize(633, 435)
        self.verticalLayout = QtWidgets.QVBoxLayout(self)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(self)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.filewidget = ThumbListWidget()
        self.filewidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.filewidget)
        self.label_3 = QtWidgets.QLabel(self)
        self.label_3.setObjectName("label_3")
        spacerItem = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.horizontalLayout_4.addItem(spacerItem)
        self.remove = QtWidgets.QPushButton(self)
        self.remove.setObjectName("remove")
        self.horizontalLayout_4.addWidget(self.remove)
        self.clear = QtWidgets.QPushButton(self)
        self.clear.setObjectName("clear")
        self.horizontalLayout_4.addWidget(self.clear)
        self.lang = QtWidgets.QComboBox(self)
        self.horizontalLayout_4.addWidget(self.lang)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.verticalLayout.addWidget(self.label_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.url = QtWidgets.QLineEdit(self)
        self.url.setObjectName("lineEdit_2")
        self.horizontalLayout_2.addWidget(self.url)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.label = QtWidgets.QLabel(self)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.outpath = QtWidgets.QLineEdit(self)
        self.outpath.setObjectName("lineEdit")
        self.horizontalLayout.addWidget(self.outpath)
        self.choosedirbutton = QtWidgets.QToolButton(self)
        self.choosedirbutton.setObjectName("toolButton")
        self.horizontalLayout.addWidget(self.choosedirbutton)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.addoccur = QtWidgets.QCheckBox(self)
        self.addoccur.setObjectName("checkBox")
        self.horizontalLayout_3.addWidget(self.addoccur)
        spacerItem1 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.label_4 = QtWidgets.QLabel(self)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        self.filetype = QtWidgets.QComboBox(self)
        self.filetype.setObjectName("filetypes")
        self.filetype.addItem("")
        self.filetype.addItem("")
        self.horizontalLayout_3.addWidget(self.filetype)
        spacerItem2 = QtWidgets.QSpacerItem(
            40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem2)
        self.label_5 = QtWidgets.QLabel(self)
        self.label_5.setObjectName("label_5")
        self.horizontalLayout_3.addWidget(self.label_5)
        self.generate = QtWidgets.QPushButton(self)
        self.generate.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.generate)
        self.verticalLayout.addLayout(self.horizontalLayout_3)

        self.retranslateUi()

    def retranslateUi(self):
        _translate = QtCore.QCoreApplication.translate
        self.remove.setText(_translate("self", "Remove"))
        self.clear.setText(_translate("self", "Clear"))
        self.setWindowTitle(_translate("self", "Frequency List Generator"))
        self.label_2.setText(_translate(
            "self", "Drag and drop files from your computer here"))
        self.label_3.setText(_translate("self", "Website URL"))
        self.label.setText(_translate("self", "Output Directory"))
        self.choosedirbutton.setText(_translate("self", "..."))
        self.label_4.setText(_translate("self", "Output File Type"))
        self.filetype.setItemText(0, _translate("self", ".txt"))
        self.filetype.setItemText(1, _translate("self", ".csv"))
        self.label_5.setText(_translate(
            "self", "Start Generating Frequency List"))
        self.generate.setText(_translate("self", "Generate"))
        self.addoccur.setText(_translate("Form", "Keep Occurence"))

def run():
    import sys
    app = QtWidgets.QApplication(sys.argv)
    screen = Ui_Form()
    screen.show()
    sys.exit(app.exec_())
