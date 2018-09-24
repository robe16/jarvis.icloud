from time import sleep
from datetime import datetime

import cache
from resources.global_resources.log_vars import logPass, logFail
from resources.lang.enGB.logs import *

retrieval_frequency = 600  # 10 minutes


def birthdayUpdater_service():
    #
    while True:
        cache.cache['calendar']['birthdays'] = []
        #
        ####
        data = cache.cache['_icloud'].get_birthdays()
        #
        cache.cache['calendar']['birthdays'] = data['birthdays']
        #
        # Logging
        result = logPass if data['status'] == 'ok' else logFail
        cache.logQ.put({'timestamp': datetime.now(),
                        'process': 'outbound', 'result': result,
                        'service_ip': '-',
                        'service_port': '',
                        'service_method': 'GET',
                        'service_request_uri': logDesc_icloud_uri_birthdays,
                        'service_request_query': '-',
                        'service_request_body': '-',
                        'http_response_code': 'unknown',
                        'description': '-'})
        #
        ####
        #
        sleep(retrieval_frequency)
