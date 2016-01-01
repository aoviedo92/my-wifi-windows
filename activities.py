import random
import re
import threading
import time
from PyQt4.QtCore import QRect, QPropertyAnimation, SIGNAL
from PyQt4.QtGui import *
from PyQt4 import QtCore
import netsh

RUN = True


class ActionBar(QFrame):
    ACTION_BAR_HEIGHT = 50

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
        # self.browser = QTextBrowser()
        # self.browser.setFixedSize(270, 350)
        self.config_lbl = QLabel("Configuración de la red hospedada")
        self.state_lbl = QLabel("Estado de la red hospedada")
        self.users_lbl = QLabel("Usuarios conectados")
        # self.linear_layout.addWidget(self.browser)
        self.linear_layout.addWidget(self.config_lbl)
        self.linear_layout.addWidget(self.state_lbl)
        self.linear_layout.addWidget(self.users_lbl)
        # self.browser.append('<h1>texto</h1>')
        self.set_ui()

        # thread = threading.Thread(target=self.run)
        # self.thread = threading.Thread(target=self.run)
        # thread.setName("browser")
        # self.thread.setName("InfoThread")
        # self.thread.setDaemon(True)
        # self.thread.start()

    def run(self):
        while True:
            # self.set_text_browser()
            # show = netsh.show_hosted_network()
            # print(show)
            # self.label.setText(str(random.randint(0, 100)))
            # print(self.thread._stopped)
            threads = threading.enumerate()
            # print(threads)
            time.sleep(5)

    def upd_info(self):
        show = netsh.show_hosted_network()

    # def set_text_browser(self):
    #     self.browser.clear()
    #     show = netsh.show_hosted_network()
    #     table = "<table width='250'>"
    #     for line in show:
    #         if line.find("--------") != -1:
    #             continue
    #         elif line.find(" : ") != -1 or line.find(": ") != -1:
    #             cols = line.split(":")
    #             row = """
    #                 <tr>
    #                 <td align="left">%s</td>
    #                 <td align="left">%s</td>
    #                 </tr>
    #                 """ % (cols[0].strip(), cols[1].strip())
    #             table += row
    #         elif re.match('^.{2}:.{2}.*\s+Autenticado', line):
    #             row = "<tr><td colspan=2><span style='color: coral'>%s</span></td></tr>" % line
    #             table += row
    #         else:
    #             row = "<tr><td colspan=2><h3>%s</h3></td></tr>" % line
    #             table += row
    #     table += "</table>"
    #     self.browser.append(table)

    def set_ui(self):
        # self.set_text_browser()
        self.config_lbl.setObjectName("title")
        self.state_lbl.setObjectName("title")
        self.users_lbl.setObjectName("title")
        self.setStyleSheet("""
        #title{
            color: #ccc;
            font: 18px;
        }
        Info{
            background-color: #fff;
        }
        QTextBrowser{
            border: 0;
        }
        """)


class HotSpot(Activity):
    TOAST_TEXT = ""
    TOAST_COLOR = ""

    def __init__(self, parent=None):
        super(HotSpot, self).__init__(parent)
        self.ssid_edit = QLineEdit()
        self.key_edit = QLineEdit()
        self.btn = QPushButton("...")
        self.connect(self.btn, SIGNAL("clicked()"), self.btn_clicked)
        self.ssid_edit.textEdited.connect(self.text_edited)
        self.key_edit.textEdited.connect(self.text_edited)
        # self.connect(self.key_edit, SIGNAL("textEdited()"), self.text_edited)
        # self.connect(self.ssid_edit, SIGNAL("textEdited"), self.text_edited)
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
                print("ver", text, info)
            else:
                text = "No se pudo iniciar\ncorrectamente la red hospedada"
                info = "error"
        elif btn_text == "Parar":
            self.btn.setText("Deteniendo...")
            stop = netsh.stop_hosted_network()
            self.cmd_status = stop
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
                self.cmd_status = activate
                if activate:  # ahora iniciarla
                    # netsh.start_hosted_network()
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

        self.TOAST_COLOR = info
        self.TOAST_TEXT = text
        print('fin', self.TOAST_COLOR, self.TOAST_TEXT)

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
        print("emit")
        if self.TOAST_TEXT and self.TOAST_COLOR:
            print('toasts', self.TOAST_TEXT, self.TOAST_COLOR)
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
        process = False
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
            process = False  # mientras se este procesando los cmd de netsh, deshabilitar btn
            self.btn.setEnabled(True)

            # comprobar estado de la red, para actualiz el btn
            state = netsh.HOSTED_NETWORK_INFO['state']
            print('sta', state)
            if state == netsh.LANG_DICT['state_init']:
                btn_text = "Parar"
            elif state == netsh.LANG_DICT['state_not_init']:
                btn_text = "Iniciar"
            elif state == netsh.LANG_DICT['state_not_available']:
                btn_text = "Activar"

            process = self.take_action(btn_text, "Activando...", ["Iniciar"], click_again=True)
            # estos bloques if corresponden a los distintos estados del btn mientras haya procesamiento.
            # if self.btn.text() == "Activando...":  # texto actual
            #     self.btn.setEnabled(False)
            #     process = True
            #     if btn_text == "Iniciar":
            #         self.btn_change_text(btn_text)  # cambiar a Iniciar
            #         self.btn.setEnabled(True)
            #         self.btn_clicked()  # para q funcione como si fuera un clic, al comprobar q el btn text es Iniciar, iniciara la red
            #         process = False  # terminado el procesamiento, se emite un toast con la noticia

            process = self.take_action(btn_text, "Iniciando...", ["Parar", "Activar"])
            # if self.btn.text() == "Iniciando...":
            #     # si esta iniciando, no se puede habilitar hasta q termine
            #     process = True
            #     self.btn.setEnabled(False)
            #     if btn_text == "Parar":  # si el estado es Iniciado, el btn_text sera Parar
            #         self.btn_change_text(btn_text)  # entonces si la red ya inicio, actualiz el btn-text
            #         self.btn.setEnabled(True)  # lo habilitamos
            #         process = False  # y emitimos Toast con la notificacion
            #     if btn_text == "Activar":  # caso en q por backgr se deshabilite la red
            #         self.btn_change_text(btn_text)
            #         self.btn.setEnabled(True)
            #         process = False

            process = self.take_action(btn_text, "Deteniendo...", ["Iniciar"])
            # if self.btn.text() == "Deteniendo...":  # el mismo proc para detener la red
            #     self.btn.setEnabled(False)
            #     process = True
            #     if btn_text == "Iniciar":
            #         self.btn_change_text(btn_text)
            #         self.btn.setEnabled(True)
            #         process = False

            process = self.take_action(btn_text, "Reiniciando...", ["Parar"])
            # if self.btn.text() == "Reiniciando...":
            #     self.btn.setEnabled(False)
            #     process = True
            #     if btn_text == "Parar":
            #         self.btn_change_text(btn_text)
            #         self.btn.setEnabled(True)
            #         process = False

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
                # self.cmd_status = False
            print('btn', btn_text)
            time.sleep(5)

    def text_edited(self):
        if str(self.btn.text()) == "Parar":
            self.btn_change_text("Reiniciar")
        elif str(self.btn.text()) == "Iniciar":
            self.btn_change_text("Aplicar e iniciar")

    def btn_change_text(self, text):
        self.btn.setText(text)

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
