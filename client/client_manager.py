from threading import Thread

import socket
import messages as comm


class ClientManager(Thread):
    def __init__(self,owner):
        Thread.__init__(self)
        self.owner=owner
        self.number= None
        self.IpServer= None
        self.PortServer= None
        self.job_id= None
        self.flag=1

    def send_job(self):

        self.number = input(comm.MESSAGE_TO_CLIENT)
        if self.flag:
            self.IpServer = input("Give me the server address")
            self.PortServer = input("give me the server port")
            self.flag=0

        bytesToSend= str.encode(comm.JOB_EXEC_REQ + comm.SEPARATOR + self.number + comm.SEPARATOR + '1' +
                                comm.SEPARATOR + '')

        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.sendto(bytesToSend,(str(self.IpServer),int(self.PortServer)))

        self.receiving_job_id()


    def receiving_job_id(self):
        msg=self.UDPClientSocket.recvfrom(1024)
        self.job_id= int(msg[0])
        print("L'id del job è {}".format(str(self.job_id)))

    def receiving_result(self):


        #TODO la richiesta deve essere fatto tramite il job_id
        job_choise= input("Digita l'id del job di cui vuoi avere il risultato")
        self.UDPClientSocket.sendto(str.encode(comm.JOB_REQ_REQ + comm.SEPARATOR +str(job_choise)),(str(self.IpServer),int(self.PortServer)))
        messageFromServer= self.UDPClientSocket.recvfrom(1024)
        #msg= "Il risultato è {}".format(messageFromServer[0])
        print("Il risultato è")
        print(messageFromServer[0])

    def run(self):

        while(True):
         print("Vuoi spedire un job oppure vuoi avere il risultato di un job spedito?")
         answer = input("Digita 0 per la prima opzione, 1 per la seconda")
         if answer=='0':
            self.send_job()
         else : self.receiving_result()


