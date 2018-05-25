import threading
import os
from datetime import datetime, date

from bottle import HTTPError
from bottle import get, post
from bottle import request, run, HTTPResponse, static_file

from common_functions.query_to_string import convert_query_to_string
from config.config import get_cfg_port_listener
from config.config import get_cfg_serviceid, get_cfg_name_long, get_cfg_name_short, get_cfg_groups, get_cfg_subservices
from log.log import log_inbound, log_internal, log_outbound
from resources.global_resources.exposed_apis import *
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.global_resources.variables import *
from resources.lang.enGB.logs import *
from service.icloud import ICloud


def start_bottle(port_threads):

    ################################################################################################
    # Create device
    ################################################################################################

    _icloud = ICloud()

    log_internal(logPass, logDescDeviceObjectCreation, description='success')

    ################################################################################################
    # Enable cross domain scripting
    ################################################################################################

    def enable_cors(response):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET'
        response.headers['Access-Control-Allow-Headers'] = service_header_clientid_label
        return response

    ################################################################################################
    # Log arguments
    ################################################################################################

    def _get_log_args(request):
        #
        urlparts = request.urlparts
        #
        try:
            client_ip = request.headers['X-Forwarded-For']
        except:
            client_ip = request['REMOTE_ADDR']
        #
        try:
            server_ip = request.headers['X-Real-IP']
        except:
            server_ip = urlparts.hostname
        #
        try:
            client_user = request.headers[service_header_clientid_label]
        except:
            client_user = request['REMOTE_ADDR']
        #
        server_request_query = convert_query_to_string(request.query) if request.query_string else '-'
        server_request_body = request.body.read() if request.body.read()!='' else '-'
        #
        return {'client_ip': client_ip,
                'client_user': client_user,
                'server_ip': server_ip,
                'server_thread_port': urlparts.port,
                'server_method': request.method,
                'server_request_uri': urlparts.path,
                'server_request_query': server_request_query,
                'server_request_body': server_request_body}

    ################################################################################################
    # Service info & Groups
    ################################################################################################

    @get(uri_config)
    def get_config():
        #
        args = _get_log_args(request)
        #
        try:
            #
            data = {'service_id': get_cfg_serviceid(),
                    'name_long': get_cfg_name_long(),
                    'name_short': get_cfg_name_short(),
                    'subservices': get_cfg_subservices(),
                    'groups': get_cfg_groups()}
            #
            status = httpStatusSuccess
            #
            args['result'] = logPass
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            return HTTPResponse(body=data, status=status)
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

    ################################################################################################
    # 2FA - html interface
    ################################################################################################

    @get(uri_get_2fa_code_request_html)
    def get_2fa_html():
        #
        args = _get_log_args(request)
        #
        try:
            with open(os.path.join(os.path.dirname(__file__), 'service/2fa.html'), 'r') as f:
                page_body = f.read()
            #
            status = httpStatusSuccess
            args['result'] = logPass
            #
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
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
            log_inbound(**args)
            #
            raise HTTPError(status)

    @get(uri_get_2fa_code_request_js)
    def get_2fa_js():
        #
        args = _get_log_args(request)
        #
        try:
            #
            status = httpStatusSuccess
            args['result'] = logPass
            #
            args['http_response_code'] = status
            args['description'] = '-'
            log_inbound(**args)
            #
            response = static_file('2fa.js', root='service')
            response.status = status
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

    ################################################################################################
    # 2FA - request code
    ################################################################################################

    @post(uri_post_2fa_code_request)
    def post_code_request():
        #
        args = _get_log_args(request)
        #
        try:
            r = _icloud.request_validation_code_default()
            #
            if not bool(r):
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

    ################################################################################################
    # 2FA - validate code
    ################################################################################################

    @post(uri_post_2fa_code_validate)
    def post_code_validation():
        #
        args = _get_log_args(request)
        #
        try:
            #
            code = dict(request.json)
            code = code['2fa_code']
            #
            r = _icloud.validate_validation_code_default(code)
            #
            if not bool(r):
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

    ################################################################################################
    # Events
    ################################################################################################

    @get(uri_get_calendar_all)
    def get_events_all(option):
        #
        args = _get_log_args(request)
        #
        try:
            #
            if option == 'events':
                data = {'events': _icloud.get_events()}
            elif option == 'birthdays':
                data = {'birthdays': _icloud.get_birthdays()}
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

    @get(uri_get_calendar_today)
    def get_events_today(option):
        #
        args = _get_log_args(request)
        #
        try:
            #
            if option == 'events':
                data = {'events': _icloud.get_events_today()}
            elif option == 'birthdays':
                data = {'birthdays': _icloud.get_birthdays_today()}
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

    @get(uri_get_calendar_tomorrow)
    def get_events_tomorrow(option):
        #
        args = _get_log_args(request)
        #
        try:
            #
            if option == 'events':
                data = {'events': _icloud.get_events_tomorrow()}
            elif option == 'birthdays':
                data = {'birthdays': _icloud.get_birthdays_tomorrow()}
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

    @get(uri_get_calendar_date)
    def get_events_date(option, dateSpecific):
        #
        args = _get_log_args(request)
        #
        try:
            # '_date' should be in format "yyyy-mm-dd"
            _date = datetime.strptime(dateSpecific, '%Y-%m-%d')
            #
            if option == 'events':
                data = {'events': _icloud.get_events_date(_date)}
            elif option == 'birthdays':
                data = {'birthdays': _icloud.get_birthdays_date(_date)}
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

    @get(uri_get_calendar_range)
    def get_events_date(option, dateFrom, dateTo):
        #
        args = _get_log_args(request)
        #
        try:
            # '_dateFrom' and '_dateTo' should be in format "yyyy-mm-dd"
            _dateFrom = datetime.strptime(dateFrom, '%Y-%m-%d')
            _dateTo = datetime.strptime(dateTo, '%Y-%m-%d')
            #
            if option == 'events':
                data = {'events': _icloud.get_events_daterange(_dateFrom, _dateTo)}
            elif option == 'birthdays':
                data = {'birthdays': _icloud.get_birthdays_daterange(_dateFrom, _dateTo)}
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

    ################################################################################################

    def bottle_run(x_host, x_port):
        log_internal(logPass, logDescPortListener.format(port=x_port), description='started')
        run(host=x_host, port=x_port, debug=True)

    ################################################################################################

    host = 'localhost'
    ports = get_cfg_port_listener()
    for port in ports:
        t = threading.Thread(target=bottle_run, args=(host, port,))
        port_threads.append(t)

    # Start all threads
    for t in port_threads:
        t.start()
    # Use .join() for all threads to keep main process 'alive'
    for t in port_threads:
        t.join()
