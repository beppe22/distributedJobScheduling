#!/usr/bin/env python3

class Job:
    def __init__(self,job_id,parameter,IpClient,portClient):
        self.job_id = job_id
        self.parameter = parameter
        self.result = None
        self.done = False
        self.portClient=portClient
        self.IpClient=IpClient

    def do(self, ):
        pass

