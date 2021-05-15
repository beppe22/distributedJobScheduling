import socket
from time import sleep
from threading import Thread

from MessageDefinition import *


class ElectionManager(Thread):
    def __init__(self, owner, b_port, executor_port):
        Thread.__init__(self)
        self.executor_port = int(executor_port)
        self.my_id = self.executor_port
        self.elect_port = int(b_port)
        self.owner = owner
        self.first_start = False
        self.coord_wait = False
        # init
        self.elect_socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.elect_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.elect_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.elect_socket_broadcast.bind(("", self.elect_port))

    def listen_all(self):
        # avvio broadcast

        sk = self.elect_socket_broadcast
        # primo avvio
        #if self.first_start:
         #   print('firststart')
          #  self.run_election()
           # self.first_start = False

        sk.settimeout(None)
        # inizializzo il timer
        my_id = self.executor_port
        try:
            while True:
                data, addr = sk.recvfrom(1024)
                param = data.decode().split(SEPARATOR)

                if param[0] == ELECTMSG and not self.coord_wait and int(param[1]) != my_id:

                    # siamo in un elezione
                    self.owner.is_election = True
                    print(param[1])
                    self.run_election(int(param[1]), my_id)
                    sk.settimeout(ELTIMEOUT)

                elif param[0] == COORDMSG and int(param[1]) != my_id:
                    print('Nuovo Coordinatore ' + param[1] + ' ' + str(addr))
                    self.owner.is_election = False
                    self.coord_wait = False

                if self.coord_wait:
                    sk.settimeout(None)
                sleep(STEP)

        except:
            print('coord')
            self.declare_coord()
            sk.recvfrom(1024) # mangio il mio coord
            sleep(STEP)
            self.listen_all()

    def declare_coord(self):
        msg = COORDMSG + SEPARATOR + str(self.my_id)
        print(msg)
        self.elect_socket_broadcast.sendto(msg.encode(), ('<broadcast>', BROAD_EL_PORT))
        self.owner.is_election = False
        self.owner.is_leader = True
        self.coord_wait = False

    def run_election(self, starter_id=0, my_id=0):
        print('mando elect')

        # sta runnando un elezione
        self.owner.is_election = True

        # verifico il rank di chi ha runnato la elect
        if starter_id > my_id:
            # mi metto in attesa
            self.coord_wait = True
            print('WAITING')
            return

        # se sono più alto mando msg elect
        msg = ELECTMSG + SEPARATOR + str(my_id)
        self.elect_socket_broadcast.sendto(msg.encode(), ('<broadcast>', BROAD_EL_PORT))
        # aspetto altri elect
        return

    def run(self):
        self.listen_all()