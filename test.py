import sys
from PyQt4.QtCore import QDir, SIGNAL
from PyQt4.QtGui import *


class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        layout = QVBoxLayout()
        edit = QLineEdit()
        layout.addWidget(edit)
        self.setLayout(layout)
        self.connect(edit, SIGNAL("textEdited(QString)"), self.slot)
    def slot(self, qst):
        print(qst)


app = QApplication(sys.argv)
main = Main()
main.show()
app.exec_()