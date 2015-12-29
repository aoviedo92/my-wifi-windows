from PyQt4.QtCore import QRect, QPropertyAnimation, SIGNAL
from PyQt4.QtGui import *
from PyQt4 import QtCore
import netsh

ACTION_BAR_HEIGHT = 50


class ActionBar(QFrame):
    def __init__(self, parent=None):
        super(ActionBar, self).__init__(parent)
        self.hotspot_btn = QPushButton("HotSpot")
        self.info_btn = QPushButton("Info")
        self.help_btn = QPushButton("Ayuda")

        self.btn_list = [self.help_btn, self.hotspot_btn, self.info_btn]

        layout = QHBoxLayout()
        layout.addWidget(self.hotspot_btn)
        layout.addWidget(self.info_btn)
        layout.addWidget(self.help_btn)
        layout.addStretch(1)
        self.setLayout(layout)
        self.move(0, 0)
        self.setFixedSize(300, ACTION_BAR_HEIGHT)
        self.setCursor(QCursor(QtCore.Qt.PointingHandCursor))
        self.setStyleSheet(self.set_qss())

    def active_btn(self, btn):
        normal_qss = """
            QPushButton{
                color: #8B0000;
            }
            QPushButton:hover{
                color: #fff;
                border-bottom: 2px solid #fff;
            }
        """
        active_qss = """
            QPushButton{
                color: #8B0000;
                border-bottom: 2px solid #fff;
            }
            QPushButton:hover{
                color: #fff;
                border-bottom: 2px solid #fff;
            }
        """
        for bt in self.btn_list:
            bt.setStyleSheet(normal_qss)
        btn.setStyleSheet(active_qss)
        # self.setStyleSheet(normal_qss)
        # for btn in self.btn_list:
        #     if btn.text() != text:
        #         btn.setStyleSheet(normal_qss)
        #     else:
        #         btn.setStyleSheet(active_qss)

    @staticmethod
    def set_qss():
        return """
            ActionBar{
                background-color: coral;
            }
            QPushButton{
                background-color: coral;
                border: 0;
                font: 14px;
                padding-bottom: 5px;
                margin-right: 10px;
            }
            QPushButton{
                color: #8B0000;
            }
            QPushButton:hover{
                color: #fff;
                border-bottom: 2px solid #fff;
            }
        """


class Toast(QFrame):
    def __init__(self, text, info, parent=None):
        super(Toast, self).__init__(parent)
        self.info = info
        toast_lbl = QPushButton(text)
        toast_lbl.setFixedSize(200, 100)
        layout = QVBoxLayout()
        layout.addWidget(toast_lbl)
        self.setLayout(layout)
        self.set_ui()

    def set_ui(self):
        color = "#C09853"
        background_color = "#FCF8E3"
        border_color = "#FBEED5"
        if self.info == "error":
            color = "#B94A48"
            background_color = "#F2DEDE"
            border_color = "#EED3D7"
        elif self.info == "success":
            color = "#468847"
            background_color = "#DFF0D8"
            border_color = "#D6E9C6"
        elif self.info == "info":
            color = "#3A87AD"
            background_color = "#D9EDF7"
            border_color = "#BCE8F1"
        self.setStyleSheet("""
            QPushButton{
                color: %s;
                background-color: %s;
                border: 1px solid %s;
                font: 14px;
                border-radius: 4px;
            }
            """ % (color, background_color, border_color))

    def animation_geometry(self, widget, init=(35, 250, 250, 200), end=(35, 250, 250, 200), finish=None, duration=2000):
        init_rect = QRect(init[0], init[1], init[2], init[3])
        end_rect = QRect(end[0], end[1], end[2], end[3])
        self.animation = QPropertyAnimation(widget, "geometry")
        self.animation.setStartValue(init_rect)
        self.animation.setEndValue(end_rect)
        self.animation.setDuration(duration)
        self.animation.start()
        if finish:
            self.connect(self.animation, SIGNAL('finished()'), finish)

    def show_toast(self, time_=3000):
        self.show()
        self.animation_geometry(self, finish=self.hide, duration=time_)


class Activity(QFrame):
    def __init__(self, parent=None):
        super(Activity, self).__init__(parent)
        self.hide()
        self.move(10, 60)
        self.linear_layout = QVBoxLayout()
        self.setLayout(self.linear_layout)


class Info(Activity):
    def __init__(self, parent=None):
        super(Info, self).__init__(parent)
        label = QLabel("info")
        self.linear_layout.addWidget(label)


class HotSpot(Activity):
    def __init__(self, parent=None):
        super(HotSpot, self).__init__(parent)
        self.ssid_edit = QLineEdit()
        self.key_edit = QLineEdit()
        self.btn = QPushButton("Iniciando...")
        self.ssid_edit.textEdited.connect(self.text_edited)
        self.key_edit.textEdited.connect(self.text_edited)

        self.set_ui()

    def set_ui(self):
        state = netsh.state_hosted_network()
        btn_text = "Iniciando..."
        if state == netsh.LANG_DICT['state_init']:
            btn_text = "Parar"
        elif state == netsh.LANG_DICT['state_not_init']:
            btn_text = "Iniciar"
        elif state == netsh.LANG_DICT['state_not_available']:
            btn_text = "Activar"
        self.btn_change_text(btn_text)

        self.ssid_edit.setPlaceholderText("Nombre SSID")
        self.key_edit.setPlaceholderText("Password")

        ssid, key = netsh.ssid_key()
        self.ssid_edit.setText(ssid)
        self.key_edit.setText(key)

        self.linear_layout.addWidget(self.ssid_edit)
        self.linear_layout.addWidget(self.key_edit)
        self.linear_layout.addWidget(self.btn)

        self.setStyleSheet(self.set_qss())

    def text_edited(self):
        if str(self.btn.text()) == "Parar":
            self.btn_change_text("Reiniciar")
        elif str(self.btn.text()) == "Iniciar":
            self.btn_change_text("Aplicar e iniciar")

    def btn_change_text(self, text):
        self.btn.setText(text)
        if text == "Iniciar":
            back_color = '#98FB98'
            text_color = "#3CB371"
        elif text == "Parar":
            back_color = "#FFCACA"
            text_color = "#FF9494"
        else:
            back_color = "#F1F1F1"
            text_color = "#555555"
        hover_color = text_color
        self.btn.setStyleSheet(
            """
            QPushButton{
                background-color: %s;
                color: %s;
            }
            QPushButton:hover{
                color: #fff;
                background-color: %s;
            }
            """ % (back_color, text_color, hover_color)
        )

    @staticmethod
    def set_qss():
        return """
            QLineEdit{
                border: 1px solid silver;
                height: 40px;
                width: 250px;
                padding-left: 5px;
                font: 14px;
            }
            QLineEdit:hover{
                border: 1px solid grey;
            }
            QPushButton{
                margin-top: 20px;
                height: 50px;
                border-radius: 4px;
                font: 16px;
                background-color: #98FB98;
                color: #3CB371;
            }
            QPushButton:hover{
                color: #fff;
                background-color: #3CB371;
            }
        """
