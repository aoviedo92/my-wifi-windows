import os
import re
import subprocess
from locale import getdefaultlocale

ENCODING = getdefaultlocale()[1]

LANG_DICT = dict()
lang = getdefaultlocale()[0][:2]
if lang == 'es':
    LANG_DICT['state'] = 'Estado'
    LANG_DICT['hosted_network'] = 'Red hospedada admitida'
    LANG_DICT['state_init'] = 'Iniciado'
    LANG_DICT['state_not_init'] = 'No iniciado'
    LANG_DICT['state_not_available'] = 'No disponible'
    LANG_DICT['ssid_name'] = 'Nombre de SSID'
    LANG_DICT['security_key'] = 'Clave de seguridad de usuario'
elif lang == 'en':
    LANG_DICT['state'] = 'State'
    LANG_DICT['hosted_network'] = 'Allow hosted network'
    LANG_DICT['state_init'] = 'Started'
    LANG_DICT['state_not_init'] = 'Stop'
    LANG_DICT['state_not_available'] = 'Unavailable'
    LANG_DICT['ssid_name'] = 'SSID Name'
    LANG_DICT['security_key'] = 'Clave de seguridad de usuario'


def run_cmd(cmd, as_list=True):
    output = subprocess.check_output(cmd)
    output = output.decode(encoding=ENCODING)
    if as_list:
        output = output.split('\n')
        output = [line.strip() for line in output if line not in ['', '\r', '\t']]
    return output


def check_hosted_network():
    show_drivers = run_cmd("netsh wlan show drivers")
    for line in show_drivers:
        if line.find(LANG_DICT['hosted_network']) != -1:
            check = line.split(":")[1]
            return True if check != "no" else False
    return False


def show_hosted_network():
    show = run_cmd('netsh wlan show hostednetwork')
    return show


def state_hosted_network():
    show = show_hosted_network()
    state = ""
    btn_text = "Iniciando..."
    for line in show:
        if re.match("^%s\s+:.+$" % LANG_DICT['state'], line):
            # si la linea coincide con algo asi (Estado                 : Iniciado)
            # partir por : y quitar los espacios en blanco
            state = line.split(":")[1].strip()
            break
    if state == LANG_DICT['state_init']:
        btn_text = "Parar"
    elif state == LANG_DICT['state_not_init']:
        btn_text = "Iniciar"
    elif state == LANG_DICT['state_not_available']:
        btn_text = "Activar"
    return btn_text, state
# print(run_cmd('ipconfig'))
# print(check_hosted_network())
# state_hosted_network()
