from threading import Thread

import socket
from time import sleep

import messages as comm


class ClientManager(Thread):
    def __init__(self,owner,port):
        Thread.__init__(self)
        self.owner=owner
        self.number= None
        self.IpServer= '192.168.1.189'
        self.PortServer= None
        self.flag=1
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.bind(("", port))

    def send_job(self):

        self.number = input(comm.MESSAGE_TO_CLIENT)
        if not self.number.isnumeric():
            return

        if self.flag:
           # self.IpServer = input("Give me the server address")
            self.PortServer = input("give me the server port")
            self.flag=0

        bytesToSend= str.encode(comm.JOB_EXEC_REQ + comm.SEPARATOR + self.number + comm.SEPARATOR + '1' +
                                comm.SEPARATOR + '')
        try:
            self.UDPClientSocket.sendto(bytesToSend,(str(self.IpServer),int(self.PortServer)))
        except Exception as e:
            print('addr errato' + str(e))
            self.flag=1
            return
        self.receiving_job_id()


    def receiving_job_id(self):
        try:
            msg, addr = self.UDPClientSocket.recvfrom(1024)
            job_id = msg.decode()
            print("L'id del job è: " + str(job_id) + ' from' +str(addr))

        except Exception as e:
            print('addr errato' + str(e))
            self.flag = 1
            return



    def receiving_result(self):


        #TODO la richiesta deve essere fatto tramite il job_id
        job_choise= input("Digita l'id del job di cui vuoi avere il risultato\n")
        if not job_choise.isnumeric():
            return
        try:
            self.UDPClientSocket.sendto(str.encode(comm.JOB_REQ_REQ + comm.SEPARATOR +str(job_choise)),(str(self.IpServer),int(self.PortServer)))
            messageFromServer= self.UDPClientSocket.recvfrom(1024)
        except Exception as e:
            print('addr errato' + str(e))
            self.flag = 1
            return

        #msg= "Il risultato è {}".format(messageFromServer[0])
        print("Il risultato è: ")
        print(messageFromServer[0])

    def run(self):

        while(True):

            print("Vuoi spedire un job oppure vuoi avere il risultato di un job spedito?\n")
            answer = input("Digita 1 per la prima opzione, 0 per la seconda\n")

            if answer =='0':
                self.receiving_result()
            else:
                self.send_job()
            sleep(0.5)


