import random
from threading import Thread

import socket
from time import sleep

import messages as comm


class ClientManager(Thread):
    def __init__(self,owner,port):
        Thread.__init__(self)
        self.owner=owner
        self.number= None
        self.IpServer= '127.0.0.1'
        self.PortServer= 49300
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.bind(("", port))
        self.UDPClientSocket.settimeout(2)



    def send_job(self):
        self.number = input(comm.MESSAGE_TO_CLIENT)
        if not self.number.isnumeric():
            self.number = random.randint(1,50)
            print(self.number)

        bytesToSend= str.encode(comm.JOB_EXEC_REQ + comm.SEPARATOR + str(self.number) + comm.SEPARATOR + '1' +
                                comm.SEPARATOR + '')
        try:
            self.UDPClientSocket.sendto(bytesToSend, (str(self.IpServer), int(self.PortServer)))
        except Exception as e:
            print(comm.ERR)
            self.input_addr()
            return
        self.receiving_job_id()


    def receiving_job_id(self):
        try:
            msg, addr = self.UDPClientSocket.recvfrom(1024)
            job_id = msg.decode()
            print(comm.JOB_ID_RPL + str(job_id))
        except Exception as e:
            print(comm.ERR)
            self.input_addr()
            return



    def receiving_result(self):

        job_choice= input(comm.JOB_ID_REQ)
        if not job_choice.isnumeric():
            return
        try:
            self.UDPClientSocket.sendto(str.encode(comm.JOB_REQ_REQ + comm.SEPARATOR +str(job_choice)),(str(self.IpServer),int(self.PortServer)))
            messageFromServer, addr = self.UDPClientSocket.recvfrom(1024)
        except socket.timeout:
            print(comm.TIME)
            return
        except Exception as e:
            print(comm.ERR)
            self.input_addr()
            return

        print(comm.RESULT)
        print(messageFromServer.decode())

    def input_addr(self):
        ip = input(comm.ADDRESS_REQ)
        port = input(comm.PORT_REQ)

        if len(ip)>=7:
            self.IpServer = ip
        if port.isnumeric() and int(port)>=49300:
            self.PortServer = int(port)


    def run(self):
        print(comm.LINE)
        self.input_addr()
        print(comm.LINE)

        while True:

            answer = input(comm.COMMAND_CHOICE)

            if answer =='1':
                self.receiving_result()
            elif answer =='2':
                self.input_addr()
            else:
                self.send_job()
            print(comm.LINE)
            #sleep(0.1)



