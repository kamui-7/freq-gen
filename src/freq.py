import csv
import requests
from PyQt5 import QtCore, QtWidgets
from gui import Ui_Form
import os
import globals
import textract
from urllib.parse import urlparse
import MeCab
from collections import Counter
from nltk import word_tokenize
import re

home = os.path.dirname(__file__)

class Worker(QtWidgets.QDialog):

    def __init__(self, files, *args):
        super().__init__()
        self.files = files
        self.resize(345, 70)
        self.progressBar = QtWidgets.QProgressBar(self)
        self.progressBar.setGeometry(QtCore.QRect(10, 20, 321, 23))
        self.progressBar.setWindowTitle("Adding...")
        self.progressBar.setMinimum(0)
        self.progressBar.setMaximum(0)

        self.freqthread = Files(self.files, *args)
        self.freqthread.start()
        self.freqthread.done.connect(lambda: self.close())

        self.show()

class Files(QtCore.QThread):
    done = QtCore.pyqtSignal(bool)

    def __init__(self, files, out, type, addoccur):
        super().__init__()
        self.files = files
        self.words = []
        self.type = type
        self.out = out
        self.addoccur = addoccur

    def run(self):
        for file in self.files:
            self.words += file.tokenize()
        self.gen_freq()
        self.done.emit(True)

    def gen_freq(self):
        freqTitle = os.path.basename(self.files[0].filepath)[
            :-4] + "_Frequency_List" + self.type
        counter = Counter(self.words)
        trashre = re.compile(
            r"^['\"{}!(:/.\\0-9%^&*@#$_\-~`|+•『』〔〕［］\[\]｛｝｟｠〈〉。、>< ,・=;※ー【】〖〗〘〙)a-zA-Z]{0,2}$")
        mc = counter.most_common()
        mc = {k: v for k, v in mc if not bool(re.findall(trashre, k))}
        freqinfo = [k for k, _ in mc.items()]
        with open(os.path.join(self.out, freqTitle), "w", encoding="utf8") as freq:
            if self.type == ".csv":
                obj = csv.writer(freq)
                for _, row in enumerate(freqinfo):
                    if self.addoccur:
                        obj.writerow([row, counter[row]])
                    else:
                        obj.writerow([row, ""])
            else:
                if self.addoccur:
                    freq.write('\n'.join(['\t'.join([k, str(v)])
                               for k, v in counter.most_common()]))
                else:
                    freq.write('\n'.join(freqinfo))


class File(QtCore.QThread):

    def __init__(self, filepath, lang):
        super().__init__()
        self.filepath = filepath
        self.lang = lang
        self.isweb = self.check_web()

        if self.lang == "japanese":
            self.wakati = MeCab.Tagger("-Owakati")

    def extract_text(self):
        if self.isweb:
            with open(os.path.join(home, "temp.html"), "wb") as f:
                f.write(requests.get(self.filepath).content)
                self.filepath = os.path.join(home, "temp.html")

        text = textract.process(self.filepath, encoding="utf-8")
        if self.isweb:
            os.remove(os.path.join(home, "temp.html"))
        return text.decode('utf-8')

    def check_web(self):
        try:
            _ = requests.get(self.filepath)
        except:
            return False
        else:
            return True

    def tokenize(self):
        if self.lang != "japanese":
            tokenized = word_tokenize(self.extract_text())
        else:
            tokenized = self.wakati.parse(self.extract_text()).split()
        return tokenized


class MainWindow(Ui_Form):

    def __init__(self):
        super().__init__()

    def setupUi(self):
        self.choosedirbutton.clicked.connect(self.choosedir)
        self.generate.clicked.connect(
            lambda: self.genfreq(self.filetype.currentText()))
        self.remove.clicked.connect(self.deleteItem)
        self.clear.clicked.connect(self.clearList)
        self.lang.addItems(globals.supportedlangs)

    def choosedir(self):
        self.dir = str(QtWidgets.QFileDialog.getExistingDirectory(
            self, "Output Folder"))
        self.outpath.setText(self.dir)

    def genfreq(self, filetype):
        files = [str(self.filewidget.item(i).text())
                 for i in range(self.filewidget.count())] + [self.url.text()]
        if len(files) == 1 and not files[0]:
            self.error("No files have been selected")
            return
        if not os.path.exists(self.outpath.text()):
            self.error("Choose an output directory first")
            return

        files = [File(filename, self.lang.currentText())
                 for filename in files if filename]
        worker = Worker(files, self.dir, filetype.currentText(), self.addoccur.isChecked())

    def error(self, text, title="Error has occured"):
        dialog = QtWidgets.QMessageBox()
        dialog.setWindowTitle(title)
        dialog.setText(text)
        dialog.setIcon(QtWidgets.QMessageBox.Warning)
        dialog.exec_()

    def deleteItem(self):
        listItems = self.filewidget.selectedItems()
        if not listItems:
            self.filewidget.setCurrentItem(self.filewidget.item(0))
            if self.filewidget.count() > 0:
                self.deleteItem()

        for item in listItems:
            self.filewidget.takeItem(self.filewidget.row(item))

    def clearList(self):
        self.filewidget.setCurrentItem(self.filewidget.item(0))
        for _ in range(self.filewidget.count()):
            self.filewidget.clear()

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    screen = MainWindow()
    screen.setupUi()
    screen.show()
    sys.exit(app.exec_())
