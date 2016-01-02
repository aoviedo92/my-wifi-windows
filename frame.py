import threading

import time
from PyQt4 import QtGui

import netsh
from PyQt4.QtCore import Qt
from PyQt4.QtGui import *

from activities import HotSpot
from res import resources

TITLE = "Easy Wifi Windows"


class TitleBar(QDialog):
    def __init__(self, frame, parent=None):
        QWidget.__init__(self, parent)
        self.frame = frame
        self.minimize_btn = QToolButton(self)
        self.maximize_btn = QToolButton(self)
        self.close_btn = QToolButton(self)

        self.maxNormal = False

        self.minimize_btn.clicked.connect(self.show_small)
        self.close_btn.clicked.connect(self.close)
        self.maximize_btn.clicked.connect(self.show_max_restore)
        self.set_ui()

    def set_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Highlight)

        self.minimize_btn.setIcon(QIcon(':/min'))
        self.maximize_btn.setIcon(QIcon('img/max.png'))
        self.close_btn.setIcon(QIcon(':/close'))

        self.close_btn.setFixedSize(15, 15)
        self.minimize_btn.setFixedSize(15, 15)
        self.maximize_btn.setFixedSize(10, 10)

        window_title = QLabel(self)
        window_title.setText(TITLE)

        layout = QHBoxLayout(self)
        layout.addWidget(window_title)
        layout.addWidget(self.minimize_btn)
        # layout.addWidget(self.maximize_btn)
        layout.addWidget(self.close_btn)
        layout.insertStretch(1, 500)
        layout.setSpacing(3)
        self.qss()
        # self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def qss(self, css=None):
        if not css:
            css = """
            QPushButton{
                border: 0;
            }
            QWidget{
                Background: coral;
                color:white;
                font:12px bold;
                font-weight:bold;
                border-radius: 1px;
                height: 11px;
            }
            /*QDialog{
                Background-image:url('icon.ico');
                font-size:12px;
                color: black;
            }*/
            QToolButton{
                Background:coral;
                font-size:11px;
                border-radius: 7px;
            }
            QToolButton:hover{
                Background:n orange;
                font-size:11px;
            }
            """
        self.setStyleSheet(css)

    def show_small(self):
        self.frame.showMinimized()  # minimiza a la taskbar
        self.frame.hide()  # lo minimiza al systray

    def show_max_restore(self):
        if self.maxNormal:
            self.frame.showNormal()
            self.maxNormal = False
            self.maximize_btn.setIcon(QIcon('max.png'))

        else:
            self.frame.showMaximized()
            self.maxNormal = True
            self.maximize_btn.setIcon(QIcon('max2.png'))

    def close(self):
        self.frame.already_close = True
        self.frame.close()

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.frame.moving = True
            self.frame.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.frame.moving:
            self.frame.move(event.globalPos() - self.frame.offset)





class Frame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.mouse_down = False
        self.title_bar = TitleBar(self)
        self.content = QWidget()
        self.layout = QVBoxLayout()
        self.set_ui()
        self.createTrayIcon()


    def set_ui(self):
        # self.setFrameShape(QFrame.StyledPanel)
        self.qss()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.title_bar)
        vbox.setMargin(0)
        vbox.setSpacing(0)
        self.resize(300, 500)

        self.layout.addWidget(self.content)
        # self.layout.addWidget(QLabel("label from frame"))
        # layout.setMargin(10)
        # layout.setSpacing(0)
        vbox.addLayout(self.layout)
        vbox.addStretch(1)

        # effect = QGraphicsDropShadowEffect(self)
        # effect.setOffset(10, 10)
        # effect.setBlurRadius(100)
        # self.setGraphicsEffect(effect)

        self.show()

    def layout_add(self, widget):
        self.layout.addWidget(widget)

    def qss(self, css=None):
        if not css:
            css = """
            Frame{
                Background:  #fff;
                color:white;
                font:13px;
                font-weight:bold;
                border: 1px solid #d4d4d4;
                }
            """
        self.setStyleSheet(css)

        # def contentWidget(self):
        #     return self.content

        # def titleBar(self):
        #     return self.title_bar

        # def mousePressEvent(self, event):
        #     self.m_old_pos = event.pos()
        #     self.mouse_down = event.button() == Qt.LeftButton

        # def mouseMoveEvent(self, event):
        #     x = event.x()
        #     y = event.y()
        #
        # def mouseReleaseEvent(self, event):
        #     m_mouse_down = False

    def createTrayIcon(self):
        # todo crear acciones: hotspot, info, ayuda

        minimizeAction = QAction("HotSpot", self, triggered=self.show)
        maximizeAction = QAction("Ma&ximize", self, triggered=self.showMaximized)
        restoreAction = QAction("&Restore", self, triggered=self.showNormal)
        quitAction = QAction("&Quit", self, triggered=QtGui.qApp.quit)

        trayIconMenu = QMenu(self)
        trayIconMenu.addAction(minimizeAction)
        trayIconMenu.addAction(maximizeAction)
        trayIconMenu.addAction(restoreAction)
        trayIconMenu.addSeparator()
        trayIconMenu.addAction(quitAction)

        self.trayIcon = QSystemTrayIcon(self)
        self.trayIcon.setContextMenu(trayIconMenu)
        self.set_icon_by_state_hosted_network()

        self.trayIcon.messageClicked.connect(self.message_clicked)
        self.trayIcon.activated.connect(self.icon_activated)
        self.trayIcon.show()

    def message_clicked(self):
        QMessageBox.information(self, "message title",
                                "message body", "button text")

    def icon_activated(self, reason):
        if reason == QtGui.QSystemTrayIcon.Trigger:
            # self.title_bar.frame.showNormal()
            self.show()
        if reason == QSystemTrayIcon.MiddleClick:
            self.set_icon_by_state_hosted_network()
            # self.show_message()

    def show_message(self):
        titleEdit = QLineEdit("titulo")
        bodyEdit = QTextEdit()
        bodyEdit.setPlainText("message.")
        icon = QSystemTrayIcon.MessageIcon(QSystemTrayIcon.Information)

        self.trayIcon.showMessage(titleEdit.text(),
                                  bodyEdit.toPlainText(), icon,
                                  5000)

    def set_icon_by_state_hosted_network(self, state=None):
        """
        establece el icono del systray segun el estado de la red hospedada.
        no iniciada --> icono gris
        iniciada --> icono color
        :param state: uno de los estados posibles
        """
        if state == netsh.LANG_DICT['state_init']:
            self.trayIcon.setIcon(QIcon(':/wifi'))
        elif state == netsh.LANG_DICT['state_not_init']:
            self.trayIcon.setIcon(QIcon(':/wifi-off'))
        else:
            self.trayIcon.setIcon(QIcon(':/wifi-off'))
