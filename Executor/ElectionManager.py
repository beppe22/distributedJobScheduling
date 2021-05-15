import socket
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
        my_id = self.executor_port

        # serve per evitare il flooding di messaggi. ci salviamo a quali id abbiamo già risposto
        reply_list = [int(my_id)]

        try:
            while True:

                data, addr = sk.recvfrom(1024)
                param = data.decode().split(SEPARATOR)

                # controllo che non sia in attesa di un COORD e che non abbia già risposto alla stessa risposta di ELECT
                if param[0] == ELECTMSG and not self.coord_wait and not int(param[1]) in reply_list:
                    # siamo in un elezione
                    self.owner.is_election = True
                    print(param[1])
                    self.run_election(int(param[1]), my_id)
                    reply_list.append(int(param[1]))
                    sk.settimeout(ELTIMEOUT)

                # accetto il messaggio di COORD e resto in attesa di nuove elezioni
                elif param[0] == COORDMSG and int(param[1]) != my_id:
                    print('Nuovo Coordinatore ' + param[1] + ' ' + str(addr))
                    self.owner.is_election = False
                    self.coord_wait = False
                    reply_list = [int(my_id)]

                # altrimenti resto in attesa di COORD
                elif self.coord_wait:
                    sk.settimeout(None)

        # se non ricevo più messaggi di ELECT allora sono io il nuovo Leader, lo comunico e resto in attesa
        except:
            print('coord')
            self.declare_coord()
            sk.recvfrom(1024)  # mangio il mio COORD
            self.listen_all()

    # mi dichiaro vincitore delle elezioni
    def declare_coord(self):
        msg = COORDMSG + SEPARATOR + str(self.my_id)
        print(msg)
        self.elect_socket_broadcast.sendto(msg.encode(), ('<broadcast>', BROAD_EL_PORT))
        self.owner.is_election = False
        self.owner.is_leader = True
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
        msg = ELECTMSG + SEPARATOR + str(my_id)
        self.elect_socket_broadcast.sendto(msg.encode(), ('<broadcast>', BROAD_EL_PORT))
        return

    def run(self):
        self.listen_all()
