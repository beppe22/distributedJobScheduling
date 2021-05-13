import os

MESSAGE = 'Quanti executors vuoi avviare?'
MINPORT = '49152'


def main():
    count = input(MESSAGE)
    for i in range(int(count)):
        port = int(MINPORT)+(i*2)
        os.system("start cmd.exe /k python3 Executor.py "+str(port))


if __name__ == "__main__":
    main()