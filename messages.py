#!/usr/bin/env python3
MESSAGE = "quanti exec vuoi avviare?"
MESSAGE_NUMBER_CLIENT= "quanti client vuoi avviare?"
MESSAGE_GID = "group id:"
ELECTMSG = "ELECT"
SEPARATOR = ":"
COORDMSG = "COORD"
MESSAGE_TO_CLIENT = "give me the number to elaborate"


# il minimo delle porte usate dovrebbe essere 49152
MINPORT = 49154
MINPORTFORJOB= 49180
BROAD_EL_PORT = 49152
BROAD_UP_PORT = 49153
MIN_PORT_CLIENT = 49200

# dopo quanti secondi posso dichiararmi vincitore
COORD_TO = 2

# per quanto resto in attesa di un COORD durante un elezione
COORD_LOST_TO = 10

# dopo quanti sec il leader viene considerato offline
LEADER_OFFLINE_TO = 3

# ogni quanto il leader manda aggiornamenti
STEP = 0.3
