import socket
from threading import Thread
from cluster import job as j, job_token as jt
import os
import messages as comm
import csv

class JobManager(Thread):
    def __init__(self, owner, l1, l2, restart):
        Thread.__init__(self)
        self.restart=restart
        self.l1=l1
        self.l2 = l2
        self.owner = owner

        self.job_dict = {}
        #self.job_token_dict = {}  # dict di tutti i thread avviati per risolvere i job
        self.job_forw = {}  # dict di tutti i job inoltrati
        self.id=str(self.owner.id)

        self.path = os.path.join(os.path.dirname(__file__), 'temp\\')
        self.file_job_forw= self.path + self.id + "_job_forw.csv"
        self.file_job_dict = self.path + self.id + "_job_dict.csv"


        self.job_id = 0
        self.job_count = 0
        self.finished_job = 0

        # se esistono i file li elimino così li ho puliti
        self.command = 'a'
        if not restart:
            if os.path.exists(self.file_job_forw):
                os.remove(self.file_job_forw)
            if os.path.exists(self.file_job_dict):
                os.remove(self.file_job_dict)
        else:
            self.recovery()

        #socket per comunicazione
        self.sk = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
        self.sk.bind(("", self.owner.executor_port))


# -------------------------------------------------------------------------------------------------------
    def recovery(self):
        #recupero i job salvati
        if os.path.exists(self.file_job_dict):
            with open(self.file_job_dict, 'r') as file:
                r = csv.reader(file)
                for row in r:
                    key = str(row[0])
                    message = row[1]
                    address = (row[2], int(row[3]))
                    result = row[4]
                    if result =='N':
                        result = None
                    else:
                        result = int(result)
                    job_token_thread = (jt.JobToken(key, int(message), address, result))
                    self.job_dict.update({key: job_token_thread})

                    #aggiorno il job id al vecchio valore
                    if key.isnumeric() and int(key) > int(self.job_id):
                        self.job_id = int(key)

            self.job_id+=1

            #starto i job non ancora ultimati
            for key in self.job_dict:
                obj = self.job_dict[key]
                if not obj.result:
                    obj.start()

        self.routine_check()

        #recupero i forwarding
        if os.path.exists(self.file_job_forw):
            with open(self.file_job_forw, 'r') as file:
                r = csv.reader(file)
                for row in r:
                    jid= row[0]
                    temp= (row[1], int(row[2]))
                    new_job_id = row[3]
                    self.job_forw.update({jid:(temp, new_job_id)})

# -------------------------------------------------------------------------------------------------------

    def receving_job(self):


        while True:

            # io manterrei la comunicazione come le due linee di codice succesive ovvero una stringa separata da
            # 'comm.SEPARATOR' così poi puoi accedere ai parametri in modo facile con param[i]
            #
            # in addr hai il tuo mittente del messaggio
            try:
                data, addr = self.sk.recvfrom(1024)
                param = data.decode().split(comm.SEPARATOR)
            except:
                continue

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

    # -------------------------------------------------------------------------------------------------------

    def routine_check(self):

        # controllo dei job terminati
        self.l1.acquire()
        with open(self.file_job_dict, self.command, newline='') as file:
            for key in self.job_dict:
                obj = self.job_dict[key]
                if obj.result and not obj.check:
                    self.finished_job += 1
                    obj.check = True
                    wr = csv.writer(file)
                    wr.writerow([key, obj.parameter, obj.client_address[0], obj.client_address[1], obj.result])

        # conteggio

        self.job_count = len(self.job_dict) - self.finished_job
        self.l1.release()

    # -------------------------------------------------------------------------------------------------------

    # direct necessario per evitare catene di inoltro
    def job_exec_request(self, address, message, new_job_id, direct):

        address=(str(address[0]), int(address[1]))
        # mando al client l'id del job

        message=int(message)
        msg = str(self.job_id)
        #print(msg)
        if direct:
            self.sk.sendto(msg.encode(), address)

        self.l2.acquire()
        temp = self.owner.free_exec

        # inoltro
        if self.job_count > self.owner.threshold and direct: #and temp[1] != self.owner.executor_port:

            new_job_id = str(self.owner.id) +'-' + str(self.job_id)
            msg = comm.JOB_EXEC_REQ + comm.SEPARATOR + str(message) + comm.SEPARATOR + '0' \
                 + comm.SEPARATOR + str(address[0]) + comm.SEPARATOR + str(address[1]) + comm.SEPARATOR \
                + new_job_id

            #inoltro il job
            self.sk.sendto(str.encode(msg), temp)

            self.job_forw[str(self.job_id)] = (temp, new_job_id)

            #scrivo file
            with open(self.file_job_forw, self.command, newline='') as file:
                wr = csv.writer(file)
                wr.writerow([str(self.job_id), temp[0], temp[1], new_job_id])



        else:
            if direct:
                id=str(self.job_id)
            else:
                id=str(new_job_id)

            #TODO job token serve?
            #job_token_thread = jt.JobToken(self, id, int(message))
            #self.job_token_dict[self.i] = job_token_thread
            #self.jtoken_writer.writerow([str(self.i), id, message])
            #self.i += 1

            job_token_thread =(jt.JobToken(id, int(message), address))
            self.job_dict[id] = job_token_thread

            with open(self.file_job_dict, self.command, newline='') as file:
                wr = csv.writer(file)
                wr.writerow([id, message, address[0], address[1], 'N'])

            if not self.owner.is_leader:
                print('job_id' + str(id))
            job_token_thread.start()

        self.l2.release()
        self.job_id += 1

    # -------------------------------------------------------------------------------------------------------

    def responding_request_client(self,job_id, addr):
        if not self.owner.is_leader:
            print('job_request id: ' + str(job_id))

        self.result = None

        # se è nei forward inoltro la richiesta
        if job_id in self.job_forw.keys():
            try:
                self.sk.sendto(str.encode(comm.JOB_REQ_REQ + comm.SEPARATOR + str(self.job_forw[job_id][1])), self.job_forw[job_id][0])
            except Exception as e:
                print(e)
                return
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
                self.sk.sendto(str.encode("Job not Finished"), client_address)
        else:
            self.sk.sendto(str.encode("Job Uknown"), addr)

    # -------------------------------------------------------------------------------------------------------

    def run(self):
        self.receving_job()

