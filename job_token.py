#!/usr/bin/env python3
import sys
import socket
from threading import Thread
from time import sleep


class JobToken(Thread):
    def __init__(self,owner,job_id,parameter,executor_port,executor_ip):
        Thread.__init__(self)
        self.owner=owner
        self.job_id = job_id
        self.parameter = parameter
        self.result = None
        self.executor_port= executor_port
        self.executor_ip= executor_ip

    def send_result(self, ):
        bytesToSend = str.encode(str(self.result) + ' '+ str(self.job_id))

        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.sendto(bytesToSend, (self.executor_ip, self.executor_port))


        #TODO dovrei killare

    def compute_result(self, ):
        # print("numero ricevuto" + str(self.parameter))
        self.result = self.parameter * 2

        sleep(3)

        self.send_result()

    def run(self):
        self.compute_result()



