#!/usr/bin/env python3
import sys
import socket
from threading import Thread
from time import sleep
from cluster import job as j


class JobToken(Thread):
    def __init__(self,owner,job_id,parameter):
        Thread.__init__(self)
        self.owner=owner
        self.job_id = job_id
        self.parameter = parameter
        self.result=None


        #TODO dovrei killare

    def compute_result(self, ):
        sleep(10)
        self.owner.job_dict[self.job_id].result= self.parameter * 2

        sleep(3)

    def run(self):
        self.compute_result()



