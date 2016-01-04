import threading
import time
import sys
import ctypes
from PyQt4.QtCore import QDir, SIGNAL
from PyQt4.QtGui import *
import netsh
from frame import Frame
from activities import HotSpot, ActionBar, Info, Toast, Clients

APP_ID = 'dev$oviedo.my-wifi-windows-py3.3PyQt4.v1'
ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(APP_ID)


class Main(QWidget):
    def __init__(self, parent=None):
        super(Main, self).__init__(parent)
        self.action_bar = ActionBar(self)
        self.hotspot = HotSpot(self)
        self.info = Info(self)
        self.clients = Clients(self)
        self.hotspot.show()
        self.connect(self.hotspot, SIGNAL("toast"), self.toast_notify)
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
        elif text.startswith("Clientes"):
            self.change_activity(self.clients)
        try:
            self.action_bar.active_btn(self.sender())
        except AttributeError:  # este error puede saltar cuando ejecutamos una accion del mebu cont,
            # pq QAction no tiene attributo de stylesheet(q uso para ponerle la rayita al tab selecc)
            # Entonces recorremos todos los btns buscando cual tiene dicho text
            for btn in self.action_bar.btn_list:
                if btn.text().startswith(text):  # usar starwith el lugar de == por el tab Clientes (x),
                    # x cambia segun la cant de clientes
                    self.action_bar.active_btn(btn)
                    break

    def change_activity(self, activity_to, activity_from=None):
        if not activity_from:
            activity_from = self.current_activity
        activity_from.hide()
        activity_to.show()
        self.current_activity = activity_to

    def toast_notify(self, text, info, time_=3000):
        toast = Toast(text, info, self)
        toast.show_toast(time_)


class UI(Frame):
    STATE = netsh.HOSTED_NETWORK_INFO['state']

    def __init__(self):
        Frame.__init__(self)
        self.main = Main()
        self.cant_clients = 0
        self.layout_add(self.main)

        self.state_has_changed(self.STATE)

        thread = threading.Thread(target=self.upd_ui)
        thread.setName('Frame')
        thread.setDaemon(True)
        thread.start()

        self.connect(self, SIGNAL("state_changed"), self.state_has_changed)
        self.connect(self.trayIcon, SIGNAL("messageClicked()"), self.message_clicked)
        # self.connect(self.trayIcon, SIGNAL("activated(QString)"), self.icon_activated)NO BORRAR
        # todo no encuentro la forma de conectar trayIcon a activated usando el nuevo estilo(ver comentario de arriba)
        self.trayIcon.activated.connect(self.icon_activated)

    def createActions(self):
        # crear primero las acciones definidas por el padre, luego las sobreescr
        super(UI, self).createActions()
        self.action1 = QAction("HotSpot", self, triggered=self.show_tab)
        self.action2 = QAction("Clientes", self, triggered=self.show_tab)
        self.action3 = QAction("Info", self, triggered=self.show_tab)
        self.action4 = QAction("Ayuda", self, triggered=self.show_tab)

    def show_tab(self):
        # cuando se selecciona una accion del menu contex
        self.main.tab_clicked()
        self.show()

    def icon_activated(self, reason):
        # cuando se da clic a la ruedita en el icon tray
        if reason == QSystemTrayIcon.MiddleClick:
            state = netsh.HOSTED_NETWORK_INFO['state']
            if state == "Iniciado":
                self.main.hotspot.btn_change_text("Parar")
                self.main.hotspot.btn_clicked()
            elif state == "No iniciado":
                self.main.hotspot.btn_change_text("Iniciar")
                self.main.hotspot.btn_clicked()
        # y ejecutar tb el metodo del padre pa el click
        super(UI, self).icon_activated(reason)

    def message_clicked(self):
        self.main.change_activity(self.main.clients)
        self.show()

    def upd_ui(self):
        while True:
            info = netsh.HOSTED_NETWORK_INFO.copy()
            state = info['state']
            # si un nuevo cliente se conecta
            if int(self.cant_clients) < int(info["cant_clients"]):
                new_client = info["data_clients"].split('\n')[
                    -2]  # -2 pq la linea es asi: mac\tstatus\nmac\tstatus\n... al terminar en \n se hace el ultimo elem de la lista ""
                # todo debe ser el ip o nombree de eq y no la mac(invest obtener ip a partir de mac)
                mac = new_client.split('\t')[0].strip()
                self.show_message("Nuevo cliente conectado", mac)
            self.cant_clients = info["cant_clients"]
            self.main.action_bar.clients_btn.setText("Clientes (%s)" % self.cant_clients)
            self.main.clients.clients_lbl.setText(info["data_clients"])
            if self.STATE != state:
                self.STATE = state
                self.emit(SIGNAL("state_changed"), self.STATE)
            time.sleep(5)

    def state_has_changed(self, state):
        self.set_icon_by_state_hosted_network(state)


app = QApplication(sys.argv)
UI()
# app.setWindowIcon(QIcon(":/icon"))
app.exec_()
