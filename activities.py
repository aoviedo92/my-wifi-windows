import random
import re
import threading
import time
from PyQt4.QtCore import QRect, QPropertyAnimation, SIGNAL
from PyQt4.QtGui import *
from PyQt4 import QtCore
import netsh

LBL_STYLE = """#info{
            color: #777;
            font: 12px;
        }
        #title{
            color: #555;
            font: 18px;
        }"""


class ActionBar(QFrame):
    ACTION_BAR_HEIGHT = 50

    def __init__(self, parent=None):
        super(ActionBar, self).__init__(parent)
        self.hotspot_btn = QPushButton("HotSpot")
        self.clients_btn = QPushButton()  # este btn toma el text dinamicam desde UI()
        self.info_btn = QPushButton("Info")
        self.help_btn = QPushButton("Ayuda")

        self.btn_list = [self.help_btn, self.hotspot_btn, self.info_btn, self.clients_btn]

        layout = QHBoxLayout()
        layout.addWidget(self.hotspot_btn)
        layout.addWidget(self.clients_btn)
        layout.addWidget(self.info_btn)
        layout.addWidget(self.help_btn)
        layout.addStretch(1)
        self.setLayout(layout)
        self.move(0, 0)
        self.setFixedSize(300, self.ACTION_BAR_HEIGHT)
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
        self.cant_users = 0
        self.config_lbl = QLabel("Configuración de la red hospedada")
        self.config_lbl_info = QLabel()
        self.state_lbl = QLabel("Estado de la red hospedada")
        self.state_lbl_info = QLabel()
        self.users_lbl = QLabel()
        self.users_lbl_info = QLabel()
        self.linear_layout.addWidget(self.config_lbl)
        self.linear_layout.addWidget(self.config_lbl_info)
        self.linear_layout.addWidget(self.state_lbl)
        self.linear_layout.addWidget(self.state_lbl_info)
        self.set_ui()

        thread = threading.Thread(target=self.run)
        thread.setDaemon(True)
        thread.start()

    def run(self):
        while True:
            info = netsh.HOSTED_NETWORK_INFO.copy()
            # print('INFO', info)
            self.config_lbl_info.setText(
                "Modo:\t{modo}\n"
                "SSID:\t{ssid}\n"
                "KEY:\t{key}\n"
                "Máximo clientes:\t{max_clientes}\n"
                "Autenticación:\t{autenticacion}\n"
                "Cifrado:\t{cifrado}".format(**info))
            try:
                status = "BSSID:\t{bssid}\n" \
                         "Radio:\t{radio}\n" \
                         "Canal:\t{canal}\n".format(**info)
            except KeyError:
                status = ""

            self.state_lbl_info.setText(
                "Estado:\t{state}\n".format(**info) + status)

            time.sleep(5)

    def upd_info(self):
        show = netsh.show_hosted_network()

    def set_ui(self):
        # self.set_text_browser()
        self.config_lbl.setObjectName("title")
        self.config_lbl_info.setObjectName("info")
        self.state_lbl.setObjectName("title")
        self.state_lbl_info.setObjectName("info")
        self.users_lbl.setObjectName("title")
        self.users_lbl_info.setObjectName("info")
        self.setStyleSheet("""

        Info{
            background-color: #fff;
        }
        """ + LBL_STYLE)


