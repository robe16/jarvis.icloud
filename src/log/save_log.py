from datetime import datetime
import os

from config.config import get_cfg_serviceid
from resources.global_resources.variables import serviceType


logFileNameDateFormat = '%Y-%m-%d'


def save_log_item(item):
    #
    log_msg = ''
    #
    for k in item:
        if not log_msg == '':
            log_msg += ', '
        log_msg += '{key}={value}'.format(key=k, value=item[k])
    #
    _add_log_entry(log_msg)


def _add_log_entry(log_msg):
    try:
        file_name = _get_log_filename()
        with open(os.path.join(os.path.dirname(__file__), 'logfiles', file_name), 'a') as output_file:
            output_file.write(log_msg + '\n')
            output_file.close()
    except Exception as e:
        pass


def _get_log_filename():
    return '{filename}.{date}.log'.format(filename=get_cfg_serviceid(),
                                          date=datetime.now().strftime(logFileNameDateFormat))
