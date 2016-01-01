import os
import re
import subprocess
import threading
from locale import getdefaultlocale
import time

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
    """
    :param cmd: ejecutar este cmd usando subprocess
    :param as_list: si es true, devuelve cada linea de la salida como item de una lista, si no, como str entero
    :return: salida del comando
    """
    try:
        output = subprocess.check_output(cmd)
        output = output.decode(encoding=ENCODING)
        if as_list:
            output = output.split('\n')
            output = [line.strip() for line in output if line not in ['', '\r', '\t']]
        return output
    except subprocess.CalledProcessError:
        # "process returns a non-zero exit status"
        return False
    except subprocess.TimeoutExpired:
        # "the timeout expires"
        return False


def check_hosted_network():
    show_drivers = run_cmd("netsh wlan show drivers")
    for line in show_drivers:
        if line.find(LANG_DICT['hosted_network']) != -1:
            check = line.split(":")[1]
            return True if check != "no" else False
    return False


def synchronized(lock):
    def dec(f):
        def func_dec(*args, **kwargs):
            lock.acquire()
            try:
                return f(*args, **kwargs)
            finally:
                lock.release()

        return func_dec

    return dec


# lock = threading.Lock()
# @synchronized(threading.Lock())
def show_hosted_network():
    show = run_cmd('netsh wlan show hostednetwork')
    print(show)
    return show


def start_hosted_network():
    start = run_cmd("netsh wlan start hostednetwork", as_list=False)
    if start:
        if start.startswith("Se inic"):
            return True
    return False


def stop_hosted_network():
    stop = run_cmd("netsh wlan stop hostednetwork", as_list=False)
    if stop:
        if stop.startswith("Se detuvo"):
            return True
    return False


def disallow_hosted_network():
    disallow = run_cmd("netsh wlan set hostednetwork mode=disallow")
    if disallow:
        print(disallow)
        return True
    return False


def only_activate_hosted_network():
    activate = run_cmd("netsh wlan set hostednetwork mode=allow", as_list=False)
    if activate:
        return True
    return False


def set_hosted_network(ssid, key):
    hosted_network = run_cmd("netsh wlan set hostednetwork mode=allow ssid=%s key=%s" % (ssid, key), as_list=False)
    if hosted_network:
        print(hosted_network)
        return True
    return False


# print(start_hosted_network())
def get_state():
    show = show_hosted_network()
    state = show[9].split(":")[1].strip()
    return show, state


def hosted_network_info():
    """
    *determinar ssid, key
    *crear dict con la info de la red hosp.
    *determinar el estado de la red hosp. puede ser
    -iniciado, no iniciado, no disponible
    """
    # while True:
    show, state = get_state()
    show_security = show_security_hosted_network()
    # print(show_security)
    # i=0
    # for line in show_security:
    #     print(i,line)
    #     i+=1

    HOSTED_NETWORK_INFO["modo"] = show[2].split(":")[1].strip().replace('"', "")
    HOSTED_NETWORK_INFO["ssid"] = show[3].split(":")[1].strip().replace('"', "")
    HOSTED_NETWORK_INFO["key"] = show_security[5].split(":")[1].strip()
    HOSTED_NETWORK_INFO["max_clientes"] = show[4].split(":")[1].strip().replace('"', "")
    HOSTED_NETWORK_INFO["autenticacion"] = show[5].split(":")[1].strip().replace('"', "")
    HOSTED_NETWORK_INFO["cifrado"] = show[6].split(":")[1].strip().replace('"', "")
    HOSTED_NETWORK_INFO["state"] = state
    # si la red no esta iniciada no tiene estos datos.
    try:
        HOSTED_NETWORK_INFO["bssid"] = show[10].split(":")[1].strip().replace('"', "")
        HOSTED_NETWORK_INFO["radio"] = show[11].split(":")[1].strip().replace('"', "")
        HOSTED_NETWORK_INFO["canal"] = show[12].split(":")[1].strip().replace('"', "")
    except IndexError:
        pass
        # time.sleep(5)


def run():
    while True:
        time.sleep(5)
        hosted_network_info()


# print("tr")
thread = threading.Thread(target=run)
thread.setName('netsh')
thread.setDaemon(True)
thread.start()


def show_security_hosted_network():
    show = run_cmd('netsh wlan show hostednetwork setting=security')
    return show


# def ssid_key():
#     ssid, key = "", ""
#     lines = show_hosted_network()
#     for line in lines:
#         spl = line.split(":")
#         if len(spl) == 2:
#             if spl[0].strip().find(LANG_DICT['ssid_name']) != -1:
#                 ssid = spl[1].strip().replace('"', "")
#                 break
#     lines = show_security_hosted_network()
#     for line in lines:
#         spl = line.split(":")
#         if len(spl) == 2:
#             if spl[0].strip().find(LANG_DICT['security_key']) != -1:
#                 key = spl[1].strip()
#                 break
#     return ssid, key


HOSTED_NETWORK_INFO = dict()
hosted_network_info()
# print(HOSTED_NETWORK_INFO)
# print(ssid_key())
# print(run_cmd('ipconfig'))
# print(check_hosted_network())
# state_hosted_network()
