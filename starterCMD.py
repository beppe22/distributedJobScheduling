#!/usr/bin/env python3

import os
import socket
from threading import Thread
from time import sleep
import messages as comm
import traceback


executor_list = {}
adding = False

class Ping(Thread):
        def __init__(self,):
            Thread.__init__(self)
            self.dict = executor_list
            self.skp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
            self.skp.bind(("", comm.C2C_PORT))
            self.skp.settimeout(comm.EXEC_OFFLINE_TO)

        def check_offline(self):
            p = comm.C2C_PORT
            while True:
                if adding:
                    continue
                try:
                    for p in self.dict:
                        if adding:
                            break
                        self.skp.sendto(comm.PING.encode(), ("127.0.0.1", p))
                        data, addr = self.skp.recvfrom(1024)
                        #param = data.decode().split(comm.SEPARATOR)
                        #print(addr)

                except socket.timeout:
                    print(str(p) + ' offline')
                    os.system("start cmd.exe /k python3 -m cluster.executor " + self.dict.get(p) + ' ' + str(
                        comm.BROAD_EL_PORT) + " " + str(
                        comm.BROAD_UP_PORT) + " " + str(p) + " " + "1" + " "+ "1")
                    sleep(5)

                except ConnectionResetError:
                    # print(ConnectionResetError)
                    pass
                except Exception as e:
                    print(e)
                    traceback.print_exc()

        def run(self):
            self.check_offline()


# utile per avere un executor su ogni finestra+

def main():
    already_started=0
    flag=1
    global adding
    while True:

        adding = True
        count_executor = input(comm.MESSAGE)
        already_started = already_started + int(count_executor)
        gid = input(comm.MESSAGE_GID)
        for i in range(int(count_executor)):
            port = int(already_started) + comm.MINPORT + (i * 3)
            os.system("start cmd.exe /k python3 -m cluster.executor " + gid + ' ' + str(comm.BROAD_EL_PORT) + " " + str(
                comm.BROAD_UP_PORT) + " " + str(port) + " " +'0' + " " +'0')
            executor_list.update({port: gid})


        print(executor_list)
        sleep(10)
        run_first_elect()
        adding = False
        if flag:
            Ping().start()
            flag = 0
        input(comm.WAIT)





def run_first_elect():
    sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
    sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    msg = comm.ELECTMSG + comm.SEPARATOR + '0'
    sk.sendto(msg.encode(), ('<broadcast>', comm.BROAD_EL_PORT))

if __name__ == "__main__":
    main()

