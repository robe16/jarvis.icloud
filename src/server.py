from bottle import request, run, route, get, post
import datetime

import cache
from config.config import get_cfg_port
from common_functions.request_enable_cors import enable_cors, response_options
from resources.global_resources.log_vars import logPass
from resources.lang.enGB.logs import *

from apis.get_config import get_config
from apis.get_2fa_html import get_2fa_html
from apis.get_2fa_js import get_2fa_js
from apis.post_2fa_code_request import post_2fa_code_request
from apis.post_2fa_code_validate import post_2fa_code_validate
from apis.get_calendar_all import get_calendar_all
from apis.get_calendar_today import get_calendar_today
from apis.get_calendar_tomorrow import get_calendar_tomorrow
from apis.get_calendar_date import get_calendar_date
from apis.get_calendar_daterange import get_calendar_daterange


def start_server():

    ################################################################################################
    # APIs
    ################################################################################################

    @route('/config', method=['OPTIONS'])
    @route('/icloud/<option>/all', method=['OPTIONS'])
    @route('/icloud/<option>/today', method=['OPTIONS'])
    @route('/icloud/<option>/tomorrow', method=['OPTIONS'])
    @route('/icloud/<option>/date/<dateSpecific>', method=['OPTIONS'])
    @route('/icloud/<option>/daterange/datefrom/<dateFrom>/dateto/<dateTo>', method=['OPTIONS'])
    def api_cors_options(**kwargs):
        return response_options()

    @get('/config')
    def api_get_config():
        response = get_config(request)
        return enable_cors(response)

    @get('/icloud/authentication/2fa/2fa.html')
    def api_get_2fa_html():
        return get_2fa_html(request)

    @get('/icloud/authentication/2fa/2fa.js')
    def api_get_2fa_js():
        return get_2fa_js(request)

    @post('/icloud/authentication/2fa/code/request')
    def api_post_2fa_code_request():
        return post_2fa_code_request(request)

    @post('/icloud/authentication/2fa/code/validate')
    def api_post_2fa_code_validate():
        return post_2fa_code_validate(request)

    @get('/icloud/<option>/all')
    def api_get_calendar_all(option):
        response = get_calendar_all(request, option)
        return enable_cors(response)

    @get('/icloud/<option>/today')
    def api_get_calendar_today(option):
        response = get_calendar_today(request, option)
        return enable_cors(response)

    @get('/icloud/<option>/tomorrow')
    def api_get_calendar_tomorrow(option):
        response = get_calendar_tomorrow(request, option)
        return enable_cors(response)

    @get('/icloud/<option>/date/<dateSpecific>')
    def api_get_calendar_date(option, dateSpecific):
        response = get_calendar_date(request, option, dateSpecific)
        return enable_cors(response)

    @get('/icloud/<option>/daterange/datefrom/<dateFrom>/dateto/<dateTo>')
    def api_get_calendar_daterange(option, dateFrom, dateTo):
        response = get_calendar_daterange(request, option, dateFrom, dateTo)
        return enable_cors(response)


    ################################################################################################
    # TODO - further API URIs
    ################################################################################################
    uri_get_devices = '/icloud/devices'
    uri_get_device_location = '/icloud/device/<deviceid>/location'
    uri_get_device_status = '/icloud/device/<deviceid>/status'
    uri_post_device_playsound = '/icloud/device/<deviceid>/playsound'
    uri_post_device_lostmode = '/icloud/device/<deviceid>/lostmode'
    uri_get_contacts = '/icloud/contacts'
    uri_get_files = '/icloud/files'
    uri_get_photos = '/icloud/photos'

    ################################################################################################

    host = '0.0.0.0'
    port = get_cfg_port()
    run(host=host, port=port, server='paste', debug=True)

    cache.logQ.put({'timestamp': datetime.now(),
                    'process': 'internal', 'result': logPass,
                    'operation': logDescPortListener.format(port=port), 'description': 'started'})

    ################################################################################################
