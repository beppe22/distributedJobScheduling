#!/usr/bin/env python3
import random
import socket
from threading import Thread
from time import sleep

import messages as comm


class Updater(Thread):
    def __init__(self, owner):
        Thread.__init__(self)
        self.owner = owner
        self.update_port = self.owner.update_port

        #   socket su cui mando l' aggiornamento del job count
        self.leader_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.leader_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.first_start = True


        # socket su cui ricevo gli update riguardo la th
        self.update_socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.update_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.update_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.update_socket_broadcast.bind(("", self.update_port))

    def send_job_count(self):
        if self.owner.leader_addr and self.first_start:
            self.leader_socket.bind(self.owner.leader_addr)
            self.first_start = False

        # se posso mando l'aggiornameto
        if self.owner.leader_addr:
            print('sending update')

            # simulazione job
            self.owner.job_count = int(random.uniform(0, 10))

            msg = str(self.owner.id)+comm.SEPARATOR+str(self.owner.job_count)
            self.leader_socket.sendto(msg.encode(), self.owner.leader_addr)

    def update_th(self):
        sk = self.update_socket_broadcast
        sk.settimeout(comm.LEADER_OFFLINE_TO)
        try:
            while True:
                # se sta andando un elezione devo stare in attesa
                while self.owner.is_election:
                    sleep(0.5)
                # ricevo l' aggiornamento
                data, addr = sk.recvfrom(1024)
                self.owner.threshold = int(data.decode())
                print(self.owner.threshold)
                # mando il conteggio dei job attivi
                self.send_job_count()
        except Exception as e:
            # è scattato il timeout, il leader si è disconnesso. devo mandare nuove elezioni
            print('Leader offline?')
            self.owner.elect_manager.run_election()
            self.update_th()

    def run(self):
        self.update_th()

