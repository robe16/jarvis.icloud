from time import sleep
from datetime import datetime

import cache
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.lang.enGB.logs import *

retrieval_frequency = 600  # 10 minutes


def birthdayUpdater_service():
    #
    while True:
        #
        if cache.cache['_2fa/2sv-complete']:
            #
            cache.cache['calendar']['birthdays'] = []
            #
            log_args = {'timestamp': datetime.now(),
                        'process': 'outbound',
                        'service_ip': '-',
                        'service_port': '',
                        'service_method': 'GET',
                        'service_request_uri': logDesc_icloud_uri_events,
                        'service_request_query': '-',
                        'service_request_body': '-',
                        'http_response_code': 'unknown',
                        'description': '-'}
            #
            ####
            #
            try:
                data = cache.cache['_icloud'].get_birthdays()
                cache.cache['calendar']['birthdays'] = data
                log_args['result'] = logPass if len(data) else logFail
            except Exception as e:
                log_args['result'] = logException
                log_args['exception'] = e
            #
            cache.logQ.put(log_args)
            ####
            #
            sleep(retrieval_frequency)
            #
        else:
            #
            sleep(10)
