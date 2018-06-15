from datetime import datetime
from bottle import HTTPResponse, HTTPError

from common_functions.request_enable_cors import enable_cors
from common_functions.request_log_args import get_request_log_args
from log.log import log_inbound
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *


def get_calendar_daterange(request, _icloud, option, dateFrom, dateTo):
    #
    args = get_request_log_args(request)
    #
    try:
        # '_dateFrom' and '_dateTo' should be in format "yyyy-mm-dd"
        _dateFrom = datetime.strptime(dateFrom, '%Y-%m-%d')
        _dateTo = datetime.strptime(dateTo, '%Y-%m-%d')
        #
        if option == str_calendar_events:
            data = {str_calendar_events: _icloud.get_events_daterange(_dateFrom, _dateTo)}
        elif option == str_calendar_birthdays:
            data = {str_calendar_birthdays: _icloud.get_birthdays_daterange(_dateFrom, _dateTo)}
        else:
            data = False
        #
        if not bool(data):
            status = httpStatusFailure
            args['result'] = logFail
        else:
            status = httpStatusSuccess
            args['result'] = logPass
        #
        args['http_response_code'] = status
        args['description'] = '-'
        log_inbound(**args)
        #
        response = HTTPResponse()
        response.status = status
        enable_cors(response)
        #
        if not isinstance(data, bool):
            response.body = data
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
