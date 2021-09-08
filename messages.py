#!/usr/bin/env python3
WAIT = "premi per continuare"
MESSAGE = "quanti exec vuoi avviare?"
MESSAGE_ALREADY = "quanti exec hai già avviato?"
MESSAGE_NUMBER_CLIENT= "quanti client vuoi avviare?"
MESSAGE_GID = "group id:"
ELECTMSG = "ELECT"
SEPARATOR = ":"
COORDMSG = "COORD"



# il minimo delle porte usate dovrebbe essere 49152
MINPORT = 49300
C2C_PORT= 49152
BROAD_EL_PORT = 49153
BROAD_UP_PORT = 49154
MIN_PORT_CLIENT = 49155

# dopo quanti secondi posso dichiararmi vincitore
COORD_TO = 2

# per quanto resto in attesa di un COORD durante un elezione
COORD_LOST_TO = 10

# dopo quanti sec il leader viene considerato offline
LEADER_OFFLINE_TO = 3

# dopo quanti sec exec viene considerato offline
EXEC_OFFLINE_TO = 5

# ogni quanto il leader manda aggiornamenti
STEP = 0

##COMANDI REMOTI CLIENT
JOB_EXEC_REQ = 'JOB_EXEC_REQ'
JOB_RES_REQ = 'JOB_RES_REQ'
JOB_REQ_REQ = 'JOB_REQ_REQ'

JOB_UNFINISHED = 'JOB_UNFINISHED'
JOB_RESULT = 'JOB_RESULT'

PING = 'PING'
PONG = 'PONG'

#CLIENT
LINE = '------------------------------------------------'
COMMAND_CHOICE = ' Choose:\n  0- send a new JOB \n  1- recall result using JOB_ID \n'\
                    '  2- edit worker address\n'
ADDRESS_REQ = " Insert worker IP: "
PORT_REQ = " Insert worker PORT: "

MESSAGE_TO_CLIENT = " Type the JOB input number: "
ERR= ' Wrong address?'
TIME= ' Worker may be offline, retry later'
JOB_ID_REQ=' Insert the JOB_ID: '
JOB_ID_RPL=' JOB_ID: '
RESULT= " The result is: "

TIK =0.1
JOBAUTO_N= 500
TIMEOUT_CLIENT= 6
#WORKER
WERR= ' Wrong number?'
