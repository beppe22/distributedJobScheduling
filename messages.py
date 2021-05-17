#!/usr/bin/env python3
MESSAGE = "quanti exec vuoi avviare?"
MESSAGE_GID = "group id:"
ELECTMSG = "ELECT"
SEPARATOR = ":"
COORDMSG = "COORD"

# il minimo delle porte usate dovrebbe essere 49152
MINPORT = 49154
BROAD_EL_PORT = 49152
BROAD_UP_PORT = 49153

# dopo quanti secondi posso dichiararmi vincitore
COORD_TO = 2

# per quanto resto in attesa di un COORD durante un elezione
COORD_LOST_TO = 10

# dopo quanti sec il leader viene considerato offline
LEADER_OFFLINE_TO = 3

# ogni quanto il leader manda aggiornamenti
STEP = 1
