#!/usr/bin/env python3
import random
import socket
import traceback
from threading import Thread
from time import sleep

import messages as comm
from datetime import datetime



class Updater(Thread):
    def __init__(self, owner, l1, l2):
        Thread.__init__(self)
        self.l1 = l1
        self.l2 = l2
        self.owner = owner
        self.update_port = self.owner.update_port

        #   socket su cui mando l' aggiornamento del job count
        self.leader_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        #self.leader_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.first_start = True


        # socket su cui ricevo gli update riguardo la th
        self.update_socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.update_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.update_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.update_socket_broadcast.bind(("", self.update_port))

    def send_job_count(self):
        sleep(random.uniform(0.5, 1))
        if self.owner.leader_addr and self.first_start:
            #self.leader_socket.bind(self.owner.leader_addr)
            self.first_start = False

        # se posso mando l'aggiornameto
        if self.owner.leader_addr:
            #print('sending update')

            # simulazione job
            #self.owner.job_count = int(random.uniform(0, 30))
            self.l1.acquire()
           # print('job count:'  + str(self.owner.job_manager.job_count) )

            msg = str(self.owner.id)+comm.SEPARATOR+str(self.owner.job_manager.job_count)+comm.SEPARATOR+str(self.owner.executor_port)+comm.SEPARATOR+str(datetime.now())
            self.leader_socket.sendto(msg.encode(), self.owner.leader_addr)
            self.l1.release()

    def update_th(self):
        sk = self.update_socket_broadcast
        sk.settimeout(comm.LEADER_OFFLINE_TO)
        tik=0
        try:
            while True:
                # se sta andando un elezione devo stare in attesa
                while self.owner.is_election:
                    sleep(1)
                # ricevo l' aggiornamento
                data, addr = sk.recvfrom(1024)
                param = data.decode().split(comm.SEPARATOR)
                self.l2.acquire()
                self.owner.threshold = int(param[0])
                self.owner.free_exec = (param[1], int(param[2]))
                #print(data)
                self.l2.release()
                # mando il conteggio dei job attivi
                if tik > 5:
                    self.send_job_count()
                    tik = 0
                else:
                    tik += 1

        except socket.timeout:
            # è scattato il timeout, il leader si è disconnesso. devo mandare nuove elezioni
            print('Leader offline?')
            self.owner.elect_manager.run_election()
            self.update_th()
        except Exception as e:
            print(e)
            traceback.print_exc()


    def run(self):
        self.update_th()

