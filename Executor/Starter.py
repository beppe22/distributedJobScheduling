from Executor.Executor import Executor
from MessageDefinition import *


MESSAGE = 'Quanti executors vuoi avviare?'

exec_list = []

def main():
    count = input(MESSAGE)
    for i in range(int(count)):
        temp_exec = Executor(BROAD_EL_PORT, (i*2)+int(MINPORT))
        exec_list.append(temp_exec)

    for e in exec_list:
        e.start()


if __name__ == "__main__":
    main()
