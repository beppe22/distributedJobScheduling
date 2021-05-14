import os

from MessageDefinition import *

MESSAGE = 'Quanti executors vuoi avviare?'


# utile per avere un executor su ogni finestra
def main():
    count = input(MESSAGE)
    for i in range(int(count)):
        port = MINPORT+(i*2)
        os.system("start cmd.exe /k python3 Executor.py "+str(BROAD_EL_PORT)+" "+str(port))


if __name__ == "__main__":
    main()