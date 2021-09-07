import socket
from asyncio import sleep
from threading import Thread
from cluster import job as j


import job_token as jt
import messages as comm

class JobManager(Thread):
    def __init__(self, owner, lock):
        Thread.__init__(self)
        self.lock=lock
        self.owner = owner
        self.job_dict = self.owner.job_dict

        self.result = None

        self.job_token_dict = {} #dict di tutti i thread avviati per risolvere i job

        self.job_forw={} #dict di tutti i job inoltrati

        self.i=0 #contatore per job_token_dict
        #socket per comunicazione
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sk.bind(("", self.owner.executor_port))

        self.job_count = 0
        self.finished_job = 0


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
                    if(param[2]=='1') :
                      self.job_exec_request(addr, param[1], True)
                    elif(param[2]=='0'):
                      self.job_exec_request((param[3], int(param[4])), param[1], False)
            elif m == comm.PING:
                    #ping pong necessario per capire se qualcuno è offline
                    self.sk.sendto(comm.PONG.encode(), addr)
            elif m == comm.JOB_REQ_REQ:
                self.responding_request_client(int(param[1]))

            self.routine_check()

    def routine_check(self):

        # controllo dei job terminati
        self.lock.acquire()
        self.finished_job = 0
        for key in self.job_dict:
            if self.job_dict[key].result:
                self.finished_job += 1
        # conteggio
        self.job_count = len(self.job_token_dict) - self.finished_job
        self.lock.release()





     # direct necessario per evitare catene di inoltro
    def job_exec_request(self, address, message, direct):

        address=(str(address[0]), int(address[1]))
        # mando al client l'id del job

        message=int(message)

        self.sk.sendto(str.encode(str(self.job_id)), address) # problema: se ad esempio il
        # job venisse trasferito da executor a executor questo job_id verrebbe di volta in volta mandato al client
        # ma ciò viene risolto perchè il client sta in attesa di questo valore solo una volta e dunque le
        # altre volte anche se il valore viene spedito dai diversi executor non viene ricevuto dal client

        temp = self.owner.free_exec

        # inoltro
        if self.job_count > self.owner.threshold and direct and temp[1] != self.owner.executor_port:

            msg = comm.JOB_EXEC_REQ + comm.SEPARATOR + str(message) + comm.SEPARATOR + '0' \
                 + comm.SEPARATOR + str(address[0]) + comm.SEPARATOR + str(address[1])


            self.sk.sendto(str.encode(msg), temp)
            self.job_forw[self.job_id] = temp
        else:
            job_token_thread = jt.JobToken(self, self.job_id, int(message))

            self.job_token_dict[self.i] = job_token_thread
            self.i += 1

            self.job_dict[self.job_id] = (j.Job(self.job_id, int(message), None, address))


            job_token_thread.start()



        self.job_id += 1


    def responding_request_client(self,job_id):

        self.result= None

        if job_id in self.job_forw.keys() :

            self.sk.sendto(str.encode(comm.JOB_REQ_REQ + comm.SEPARATOR + str(job_id)),self.job_forw[job_id])
        else:
         print("eccolo2")
         if job_id in self.job_dict.keys() :
             print("eccolo2")
             self.result = self.job_dict[job_id].result
         print("eccolo4")
         self.client_address = self.job_dict[job_id].client_address
         #TODO ristrutturare sta cosa perchè se avessimo tante esecuzioni il result risulterebbe sempre diverso da none
         if self.result != None:
            print("eccolo5")
            self.sk.sendto(str.encode(str(self.result)), self.client_address)
         else:
            print("eccolo6")
            self.sk.sendto(str.encode("Risultato ancora non calcolato"), self.client_address)
            pass
    def run(self):
        self.receving_job()

