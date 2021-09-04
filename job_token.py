#!/usr/bin/env python3
import sys
import socket
from threading import Thread
from time import sleep


class JobToken(Thread):
    def __init__(self,job_id,parameter):
        Thread.__init__(self)
        self.job_id = job_id
        self.parameter = parameter
        self.result = None

    def send_result(self, ):
        bytesToSend = str.encode(str(self.result))

        UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPClientSocket.sendto(bytesToSend, ('127.0.0.1', 49220))

        #TODO oltre al risultato dovrei mandare anche l'id del job così da cercarlo nella lista
        #TODO dovrei killare

    def compute_result(self, ):
        # print("numero ricevuto" + str(self.parameter))
        self.result = self.parameter * 2

        sleep(3)

        self.send_result()

    def run(self):
        self.compute_result()





def main():
    JobToken(int(sys.argv[1]),int(sys.argv[2])).start()


if __name__ == "__main__":
    main()

