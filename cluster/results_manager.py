from threading import Thread
import messages as comm


class ResultsManager(Thread):
    def __init__(self,owner):
        Thread.__init__(self)
        self.owner=owner


    def receiving_request(self):


        while True:

         data, addr = self.owner.sk.recvfrom(1024)
         param = data.decode().split(comm.SEPARATOR)

         m=param[0]
         if m == comm.JOB_REQ_REQ:
            self.result = self.owner.job_dict[param[1]].result
            self.client_address = self.owner.job_dict[param[1]].client_address
            if  self.result != None :
                self.owner.sk.sendto(str.encode(str(self.result)),self.client_address)
            else :
                self.owner.sk.sendto(str.encode("Risultato ancora non calcolato"), self.client_address)










    def run(self):
        self.receiving_request()