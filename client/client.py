#!/usr/bin/env python3
import socket
import sys
from threading import Thread

from client import client_manager as cm
import messages as comm

class Client(Thread):
    def __init__(self,executing_port):
        Thread.__init__(self)
        self.port = executing_port
        self.client_manager= None


    def send_job(self, ):

        self.client_manager= cm.ClientManager(self)
        self.client_manager.start()


    def run(self):
        self.send_job()


def main():
    Client(int(sys.argv[1])).start()


if __name__ == "__main__":
    main()