import socket
from threading import Thread

from MessageDefinition import *


class Updater(Thread):
    def __init__(self, owner):
        Thread.__init__(self)
        self.owner = owner
        self.update_port = None

        self.leader_ip = None
        self.leader_port = None
        self.leader_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

        self.update_socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP

    def send_job_count(self):
        pass

    def update_th(self, ):
        sk = self.update_socket_broadcast
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sk.bind(("", self.update_port))
        while True:
            while self.owner.is_election:
                pass
            data, addr = sk.recvfrom(1024)
            param = data.decode()
            print(param)

    def setup_connection(self):

        # leader
        sk = self.update_socket_broadcast
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sk.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sk.bind(("", self.update_port))

    def run(self):
        self.update_th()

