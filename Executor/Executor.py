#!/usr/bin/python
# -*- coding: utf-8 -*-
from threading import Thread
import sys
from time import sleep

from ElectionManager import *
from Updater import *
from MessageDefinition import *


# se avviato da StarterCMD è una classe normale, se avviato usando Starter utilizziamo i thread

class Executor(Thread):
    def __init__(self, elect_port, executor_port):
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

    def run(self):
        sleep(3)
        self.elect_manager.listen_all()


def main():
    if len(sys.argv) == 3:
        Executor(int(sys.argv[1]), int(sys.argv[2])).run()
    else:
        Executor(BROAD_EL_PORT, MINPORT+100).run()


if __name__ == "__main__":
    main()
