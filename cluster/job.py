#!/usr/bin/env python3

class Job:
    def __init__(self,job_id,parameter,result, client_address):
        self.job_id = job_id
        self.parameter = parameter
        self.result = result
        self.done = False
        self.client_address = client_address

    def do(self, ):
        pass

