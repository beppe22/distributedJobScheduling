from Executor import Executor


MESSAGE = 'Quanti executors vuoi avviare?'
MINPORT = '49152'


exec_list = []

def main():
    count = input(MESSAGE)
    for i in range(int(count)):
        temp_exec = Executor((i*2)+int(MINPORT))
        exec_list.append(temp_exec)
        print(temp_exec.id_executor)

    for e in exec_list:
        e.start()


if __name__ == "__main__":
    main()
