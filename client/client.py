#!/usr/bin/env python3
import socket
import sys
from threading import Thread

from client import client_manager as cm
import messages as comm

class Client(Thread):
    def __init__(self,executing_port):
        Thread.__init__(self)
        #TODO si dovrebbero levare le info riguardanti la porta e l'ip del client perchè tanto sono usperflue perchè
        # questi valori li prenderemo direttamente dall'executor dopo che gli arriveranno info dal client
        self.port = executing_port
        self.Ip = socket.gethostname()
        self.client_manager= None
        self.number= None
        self.IpServer=None
        self.PortServer= None


    def send_job(self, ):
        self.number= input(comm.MESSAGE_TO_CLIENT)
        self.IpServer=input("Give me the server address")
        self.PortServer=input("give me the server port")
        self.client_manager= cm.ClientManager(self)
        self.client_manager.start()


    def recall_result(self, ):
        pass

    def run(self):
        self.send_job()


def main():
    Client(int(sys.argv[1])).start()


if __name__ == "__main__":
    main()