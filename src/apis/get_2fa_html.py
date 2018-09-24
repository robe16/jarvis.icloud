import os
from datetime import datetime
from bottle import HTTPResponse, HTTPError

import cache
from common_functions.request_enable_cors import enable_cors
from common_functions.request_log_args import get_request_log_args
from resources.global_resources.log_vars import logPass, logException
from resources.global_resources.variables import *


def get_2fa_html(request):
    #
    args = get_request_log_args(request)
    args['timestamp'] = datetime.now()
    args['process'] = 'inbound'
    #
    try:
        with open(os.path.join(os.path.dirname(__file__), '..', 'service/2fa/2fa.html'), 'r') as f:
            page_body = f.read()
        #
        status = httpStatusSuccess
        args['result'] = logPass
        #
        args['http_response_code'] = status
        args['description'] = '-'
        cache.logQ.put(args)
        #
        response = HTTPResponse()
        response.status = status
        response.body = page_body
        enable_cors(response)
        #
        return response
        #
    except Exception as e:
        #
        status = httpStatusServererror
        #
        args['result'] = logException
        args['http_response_code'] = status
        args['description'] = '-'
        args['exception'] = e
        cache.logQ.put(args)
        #
        raise HTTPError(status)
