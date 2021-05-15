#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
import sys
from time import sleep

from ElectionManager import *
from Leader import *
from Updater import *
from MessageDefinition import *

flag = False

# se avviato da StarterCMD è una classe normale, se avviato usando Starter utilizziamo i thread


class Executor(Thread):
    def __init__(self, elect_port, update_port, executor_port, start_election=False):
        Thread.__init__(self)

        # connessioni
        self.executor_port = int(executor_port)

        self.elect_port = int(elect_port)
        self.elect_manager = ElectionManager(self)

        self.update_port = int(update_port)
        self.updater = Updater(self)

        # id- deve essere un intero!
        self.id = self.executor_port

        # leader info
        self.leader_addr = None

        # other flags
        self.is_election = True
        self.is_leader = False
        self.leader = None

        self.job_count = 0
        self.threshold = None
        self.job_result = None

        self.start_election = start_election

    def run(self):

        # faccio partire l'elect manager. se viene avviato senza StarterCMD serve un elezione "forzata"
        self.elect_manager.start()
        self.updater.start()
        if self.start_election:
            self.elect_manager.run_election()


def main():
    # se avviato tramite linea di comando
    if len(sys.argv) > 1:
        Executor(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3])).run()
    else:
        # se avviato per aggiungere un executor dopo aver creato il cluster
        Executor(BROAD_EL_PORT, BROAD_UP_PORT, 50000, True).run()


if __name__ == "__main__":
    main()
