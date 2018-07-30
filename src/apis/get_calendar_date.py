from datetime import datetime
from bottle import HTTPResponse, HTTPError

from common_functions.request_log_args import get_request_log_args
from log.log import log_inbound
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *


def get_calendar_date(request, _icloud, option, dateSpecific):
    #
    args = get_request_log_args(request)
    #
    try:
        # '_date' should be in format "yyyy-mm-dd"
        _date = datetime.strptime(dateSpecific, '%Y-%m-%d')
        #
        if option == str_calendar_events:
            data = {str_calendar_events: _icloud.get_events_date(_date)}
        elif option == str_calendar_birthdays:
            data = {str_calendar_birthdays: _icloud.get_birthdays_date(_date)}
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
