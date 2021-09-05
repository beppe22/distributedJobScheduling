import socket
from threading import Thread
from cluster import job as j
import job_token as jt


class JobManager(Thread):
    def __init__(self, owner):
        Thread.__init__(self)
        self.owner=owner


    def receving_job(self):

        self.job_id = 0


        self.owner.UDPExecutorSocket.bind(("", self.owner.executor_port))

        while (True):
            bytesAddressPair = self.owner.UDPExecutorSocket.recvfrom(1024)
            message = bytesAddressPair[0]
            address = bytesAddressPair[1]

            clientMsg = "Messagge from client:{}".format(message)
            clientAddress = "client address:{}".format(address)
            print(clientMsg)
            print(clientAddress)

            #mando al client l'id del job
            self.owner.UDPExecutorSocket.sendto(str.encode(str(self.job_id)),address)

            # TODO fare i controlli per vedere se executor non ha superato threshold

            self.owner.job_dict[self.job_id] = (j.Job(self.job_id, int(message), address[0], address[1]))

            jt.JobToken(self,str(self.job_id),str(int(message)),self.owner.port_for_job,
                             str(socket.gethostname())).start()

            self.job_id += 1









    def run(self):
        self.receving_job()