#!/usr/bin/env python3
import os
import sys
import socket
import threading
from threading import Thread
from time import sleep

from cluster import updater as up
from cluster import election as el
from cluster import job_manager as jm
import messages as comm


flag = False
# se avviato da StarterCMD è una classe normale, se avviato usando Starter utilizziamo i thread


class Executor(Thread):
    def __init__(self, group_id, elect_port, update_port, executor_port, start_election, restart=0):
        Thread.__init__(self)
        # job_count_lock
        # id- deve essere un intero!
        l1 = threading.RLock()
        l2 = threading.RLock()

        # connessioni
        self.executor_port = int(executor_port)
        self.port_for_job = executor_port+2
        self.group_id = group_id
        self.id = int(str(group_id) + str(self.executor_port))
        print(self.id)

        self.elect_port = int(elect_port)
        self.elect_manager = el.ElectionManager(self)

        self.update_port = int(update_port)
        self.updater = up.Updater(self,l1, l2)

        # dizionario dei job
        #self.job_dict = {}

        self.job_manager = jm.JobManager(self,l1, l2, restart)



        # leader info
        self.leader_addr = None

        # other flags
        self.is_election = True
        self.is_leader = False
        self.leader = None

        # tupla con indirizzo dell'executor libero al momento
        self.free_exec = (0,)

        # qui o usiamo il contatore job_count oppure usiamo direttamente la dimensione della lista.
        #self.job_count = 0
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

        #job_manager gestisce pure i pingpong
        self.job_manager.start()

        #self.exec_stuff()

        #self.receiving_result()


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
        Executor(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), int(sys.argv[6])).start()
    else:
        # se avviato per aggiungere un executor dopo aver creato il cluster
        Executor(0, comm.BROAD_EL_PORT, comm.BROAD_UP_PORT, 50000, 1).start()


if __name__ == "__main__":
    main()
