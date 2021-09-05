#!/usr/bin/env python3
import os
import sys
import socket
from threading import Thread
from time import sleep

from cluster import updater as up
from cluster import election as el
import messages as comm
from cluster import job as j

flag = False
# se avviato da StarterCMD è una classe normale, se avviato usando Starter utilizziamo i thread


class Executor(Thread):
    def __init__(self, group_id, elect_port, update_port, executor_port,port_for_job, start_election=False):
        Thread.__init__(self)

        # connessioni
        self.executor_port = int(executor_port)
        self.port_for_job=port_for_job

        self.elect_port = int(elect_port)
        self.elect_manager = el.ElectionManager(self)

        self.update_port = int(update_port)
        self.updater = up.Updater(self)

        # id- deve essere un intero!
        self.group_id = group_id
        self.id = int(str(group_id)+str(self.executor_port))
        print(self.id)

        # leader info
        self.leader_addr = None

        # other flags
        self.is_election = True
        self.is_leader = False
        self.leader = None

        # tupla con indirizzo dell'executor libero al momento
        self.free_exec = (0,)

        # qui o usiamo il contatore job_count oppure usiamo direttamente la dimensione della lista.
        self.job_count = 0
        #valore arbitrario
        self.threshold = 5
        self.job_result = None

        self.start_election = start_election

    def run(self):

        # faccio partire l'elect manager. se viene avviato senza StarterCMD serve un elezione "forzata"
        self.elect_manager.start()
        self.updater.start()
        if self.start_election:
            self.elect_manager.run_election()
        #self.exec_stuff()
        self.receiving_job()

        self.receiving_result()


    def receiving_job(self):

        self.job=0
        self.job_dict={}

        self.UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPServerSocket.bind(("", self.executor_port))
        while(True):

            bytesAddressPair= self.UDPServerSocket.recvfrom(1024)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]


            clientMsg ="Messagge from client:{}".format(message)
            clientAddress = "client address:{}".format(address)
            print(clientMsg)
            print(clientAddress)

            #TODO fare i controlli per vedere se executor non ha superato threshold

            self.job_dict[self.job]=(j.Job(self.job,int(message),address[0],address[1]))
            os.system("start cmd.exe /k python3 -m job_token " +str(self.job) + ' ' + str(int(message)) +
                      ' ' + str(self.port_for_job) + ' ' + str(socket.gethostname()))

            self.job += 1
            break

    def receiving_result(self):


        UDPReceivingSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        UDPReceivingSocket.bind(("",int(self.port_for_job)))
        while (True):
            bytesAddressPair = UDPReceivingSocket.recvfrom(1024)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            #clientMsg = "risultato:{}".format(message.split()[0])
            #indice= message.split()[1]
            #print(clientMsg)
            #print(indice)

            client_Ip= self.job_dict[int(message.split()[1])].IpClient
            client_port = self.job_dict[int(message.split()[1])].portClient
            client_address= (str(client_Ip),int(client_port))
            self.UDPServerSocket.sendto(str.encode(str(int(message.split()[0]))),client_address)

            self.job_dict.pop(int(message.split()[1]),"Element not found")







    def exec_stuff(self):
        while True:
            while self.is_election or self.is_leader:
                sleep(3)
                pass
            print(str(self.free_exec) + ' ' + str(self.threshold))
            sleep(1)


def main():
    # se avviato tramite linea di comando
    if len(sys.argv) > 1:
        Executor(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5])).start()
    else:
        # se avviato per aggiungere un executor dopo aver creato il cluster
        Executor(0, comm.BROAD_EL_PORT, comm.BROAD_UP_PORT, 50000, True).start()


if __name__ == "__main__":
    main()
