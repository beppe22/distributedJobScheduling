import socket
from threading import Thread
from cluster import job as j, job_token as jt

import messages as comm

class JobManager(Thread):
    def __init__(self, owner, l1, l2):
        Thread.__init__(self)
        self.l1=l1
        self.l2 = l2
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


            #comunicazione usando match statement così è più chiara e facile da gestire, poi chiama una sotto funzione tua
            #per ogni operazione necessaria

            m = param[0]
            if m == comm.JOB_EXEC_REQ:
                    if(param[2]=='1') :
                      self.job_exec_request(addr, param[1], '', True)
                    elif(param[2]=='0'):
                      self.job_exec_request((param[3], int(param[4])), param[1], param[5], False)
            elif m == comm.PING:
                #ping pong necessario per capire se qualcuno è offline
                self.sk.sendto(comm.PONG.encode(), addr)
            elif m == comm.JOB_REQ_REQ:
                self.responding_request_client(str(param[1]), addr)

            self.routine_check()

    def routine_check(self):

        # controllo dei job terminati
        self.l1.acquire()
        self.finished_job = 0
        for key in self.job_dict:
            if self.job_dict[key].result:
                self.finished_job += 1
        # conteggio
        self.job_count = len(self.job_token_dict) - self.finished_job
        self.l1.release()





     # direct necessario per evitare catene di inoltro
    def job_exec_request(self, address, message, new_job_id, direct):

        address=(str(address[0]), int(address[1]))
        # mando al client l'id del job

        message=int(message)
        msg = str(self.job_id)
        #print(msg)
        if direct:
            self.sk.sendto(msg.encode(), address) # problema: se ad esempio il
        # job venisse trasferito da executor a executor questo job_id verrebbe di volta in volta mandato al client
        # ma ciò viene risolto perchè il client sta in attesa di questo valore solo una volta e dunque le
        # altre volte anche se il valore viene spedito dai diversi executor non viene ricevuto dal client


        self.l2.acquire()
        temp = self.owner.free_exec

        # inoltro
        if (self.job_count + 1) > self.owner.threshold and direct and temp[1] != self.owner.executor_port:

            new_job_id = str(self.owner.id) +'-' + str(self.job_id)
            msg = comm.JOB_EXEC_REQ + comm.SEPARATOR + str(message) + comm.SEPARATOR + '0' \
                 + comm.SEPARATOR + str(address[0]) + comm.SEPARATOR + str(address[1]) + comm.SEPARATOR \
                + new_job_id


            self.sk.sendto(str.encode(msg), temp)

            self.job_forw[str(self.job_id)] = (temp, new_job_id)
        else:
            if direct:
                id=str(self.job_id)
            else:
                id=str(new_job_id)
            job_token_thread = jt.JobToken(self, id, int(message))
            self.job_token_dict[self.i] = job_token_thread
            self.i += 1
            self.job_dict[id] = (j.Job(id, int(message), None, address))
            if not self.owner.is_leader:
                print('job_id' + str(id))
            job_token_thread.start()

        self.l2.release()
        self.job_id += 1


    def responding_request_client(self,job_id, addr):
        if not self.owner.is_leader:
            print('job_request' + str(job_id))

        self.result = None

        # se è nei forward inoltro la richiesta
        if job_id in self.job_forw.keys():
            self.sk.sendto(str.encode(comm.JOB_REQ_REQ + comm.SEPARATOR + str(self.job_forw[job_id][1])), self.job_forw[job_id][0])
            return

        #altrimenti controllo di averlo io
        if job_id in self.job_dict.keys():
            self.result = self.job_dict[job_id].result
            client_address = self.job_dict[job_id].client_address
            #print(client_address)
            if self.result != None:
                #print("eccolo5")
                self.sk.sendto(str.encode(str(self.result)), client_address)
            else:
                #print("eccolo6")
                self.sk.sendto(str.encode("Risultato ancora non calcolato"), client_address)
        else:
            self.sk.sendto(str.encode("Job Non esiste"), addr)




    def run(self):
        self.receving_job()

