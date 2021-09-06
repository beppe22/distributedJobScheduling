#!/usr/bin/env python3
MESSAGE = "quanti exec vuoi avviare?"
MESSAGE_NUMBER_CLIENT= "quanti client vuoi avviare?"
MESSAGE_GID = "group id:"
ELECTMSG = "ELECT"
SEPARATOR = ":"
COORDMSG = "COORD"
MESSAGE_TO_CLIENT = "give me the number to elaborate"


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
EXEC_OFFLINE_TO = 3

# ogni quanto il leader manda aggiornamenti
STEP = 0.3

##COMANDI REMOTI CLIENT
JOB_EXEC_REQ = 'JOB_EXEC_REQ'
JOB_RES_REQ = 'JOB_RES_REQ'

JOB_UNFINISHED = 'JOB_UNFINISHED'
JOB_RESULT = 'JOB_RESULT'

PING = 'PING'
PONG = 'PONG'
