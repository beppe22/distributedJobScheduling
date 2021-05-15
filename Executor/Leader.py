#!/usr/bin/python
# -*- coding: utf-8 -*-
import socket
from threading import Thread
from time import sleep

from MessageDefinition import *


class Leader(Thread):
    def __init__(self, owner):
        Thread.__init__(self)
        self.owner = owner
        self.ex_map = {}
        self.threshold = 0

        self.update_port = self.owner.update_port

        # socket su cui mando gli aggiornamenti in broadcast riguardo la th
        self.update_socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.update_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.update_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # socket su cui ricevo aggiornamenti riguardo i singoli executor
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.owner.leader_addr)

    def calc_threshold(self):
        tot_job = 0
        exec_tot = 0
        for i in self.ex_map:
            tot_job = tot_job + int(self.ex_map.get(i))
            exec_tot = exec_tot + 1
        self.threshold = int(tot_job/exec_tot)

    def receive_up(self):
        data, addr = self.socket.recvfrom(1024)
        param = data.decode().split(SEPARATOR)
        self.ex_map.update({param[0]: param[1]})
        print(self.ex_map)

    def run(self):
        while self.owner.is_leader:
            self.update_socket_broadcast.sendto(str(self.threshold).encode(), ('<broadcast>', self.update_port))
            self.receive_up()
            self.calc_threshold()
            while self.owner.is_election:
                sleep(1)
            sleep(0.5)
