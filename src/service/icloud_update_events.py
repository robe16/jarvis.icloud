from time import sleep
from datetime import datetime

import cache
from resources.global_resources.log_vars import logPass, logFail
from resources.lang.enGB.logs import *

retrieval_frequency = 300  # 5 minutes


def eventUpdater_service():
    #
    while True:
        cache.cache['calendar']['events'] = {}
        #
        ####
        data = cache.cache['_icloud'].get_events()
        #
        cache.cache['calendar']['events'] = data['events']
        #
        # Logging
        result = logPass if data['status'] == 'ok' else logFail
        cache.logQ.put({'timestamp': datetime.now(),
                        'process': 'outbound', 'result': result,
                        'service_ip': '-',
                        'service_port': '',
                        'service_method': 'GET',
                        'service_request_uri': logDesc_icloud_uri_events,
                        'service_request_query': '-',
                        'service_request_body': '-',
                        'http_response_code': 'unknown',
                        'description': '-'})
        #
        ####
        #
        sleep(retrieval_frequency)
