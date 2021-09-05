import socket
from asyncio import sleep
from threading import Thread
from cluster import job as j
import job_token as jt


class JobManager(Thread):
    def __init__(self, owner):
        Thread.__init__(self)
        self.owner=owner
        self.job_dict=self.owner.job_dict
        self.result= None


    def receving_job(self):

        self.job_id = 0


        self.owner.UDPExecutorSocket.bind(("", self.owner.executor_port))

        while (True):
            bytesAddressPair = self.owner.UDPExecutorSocket.recvfrom(1024)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            clientMsg = "Messagge from client:{}".format(message)
            clientAddress = "client address:{}".format(address)
            print(clientMsg)
            print(clientAddress)

            #mando al client l'id del job
            self.owner.UDPExecutorSocket.sendto(str.encode(str(self.job_id)),address)

            # TODO fare i controlli per vedere se executor non ha superato threshold


            jt.JobToken(self,str(self.job_id),int(message)).start()

            sleep(1)

            self.job_dict[self.job_id] = (j.Job(self.job_id, int(message),self.result, address[0], address[1]))


            #spedisco il risultato al client

            self.owner.UDPExecutorSocket.sendto(str.encode(str(self.result)), address)

            self.job_id += 1
            #self.job_dict.pop(int(message.split()[1]), "Element not found")









    def run(self):
        self.receving_job()