import sys
from PyQt4.QtGui import *
from PyQt4 import QtCore
from PyQt4.QtCore import Qt, SIGNAL


# import resources


class TitleBar(QDialog):
    def __init__(self, frame, parent=None):
        QWidget.__init__(self, parent)
        self.frame = frame
        self.minimize_btn = QToolButton(self)
        self.maximize_btn = QToolButton(self)
        self.close_btn = QToolButton(self)

        self.window_title = QLabel(self)
        self.maxNormal = False

        self.minimize_btn.clicked.connect(self.show_small)
        self.close_btn.clicked.connect(self.close)
        self.maximize_btn.clicked.connect(self.show_max_restore)
        self.set_ui()

    def set_ui(self):
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAutoFillBackground(True)
        self.setBackgroundRole(QPalette.Highlight)

        self.minimize_btn.setIcon(QIcon('min2.png'))
        self.maximize_btn.setIcon(QIcon('img/max.png'))
        self.close_btn.setIcon(QIcon('close.png'))

        self.close_btn.setFixedSize(15, 15)
        self.minimize_btn.setFixedSize(15, 15)
        self.maximize_btn.setFixedSize(10, 10)
        # self.setMinimumHeight(50)

        self.window_title.setText("Easy Wifi Windows")
        # self.setWindowTitle("Window Title")

        layout = QHBoxLayout(self)
        layout.addWidget(self.window_title)
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
        self.frame.showMinimized()

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
        print("self.frame", self.frame)
        if event.button() == Qt.LeftButton:
            self.frame.moving = True
            self.frame.offset = event.pos()

    def mouseMoveEvent(self, event):
        if self.frame.moving:
            self.frame.move(event.globalPos() - self.frame.offset)


class Frame(QFrame):
    def __init__(self, parent=None):
        QFrame.__init__(self, parent)
        self.already_close = False
        self.__m_mouse_down = False
        self.__m_titleBar = TitleBar(self)
        self.__m_content = QWidget()
        self.__layout = QVBoxLayout()
        self.set_ui()

    def set_ui(self):
        # self.setFrameShape(QFrame.StyledPanel)
        self.qss()
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setMouseTracking(True)
        vbox = QVBoxLayout(self)
        vbox.addWidget(self.__m_titleBar)
        vbox.setMargin(0)
        vbox.setSpacing(0)
        self.resize(300, 500)

        self.__layout.addWidget(self.__m_content)
        # self.layout.addWidget(QLabel("label from frame"))
        # layout.setMargin(10)
        # layout.setSpacing(0)
        vbox.addLayout(self.__layout)
        vbox.addStretch(1)

        # effect = QGraphicsDropShadowEffect(self)
        # effect.setOffset(10, 10)
        # effect.setBlurRadius(100)
        # self.setGraphicsEffect(effect)

        self.show()

    def layout_add(self, widget):
        self.__layout.addWidget(widget)

    def qss(self, css=None):
        print(2)
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

    def contentWidget(self):
        return self.__m_content

    def titleBar(self):
        return self.__m_titleBar

    def mousePressEvent(self, event):
        self.m_old_pos = event.pos()
        self.__m_mouse_down = event.button() == Qt.LeftButton

    def mouseMoveEvent(self, event):
        x = event.x()
        y = event.y()

    def mouseReleaseEvent(self, event):
        m_mouse_down = False

        # if __name__ == '__main__':
        #     app = QApplication(sys.argv)
        # box = Frame()
        # l = QVBoxLayout(box.contentWidget())
        # l.setMargin(10)
        # l.addWidget(main)
        # box.show()
        # app.exec_()
