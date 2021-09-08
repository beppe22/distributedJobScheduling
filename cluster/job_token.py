#!/usr/bin/env python3
import sys
import socket
from threading import Thread
from time import sleep
from cluster import job as j


class JobToken(Thread):
    def __init__(self,job_id,parameter, client_address, result=None, check=False):
        Thread.__init__(self)
        #self.owner=owner
        self.job_id = job_id
        self.parameter = parameter
        self.result = result
        self.client_address = client_address
        self.check = check
        #TODO dovrei killare

    def compute_result(self, ):
        sleep(15)
        #self.owner.job_dict[self.job_id].result= self.parameter * 2
        self.result = self.parameter * 2

    def run(self):
        self.compute_result()



