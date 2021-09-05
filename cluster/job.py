#!/usr/bin/env python3

class Job:
    def __init__(self,job_id,parameter,result,IpClient,portClient):
        self.job_id = job_id
        self.parameter = parameter
        self.result = result
        self.done = False
        self.portClient=portClient
        self.IpClient=IpClient

    def do(self, ):
        pass

