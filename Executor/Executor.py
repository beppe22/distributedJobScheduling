#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
import sys
from time import sleep

from ElectionManager import *
from Updater import *
from MessageDefinition import *

flag = False

# se avviato da StarterCMD è una classe normale, se avviato usando Starter utilizziamo i thread

class Executor(Thread):
    def __init__(self, elect_port, executor_port, start_election=0):
        Thread.__init__(self)

        # connessioni
        self.executor_port = int(executor_port)
        self.b_port = int(elect_port)
        self.elect_manager = ElectionManager(self, self.b_port, self.executor_port)

        # leader info
        self.leader_port = None
        self.leader_ip = None

        # other flags
        self.is_election = None
        self.is_leader = None

        self.job_count = None
        self.threshold = None
        self.job_result = None

        self.start_election = start_election

    def run(self):

        # faccio partire l'elect manager. se viene avviato senza StarterCMD serve un elezione "forzata"
        self.elect_manager.start()
        if self.start_election:
            self.elect_manager.run_election()


def main():
    # se avviato tramite linea di comando
    if len(sys.argv) == 3:
        Executor(int(sys.argv[1]), int(sys.argv[2])).run()
    else:
        # se avviato per aggiungere un executor dopo aver creato il cluster
        Executor(BROAD_EL_PORT, 49255, 1).run()


if __name__ == "__main__":
    main()
