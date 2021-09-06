#!/usr/bin/env python3
import sys
import socket
from threading import Thread
from time import sleep
from cluster import job as j


class JobToken(Thread):
    def __init__(self,owner,job_id,parameter,client_address):
        Thread.__init__(self)
        self.owner=owner
        self.job_id = job_id
        self.parameter = parameter
        self.client_address= client_address
        self.result=None


        #TODO dovrei killare

    def compute_result(self, ):

        self.result = self.parameter * 2
        self.owner.job_dict[self.job_id] = (j.Job(self.job_id, int(self.parameter), self.result, self.client_address))

        sleep(3)

    def run(self):
        self.compute_result()



