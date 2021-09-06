#!/usr/bin/env python3

import os
import socket
from time import sleep
import messages as comm
import traceback


skp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
skp.bind(("", comm.C2C_PORT))
skp.settimeout(comm.EXEC_OFFLINE_TO)

executor_list= []

# utile per avere un executor su ogni finestra
def main():
    count_executor = input(comm.MESSAGE)
    gid = input(comm.MESSAGE_GID)
    for i in range(int(count_executor)):
        port = comm.MINPORT + (i * 3)
        os.system("start cmd.exe /k python3 -m cluster.executor " + gid + ' ' + str(comm.BROAD_EL_PORT) + " " + str(
            comm.BROAD_UP_PORT) + " " + str(port) + " " +'0')
        executor_list.append(port)

    sleep(3)
    run_first_elect()
    check_offline(executor_list, gid)

def check_offline(list,id):
    p = comm.C2C_PORT
    while True:
        try:
            for p in list:
                skp.sendto(comm.PING.encode(), ("127.0.0.1", p))
                data, addr = skp.recvfrom(1024)
                param = data.decode().split(comm.SEPARATOR)
                #print(addr)

        except socket.timeout:
            print(str(p) + ' offline')
            os.system("start cmd.exe /k python3 -m cluster.executor " + id + ' ' + str(comm.BROAD_EL_PORT) + " " + str(
                comm.BROAD_UP_PORT) + " " + str(p) + " "+ "1")
            sleep(1)

        except ConnectionResetError:
            pass
        except Exception as e:
            print(e)
            traceback.print_exc()









def run_first_elect():
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    #sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    #sk.bind(("", comm.BROAD_EL_PORT))

    msg = comm.ELECTMSG + comm.SEPARATOR + '0'
    sk.sendto(msg.encode(), ('<broadcast>', comm.BROAD_EL_PORT))

if __name__ == "__main__":
    main()