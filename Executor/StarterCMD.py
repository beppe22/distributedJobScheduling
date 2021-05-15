import os
import socket
from time import sleep

from MessageDefinition import *

MESSAGE = 'Quanti executors vuoi avviare?'


# utile per avere un executor su ogni finestra
def main():
    count = input(MESSAGE)
    for i in range(int(count)):
        port = MINPORT+(i*2)
        os.system("start cmd.exe /k python3 Executor.py "+' 1 '+str(BROAD_EL_PORT)+" "+str(BROAD_UP_PORT)+" "+str(port))

    sleep(3)
    run_first_elect()


def run_first_elect():
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    sk.bind(("", BROAD_EL_PORT))

    msg = ELECTMSG + SEPARATOR + '0'
    sk.sendto(msg.encode(), ('<broadcast>', BROAD_EL_PORT))

if __name__ == "__main__":
    main()