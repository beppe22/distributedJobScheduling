#!/usr/bin/env python3

import socket
from threading import Thread
from time import sleep

import messages as comm


class Leader(Thread):
    def __init__(self, owner):
        Thread.__init__(self)
        self.owner = owner
        self.ex_map = {}
        self.ex_port = {}
        self.threshold = 0
        self.free_exec = str(self.owner.leader_addr)+comm.SEPARATOR+str(self.owner.executor_port)
        self.update_port = self.owner.update_port

        # socket su cui mando gli aggiornamenti in broadcast riguardo la th
        self.update_socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        #self.update_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.update_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        # socket su cui ricevo aggiornamenti riguardo i singoli executor
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.socket.bind(self.owner.leader_addr)


    def calc_threshold(self):
        tot_job = 0
        exec_tot = 0
        all_value = self.ex_map
        temp = None
        lazy = None
        first = True
        #stampo tutti i valori
        #print(self.ex_map.values())
        for i in all_value:
            val = int(all_value.get(i))
            if first:
                temp = val
                lazy = i
                first = False
            if val < temp:
                lazy = i
            tot_job = tot_job + val
            exec_tot = exec_tot + 1

        self.threshold = int(tot_job/exec_tot)
        self.free_exec = self.ex_port.get(lazy)
        #print('\nlazy exec: '+lazy + ' : ' + self.ex_map.get(lazy) + ' th:' +str(self.threshold))
        #print(self.free_exec)

    def monitor(self):
        temp = str(self.threshold)
        while len(temp) < 4:
            temp = temp + ' '
        msg = temp + '- '
        for i in self.ex_map.values():
            temp = str(i)
            while len(temp) < 4:
                temp = temp + ' '
            msg = msg + temp
        print(msg)

    def receive_up(self):
        data, addr = self.socket.recvfrom(1024)
        param = data.decode().split(comm.SEPARATOR)
        #print('time: ' + str(param[3]) +':'+str(param[4]) +':'+ str(param[5]) )

        self.ex_map.update({param[0]: param[1]})
        lazy = addr[0]+comm.SEPARATOR+param[2]
        self.ex_port.update({param[0]: lazy})


    def run(self):
        tik=0
        while self.owner.is_leader:
            msg = str(self.threshold) + comm.SEPARATOR + str(self.free_exec)
            #print(msg)
            self.update_socket_broadcast.sendto(msg.encode(), ('<broadcast>', self.update_port))
            self.receive_up()
            self.calc_threshold()
            if tik>5:
                self.monitor()
                tik = 0
            else:
                tik+=1

            if self.owner.is_election:
                break
            sleep(comm.STEP)
