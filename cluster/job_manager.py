import socket
from asyncio import sleep
from threading import Thread
from cluster import job as j
import job_token as jt
import messages as comm

class JobManager(Thread):
    def __init__(self, owner):
        Thread.__init__(self)
        self.owner = owner
        self.job_dict = self.owner.job_dict
        self.result = None

        #socket per comunicazione
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sk.bind(("", self.owner.executor_port))


    def receving_job(self):

        self.job_id = 0

        while True:

            # io manterrei la comunicazione come le due linee di codice succesive ovvero una stringa separata da
            # 'comm.SEPARATOR' così poi puoi accedere ai parametri in modo facile con param[i]
            #
            # in addr hai il tuo mittente del messaggio

            data, addr = self.sk.recvfrom(1024)
            param = data.decode().split(comm.SEPARATOR)


           # bytesAddressPair = sk.recvfrom(1024)
            #message = bytesAddressPair[0]
            #address = bytesAddressPair[1]

            #comunicazione usando match statement così è più chiara e facile da gestire, poi chiama una sotto funzione tua
            #per ogni operazione necessaria

            m = param[0]
            if m == comm.JOB_EXEC_REQ:
                    self.job_exec_request(addr, param[1])
            elif m == comm.JOB_RES_REQ:
                    pass
            elif m == comm.PING:
                    #ping pong necessario per capire se qualcuno è offline
                    self.sk.sendto(comm.PONG.encode(), addr)





    def job_exec_request(self, address, message):
        # mando al client l'id del job
        self.owner.UDPExecutorSocket.sendto(str.encode(str(self.job_id)), address)

        # TODO fare i controlli per vedere se executor non ha superato threshold

        jt.JobToken(self, str(self.job_id), int(message)).start()

        sleep(1)

        self.job_dict[self.job_id] = (j.Job(self.job_id, int(message), self.result, address[0], address[1]))

        # spedisco il risultato al client

        self.owner.UDPExecutorSocket.sendto(str.encode(str(self.result)), address)

        self.job_id += 1
        # self.job_dict.pop(int(message.split()[1]), "Element not found")






    def run(self):
        self.receving_job()
