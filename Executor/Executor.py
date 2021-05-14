#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
import sys
import socket
from time import sleep

from MessageDefinition import *

MINPORT = 49153
BROD_PORT = 49152
ELTIMEOUT = 5


# se avviato da StarterCMD è una classe normale, se avviato usando Starter utilizziamo i thread

class Executor(Thread):
    def __init__(self, b_port, executor_port):
        Thread.__init__(self)

        # connessioni
        self.executor_port = int(executor_port)
        self.b_port = int(b_port)

        self.sk_broadcast = None

        # other flags
        self.is_leader = None
        self.is_election = None
        self.coord_wait = False
        self.first_start = True

        self.job_count = None
        self.threshold = None
        self.job_result = None

    def listen_all(self):
        # avvio broadcast
        self.sk_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        sk = self.sk_broadcast
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sk.bind(("", self.b_port))

        # primo avvio
        if self.first_start:
            self.run_election(0)
            self.first_start = False

        # inizializzo il timer
        step = 0.2
        sk.settimeout(ELTIMEOUT)
        try:
            while True:
                data, addr = sk.recvfrom(1024)
                param = data.decode().split(SEPARATOR)

                if param[0] == ELECTMSG and not self.coord_wait and int(param[1]) != self.executor_port:
                    print(param[1])
                    self.run_election(int(param[1]))
                    sk.settimeout(ELTIMEOUT)

                elif param[0] == COORDMSG:
                    print('COORDINATOREEEE' + param[1])
                    return

                elif self.coord_wait:
                    sk.settimeout(None)

                sleep(step)

        except:
            print('coord')
            self.declare_coord()
            return


    def declare_coord(self):
        msg = COORDMSG + SEPARATOR + str(self.executor_port)
        self.sk_broadcast.sendto(msg.encode(), ('<broadcast>', BROD_PORT))
        self.is_election = False
        self.is_leader = True

    def run_election(self, starter_id):
        print('mando elect')

        # sta runnando un elezione
        self.is_election = True

        # verifico il rank di chi ha runnato la elect
        if starter_id > self.executor_port:
            # mi metto in attesa
            self.coord_wait = True
            return

        # se sono più alto mando msg elect
        msg = ELECTMSG + SEPARATOR + str(self.executor_port)
        self.sk_broadcast.sendto(msg.encode(), ('<broadcast>', BROD_PORT))
        # aspetto altri elect
        return

    def send_job_count(self, ):
        pass

    def run(self):
        sleep(3)
        self.listen_all()


def main():
    if len(sys.argv) == 3:
        Executor(int(sys.argv[1]), int(sys.argv[2])).run()
    else:
        Executor(BROD_PORT, MINPORT).run()


if __name__ == "__main__":
    main()
