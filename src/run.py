from multiprocessing import Process
from datetime import datetime

import cache
from log.logging import logging_service
from service.start_service import start_service
from discovery.broadcast import broadcast_service
from resources.lang.enGB.logs import *
from resources.global_resources.log_vars import logPass, logException
from config.config import get_cfg_serviceid, get_cfg_port
from server import start_server


try:
    cache.logQ.put({'timestamp': datetime.now(),
                    'process': 'internal', 'result': logPass,
                    'operation': logDescStartingService, 'description': 'started'})
    ################################
    # Initiate logging
    process_logging = Process(target=logging_service)
    process_logging.start()
    ################################
    # Initiate service broadcast
    process_broadcast = Process(target=broadcast_service, args=(get_cfg_serviceid(), get_cfg_port(), ))
    process_broadcast.start()
    ################################
    # Start service code
    start_service()
    ################################
    # Port_listener
    cache.logQ.put({'timestamp': datetime.now(),
                    'process': 'internal', 'result': logPass,
                    'operation': logDescPortListener.format(port=get_cfg_port()), 'description': 'starting'})
    start_server()
    cache.logQ.put({'timestamp': datetime.now(),
                    'process': 'internal', 'result': logPass,
                    'operation': logDescPortListener.format(port=get_cfg_port()), 'description': 'stopped'})
    ################################
    # Process termination if start_server() ends (i.e. crashes)
    process_logging.terminate()
    process_broadcast.terminate()

except Exception as e:
    cache.logQ.put({'timestamp': datetime.now(),
                    'process': 'internal', 'result': logException,
                    'operation': logDescStartingService, 'description': 'fail', 'exception': e})
