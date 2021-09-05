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

        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.sendto(bytesToSend,(str(self.IpServer),int(self.PortServer)))
        self.receiving_result()

    def receiving_result(self):

        messageFromServer= self.UDPClientSocket.recvfrom(1024)
        msg= "Il risultato è {}".format(messageFromServer[0])
        print(msg)

    def run(self):
        self.send_job()


