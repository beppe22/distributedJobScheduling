from Executor import Executor


MESSAGE = 'Quanti executors vuoi avviare?'
MINPORT = '49153'
BROD_PORT = '49152'

exec_list = []

def main():
    count = input(MESSAGE)
    for i in range(int(count)):
        temp_exec = Executor(BROD_PORT, (i*2)+int(MINPORT))
        exec_list.append(temp_exec)

    for e in exec_list:
        e.start()


if __name__ == "__main__":
    main()
