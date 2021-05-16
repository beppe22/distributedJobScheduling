#!/usr/bin/env python3

import socket
from threading import Thread

from cluster import leader as ld
import messages as comm


class ElectionManager(Thread):
    def __init__(self, owner):
        Thread.__init__(self)
        self.owner = owner
        self.executor_port = self.owner.executor_port
        #self.my_id = self.executor_port
        self.elect_port = self.owner.elect_port
        self.first_start = False
        self.coord_wait = False
        # init broadcast
        self.elect_socket_broadcast = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)  # UDP
        self.elect_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.elect_socket_broadcast.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.elect_socket_broadcast.bind(("", self.elect_port))

    # resto nel loop in attesa di comunicazioni di ELECT
    def listen_all(self):

        sk = self.elect_socket_broadcast
        sk.settimeout(None)

        # questo id verrà aggiornato in futuro per supportare i cluster su macchine diverse
        my_id = self.owner.id

        # serve per evitare il flooding di messaggi. ci salviamo a quali id abbiamo già risposto
        reply_list = [int(my_id)]

        try:
            while True:

                data, addr = sk.recvfrom(1024)
                param = data.decode().split(comm.SEPARATOR)

                # controllo che non sia in attesa di un COORD e che non abbia già risposto alla stessa risposta di ELECT
                if param[0] == comm.ELECTMSG and not self.coord_wait and not int(param[1]) in reply_list:
                    # siamo in un elezione
                    self.owner.is_election = True
                    print(param[1])
                    self.run_election(int(param[1]), my_id)
                    reply_list.append(int(param[1]))
                    sk.settimeout(comm.COORD_TO)

                # accetto il messaggio di COORD e resto in attesa di nuove elezioni
                elif param[0] == comm.COORDMSG and int(param[1]) != my_id:
                    print('Nuovo Coordinatore ' + param[1] + ' in: '+param[2])
                    self.owner.leader_addr = (addr[0], int(param[2])+1)
                    self.owner.is_leader = False
                    self.owner.is_election = False
                    self.coord_wait = False
                    reply_list = [int(my_id)]
                    sk.settimeout(None)

                # altrimenti resto in attesa di COORD
                elif self.coord_wait:
                    sk.settimeout(comm.COORD_LOST_TO)

        # se non ricevo più messaggi di ELECT allora sono io il nuovo Leader, lo comunico e resto in attesa
        except Exception as e:
            #print(e)
            #traceback.print_exc()
            if self.coord_wait:
                print("COORD LOST")
                self.coord_wait = False
                self.run_election()
                self.listen_all()
            else:
                print('coord')
                self.declare_coord()
                self.listen_all()

    # mi dichiaro vincitore delle elezioni
    def declare_coord(self):
        msg = comm.COORDMSG + comm.SEPARATOR + str(self.owner.id) + comm.SEPARATOR + str(self.executor_port)
        print(msg)
        self.elect_socket_broadcast.sendto(msg.encode(), ('<broadcast>', self.elect_port))
        data, addr = self.elect_socket_broadcast.recvfrom(1024)  # mangio il mio COORD
        self.owner.leader_addr = (addr[0], self.owner.executor_port+1)
        self.owner.is_leader = True
        self.owner.leader = ld.Leader(self.owner)
        self.owner.leader.start()
        self.owner.is_election = False
        self.coord_wait = False

    # avvio un elezione. i valori di default sono necessari per provocare un elezione di massa in tutto il cluster
    def run_election(self, starter_id=0, my_id=0):
        self.owner.is_election = True

        # verifico il rank di chi ha mandato la ELECT
        if starter_id > my_id:
            # sono più basso, mi metto in attesa
            self.coord_wait = True
            print('WAITING')
            return

        # mando il mio messaggio di ELECT e mi rimetto in attesa
        msg = comm.ELECTMSG + comm.SEPARATOR + str(my_id)
        self.elect_socket_broadcast.sendto(msg.encode(), ('<broadcast>', self.elect_port))
        return

    def run(self):
        self.listen_all()
