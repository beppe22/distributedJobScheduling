import os

MESSAGE = 'Quanti executors vuoi avviare?'
MINPORT = 49153
BROD_PORT = 49152

# utile per avere un executor su ogni finestra
def main():
    count = input(MESSAGE)
    for i in range(int(count)):
        port = MINPORT+(i*2)
        os.system("start cmd.exe /k python3 Executor.py "+str(BROD_PORT)+" "+str(port))


if __name__ == "__main__":
    main()