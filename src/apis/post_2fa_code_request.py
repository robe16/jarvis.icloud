from bottle import HTTPResponse, HTTPError

from common_functions.request_enable_cors import enable_cors
from common_functions.request_log_args import get_request_log_args
from log.log import log_inbound
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *


def post_2fa_code_request(request, _icloud):
    #
    args = get_request_log_args(request)
    #
    try:
        r = _icloud.request_validation_code_default()
        #
        if r['result']:
            status = httpStatusSuccess
            args['result'] = logPass
        else:
            status = httpStatusFailure
            args['result'] = logFail
        #
        args['http_response_code'] = status
        args['description'] = '-'
        log_inbound(**args)
        #
        response = HTTPResponse()
        response.status = status
        response.body = r
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
        log_inbound(**args)
        #
        raise HTTPError(status)
