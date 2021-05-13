#!/usr/bin/python
#-*- coding: utf-8 -*-
from time import sleep
from threading import Thread
import sys


class Executor(Thread):
    def __init__(self, id_executor):
        Thread.__init__(self)
        self.id_executor = id_executor
        self.is_leader = None
        self.job_count = None
        self.threshold = None
        self.job_result = None

    def run_election(self, ):
        pass

    def send_job_count(self, ):
        pass

    def run(self):
        print("%d operativo!" % self.id_executor)



def main():
    Executor(int(sys.argv[1])).run()


if __name__ == "__main__":
    main()