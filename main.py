import time
import sys
import ctypes
from PyQt4.QtGui import *
from frame import Frame
from activities import HotSpot, ActionBar, Info, Toast

APP_ID = 'dev$oviedo.my-wifi-windows-py3.3PyQt4.v1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.action_bar = ActionBar(self)
        self.hotspot = HotSpot(self)
        self.info = Info(self)
        self.hotspot.show()
        self.set_ui()

        self.current_activity = self.hotspot

        for btn in self.action_bar.btn_list:
            btn.clicked.connect(self.tab_clicked)

    def set_ui(self):
        self.setFixedSize(300, 500)
        self.setWindowIcon(QIcon(":/wifi"))

    def tab_clicked(self):
        text = str(self.sender().text())
        if text == "Ayuda":
            self.change_activity(self.help)
        elif text == "HotSpot":
            self.change_activity(self.hotspot)
        elif text == "Info":
            # self.info.set_text_browser(self.browser_text)
            self.change_activity(self.info)
        self.action_bar.active_btn(self.sender())

    def change_activity(self, activity_to, activity_from=None):
        if not activity_from:
            activity_from = self.current_activity
        activity_from.hide()
        activity_to.show()
        self.current_activity = activity_to


class UI(Frame):
    def __init__(self):
        Frame.__init__(self)
        self.main = Main()
        self.layout_add(self.main)


app = QApplication(sys.argv)
UI()
# app.setWindowIcon(QIcon(":/icon"))
app.exec_()
