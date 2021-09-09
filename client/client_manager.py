import random
from threading import Thread
from time import sleep
import messages as comm
import socket


class ClientManager(Thread):
    def __init__(self,owner,port):
        Thread.__init__(self)
        self.owner=owner
        self.number= None
        self.my_ip= socket.gethostbyname(socket.gethostname())
        self.IpServer= self.my_ip
        self.PortServer= 49300
        self.UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
        self.UDPClientSocket.bind((self.my_ip, port))
        self.UDPClientSocket.settimeout(comm.TIMEOUT_CLIENT)



    def send_job(self):
        self.number = input(comm.MESSAGE_TO_CLIENT)
        if not self.number.isnumeric():
            self.number = random.randint(1,50)
            print(self.number)

        bytesToSend= str.encode(comm.JOB_EXEC_REQ + comm.SEPARATOR + str(self.number) + comm.SEPARATOR + '1' +
                                comm.SEPARATOR + '')
        try:
            self.UDPClientSocket.sendto(bytesToSend, (str(self.IpServer), int(self.PortServer)))
            self.receiving_job_id()
        except Exception as e:
            print(comm.ERR)
            self.input_addr()
            return

    def receiving_job_id(self):
        job_id= None

        msg, addr = self.UDPClientSocket.recvfrom(1024)
        job_id = msg.decode()
        print(comm.JOB_ID_RPL + str(job_id))

        return job_id



    def receiving_result(self):

        job_choice= input(comm.JOB_ID_REQ)

        try:
            self.UDPClientSocket.sendto(str.encode(comm.JOB_REP_REQ + comm.SEPARATOR + str(job_choice)), (str(self.IpServer), int(self.PortServer)))
            messageFromServer, addr = self.UDPClientSocket.recvfrom(1024)
        except socket.timeout:
            print(comm.TIME)
            return
        except Exception as e:
            print(comm.ERR)
            self.input_addr()
            return

        print(comm.RESULT)
        print(messageFromServer.decode())

    def input_addr(self):
        ip = input(comm.ADDRESS_REQ)
        port = input(comm.PORT_REQ)

        if len(ip)>=7:
            self.IpServer = ip
        if port.isnumeric() and int(port)>=49300:
            self.PortServer = int(port)

    def auto_mode(self):
        tot=comm.JOBAUTO_N
        job_sent= {}

        self.auto_send(tot, job_sent)
        input('\nPress a enter to check')

        self.auto_recall(job_sent)
        input('\nPress a enter to check again')
        self.auto_recall(job_sent)

        self.run()


    def auto_send(self, tot, job_sent):
        flag=tot
        while tot:
            number = random.randint(1, 500)
            print(number)

            bytesToSend = str.encode(comm.JOB_EXEC_REQ + comm.SEPARATOR + str(number) + comm.SEPARATOR + '1' +
                                     comm.SEPARATOR + '')
            try:
                self.UDPClientSocket.sendto(bytesToSend, (str(self.IpServer), int(self.PortServer)))
                id = self.receiving_job_id()
                # print(id)
                job_sent.update({id: number})
                tot -= 1

            except socket.timeout:
                print(comm.TIME)

            except Exception as e:
                if flag == tot:
                    print(comm.ERR)
                    self.input_addr()
                else:
                    input('Worker is Recovering, Press enter when ready')


            sleep(comm.TIK)


    def auto_recall(self, job_sent, f= False):
        temp={}
        error=0
        flag= f
        for i in job_sent:
            #print(i)
            try:
                self.UDPClientSocket.sendto(str.encode(comm.JOB_REP_REQ + comm.SEPARATOR + str(i)),
                                            (str(self.IpServer), int(self.PortServer)))
                messageFromServer, addr = self.UDPClientSocket.recvfrom(1024)

                res = messageFromServer.decode()

                flag= True
                if res.isnumeric() and int(res)==(job_sent.get(i)*2):
                    print(str(i) + ' ok')
                elif not res.isnumeric():
                    print(res)
                else:
                    print(str(i) + ' error' )
                    error += 1


            except socket.timeout:
                print(comm.TIME)
                temp.update({i: job_sent.get(i)})


            except Exception as e:
                if not flag:
                    print(comm.ERR)
                    self.input_addr()
                else:
                    sleep(1)
                    print(comm.TIME)
                    temp.update({i: job_sent.get(i)})

            sleep(comm.TIK)

        print("Error found: " + str(error) + '\n')

        if len(temp):
            print("\nchecking again not available jobs:")
            sleep(2)
            self.auto_recall(temp, True)

    def run(self):
        print(self.my_ip)
        print(comm.LINE)
        self.input_addr()
        print(comm.LINE)

        if input("auto mode press 1: "):
            self.auto_mode()

        while True:

            answer = input(comm.COMMAND_CHOICE)

            if answer =='1':
                self.receiving_result()
            elif answer =='2':
                self.input_addr()
            else:
                self.send_job()
            print(comm.LINE)
            sleep(comm.TIK)



