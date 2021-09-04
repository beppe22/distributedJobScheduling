from threading import Thread

import socket
import messages as comm


class ClientManager(Thread):
    def __init__(self,owner):
        Thread.__init__(self)
        self.owner=owner
        self.number= self.owner.number
        self.IpServer= self.owner.IpServer
        self.PortServer= self.owner.PortServer

    def send_job(self):

        bytesToSend= str.encode(self.number)

        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.sendto(bytesToSend,(str(self.IpServer),int(self.PortServer)))


    def receiving_result(self):
        pass

    def run(self):
        self.send_job()


