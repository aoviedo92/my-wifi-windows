import time
import sys
import ctypes
from PyQt4.QtGui import *
from title_bar import Frame

APP_ID = 'dev$oviedo.my-wifi-windows-py3.3PyQt4.v1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.already_close = False
        self.btn_txt, self.browser_text = "", ""
        self.set_ui()

    def set_ui(self):
        self.setFixedSize(300, 500)


class UI(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.main = Main()
        self.layout_add(self.main)


app = QApplication(sys.argv)
UI()
app.setWindowIcon(QIcon(":/icon"))
app.exec_()
