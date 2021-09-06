#!/usr/bin/env python3

import os
import socket
from time import sleep
import messages as comm


# utile per avere un executor su ogni finestra
def main():

    count_client = input(comm.MESSAGE_NUMBER_CLIENT)
    for i in range(int(count_client)):
        client_port = comm.MIN_PORT_CLIENT + i
        os.system("start cmd.exe /k python3 -m client.client " + str(client_port))

if __name__ == "__main__":
    main()