class HotSpot(Activity):
    TOAST_TEXT = ""
    TOAST_COLOR = ""

    def __init__(self, parent=None):
        super(HotSpot, self).__init__(parent)
        self.ssid_edit = QLineEdit()
        self.key_edit = QLineEdit()
        self.btn = QPushButton("...")
        self.connect(self.btn, SIGNAL("clicked()"), self.btn_clicked)
        self.connect(self.key_edit, SIGNAL("textChanged(QString)"), self.text_edited)
        self.connect(self.ssid_edit, SIGNAL("textChanged(QString)"), self.text_edited)
        self.set_ui()

        thread = threading.Thread(target=self.upd_ui)
        thread.setName("HotSpotThread")
        thread.setDaemon(True)
        thread.start()

    def validate(self):
        try:
            ssid = str(self.ssid_edit.text())
            key = str(self.key_edit.text())
            if ssid.strip() == "" or key.strip() == "":
                self.TOAST_TEXT = "LLene todos los campos"
                self.TOAST_COLOR = "error"
                return False
            if len(key) < 8:
                self.TOAST_TEXT = "El password debe tener \n8 o más caracteres"
                self.TOAST_COLOR = "error"
                return False
            if ssid.find(" ") != -1 or key.find(" ") != -1:
                self.TOAST_TEXT = "Los datos no deben tener\nespacios"
                self.TOAST_COLOR = "error"
                return False
            return True
        except (UnicodeDecodeError, UnicodeEncodeError):
            self.TOAST_TEXT = "Los datos deben ser \ncadenas ASCII"
            self.TOAST_COLOR = "error"
            return False

    def btn_clicked(self):
        if not self.validate():
            self.emit_toast()
            return
        info, text = "", ""
        self.btn.setEnabled(False)

        btn_text = self.btn.text()
        if btn_text == "Iniciar":
            self.btn.setText("Iniciando...")
            start = netsh.start_hosted_network()
            if start:
                text = "Se inició correctamente\nla red hospedada"
                info = "info"
            else:
                text = "No se pudo iniciar\ncorrectamente la red hospedada"
                info = "error"
        elif btn_text == "Parar":
            self.btn.setText("Deteniendo...")
            stop = netsh.stop_hosted_network()
            if stop:
                text = "Se detuvo la red hospedada"
                info = "info"
            else:
                text = "No se pudo detener\nla red hospedada"
                info = "info"
        elif btn_text == "Activar":
            self.btn.setText("Activando...")
            if self.ssid_edit.text() == netsh.HOSTED_NETWORK_INFO['ssid'] and \
                            self.key_edit.text() == netsh.HOSTED_NETWORK_INFO['key']:
                activate = netsh.only_activate_hosted_network()
                if activate:  # ahora iniciarla
                    text = "El modo de red hospedada\nse estableció en permitir"
                    info = "info"
                else:
                    text = "No se pudo activar\nla red hospedada"
                    info = "error"
            else:
                # si se cambio el ssid o key, entonces aplicar los cambios en la red h.
                set_hosted_network = netsh.set_hosted_network(self.ssid_edit.text(), self.key_edit.text())
                if set_hosted_network:
                    text = "Se ha activado la red hospedada\ny establecido los nuevos\nparámetros"
                    info = "info"
                else:
                    text = "No se ha activado la red hospedada"
                    info = "info"
        elif btn_text == "Reiniciar":
            self.btn.setText("Reiniciando...")
            text = "No se ha reiniciado\ncorrectamente la red"
            info = "error"
            ctrl = netsh.stop_hosted_network()
            if ctrl:
                ctrl = netsh.set_hosted_network(self.ssid_edit.text(), self.key_edit.text())
            if ctrl:
                ctrl = netsh.start_hosted_network()
            if ctrl:
                text = "Se ha reiniciado\nla red"
                info = "info"
        elif btn_text == "Aplicar e iniciar":
            self.btn.setText("Aplicando...")
            text = "No se han podido\nestablecer los nuevos cambios"
            info = "error"
            ctrl = netsh.set_hosted_network(self.ssid_edit.text(), self.key_edit.text())
            if ctrl:
                ctrl = netsh.start_hosted_network()
            if ctrl:
                text = "Se han aplicado los cambios\na la red"
                info = "info"

        self.TOAST_TEXT = text
        self.TOAST_COLOR = info

    def set_ui(self):
        self.ssid_edit.setPlaceholderText("Nombre SSID")
        self.key_edit.setPlaceholderText("Password")

        self.ssid_edit.setText(netsh.HOSTED_NETWORK_INFO['ssid'])
        self.key_edit.setText(netsh.HOSTED_NETWORK_INFO['key'])

        self.linear_layout.addWidget(self.ssid_edit)
        self.linear_layout.addWidget(self.key_edit)
        self.linear_layout.addWidget(self.btn)

        self.setStyleSheet(self.set_qss())

    def emit_toast(self):
        if self.TOAST_TEXT and self.TOAST_COLOR:
            self.emit(SIGNAL("toast"), self.TOAST_TEXT, self.TOAST_COLOR)
            self.TOAST_COLOR, self.TOAST_TEXT = "", ""

    def take_action(self, btn_text, current_btn_text, btn_text_list, click_again=False):
        """
        tomar accion a partir del btn-text: es colocar el nombre correcto para el estado correcto
        :param btn_text: estado de la red actual segun netsh.HOSTED_NETWORK_INFO['state'] (Parar, Iniciar, Activar)
        :param current_btn_text: si el btn-text actual es uno de los gerundios por ej (Iniciando..., Activando...) es pq hay procesamiento, y no se puede establecer en btn-text al estado actual
        :param btn_text_list: Lista de estados a comprobar, si concuerda uno, se acabo el procesam y se establece como btn-text
        :param click_again: Si es necesaro simular un click con el nuevo btn-text
        :return: btn_text, process
        """
        process = False  # mientras se este procesando los cmd de netsh, deshabilitar btn
        if self.btn.text() == current_btn_text:
            self.btn.setEnabled(False)
            process = True
            for item in btn_text_list:
                if btn_text == item:
                    self.btn_change_text(btn_text)
                    self.btn.setEnabled(True)
                    if click_again:
                        self.btn_clicked()
                    process = False
        return process

    def upd_ui(self):
        """
        actualiza cada 5s el estado del btn
        """
        while True:
            self.btn.setEnabled(True)

            # comprobar estado de la red, para actualiz el btn
            state = netsh.HOSTED_NETWORK_INFO['state']
            # print('sta', state)
            if state == netsh.LANG_DICT['state_init']:
                btn_text = "Parar"
            elif state == netsh.LANG_DICT['state_not_init']:
                btn_text = "Iniciar"
            elif state == netsh.LANG_DICT['state_not_available']:
                btn_text = "Activar"

            process = self.take_action(btn_text, "Activando...", ["Iniciar"], click_again=True)
            if not process:
                process = self.take_action(btn_text, "Aplicando...", ["Iniciar"], click_again=True)
            if not process:
                process = self.take_action(btn_text, "Iniciando...", ["Parar", "Activar"])
            if not process:
                process = self.take_action(btn_text, "Deteniendo...", ["Iniciar"])
            if not process:
                process = self.take_action(btn_text, "Reiniciando...", ["Parar"])

            # cuand btn es "reiniciar" o "aplicar e iniciar" evitar q se cambie el btn-text por el estad actual
            if self.btn.text() == "Aplicar e iniciar":
                # Aqui no hay procesamiento, pero para evitar q el hilo cambie el text de btn
                # establecemos process True
                # Cuand el estado es No iniciado, y se modifica ssid o key
                process = True
            if self.btn.text() == "Reiniciar":
                # Cuando estado es Iniciado y se modifica ssid o key
                process = True

            if not process:  # si no hay proc en backgr
                self.btn_change_text(btn_text)  # establec el btn-text actual
                self.emit_toast()  # siemre q process=False se notifica q ocurrio

            # print('btn', btn_text)
            time.sleep(5)

    def text_edited(self):
        if self.btn.text() == "Parar":
            self.btn_change_text("Reiniciar")
        elif self.btn.text() == "Reiniciar":
            if self.ssid_edit.text() == netsh.HOSTED_NETWORK_INFO['ssid'] and \
                            self.key_edit.text() == netsh.HOSTED_NETWORK_INFO['key']:
                self.btn_change_text("Parar")
        elif self.btn.text() == "Iniciar":
            self.btn_change_text("Aplicar e iniciar")
        elif self.btn.text() == "Aplicar e iniciar":
            if self.ssid_edit.text() == netsh.HOSTED_NETWORK_INFO['ssid'] and \
                            self.key_edit.text() == netsh.HOSTED_NETWORK_INFO['key']:
                self.btn_change_text("Iniciar")

    def btn_change_text(self, text):
        self.btn.setText(text)
        # todo cambiarle el qss dinamicamente a btn hace q la app stop and crash
        # if text == "Iniciar":
        #     back_color = '#98FB98'
        #     text_color = "#3CB371"
        # elif text == "Parar":
        #     back_color = "#FFCACA"
        #     text_color = "#FF9494"
        # else:
        #     back_color = "#F1F1F1"
        #     text_color = "#555555"
        # hover_color = text_color
        # self.btn.setStyleSheet(
        #     """
        #     QPushButton{
        #         background-color: %s;
        #         color: %s;
        #     }
        #     QPushButton:hover{
        #         color: #fff;
        #         background-color: %s;
        #     }
        #     """ % (back_color, text_color, hover_color)
        # )

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


class Clients(Activity):
    def __init__(self, parent=None):
        super(Clients, self).__init__(parent)
        self.title_lbl = QLabel("Clientes conectados")
        self.clients_lbl = QLabel()
        self.linear_layout.addWidget(self.title_lbl)
        self.linear_layout.addWidget(self.clients_lbl)
        self.set_ui()

    def set_ui(self):
        self.title_lbl.setObjectName("title")
        self.clients_lbl.setObjectName("info")
        self.setStyleSheet(LBL_STYLE)
