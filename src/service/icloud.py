from pyicloud import PyiCloudService
from datetime import datetime, date, timedelta
from time import time

from config.config import get_cfg_details_account_username, get_cfg_details_account_password
from config.config import get_cfg_details_2fa_deviceType, get_cfg_details_2fa_phoneNumber
from config.config import get_cfg_details_calendar_name, get_cfg_details_calendar_colour
from log.log import log_outbound, log_internal
from resources.global_resources.log_vars import logPass, logFail, logException
from resources.lang.enGB.logs import *


class ICloud():

    def __init__(self):
        #
        self._icloud = PyiCloudService(get_cfg_details_account_username(),
                                       get_cfg_details_account_password())

    # 2SA/2FA

    def check2sa(self):
        # no function 'requires_2sa available yet from PyiCloudService,
        # therefore default to False and update when available
        return {'2fa': False}
        # r = self._icloud.requires_2sa
        # if r:
        #     return {'2fs': True}
        # else:
        #     return {'2sa': False}

    def check2fa(self):
        r = self._icloud.requires_2fa
        if r:
            return {'2fa': True}
        else:
            return {'2fa': False}

    def get_2fa_trusted_devices(self):
        if self._icloud.requires_2fa:
            devices = self._icloud.trusted_devices
            return {'2fa': True,
                    'devices': devices}
        else:
            return {'2fa': False,
                    'devices': []}

    def _get_2fa_trusted_device_default(self):
        devices = self.get_2fa_trusted_devices()
        if devices['2fa']:
            for d in devices['devices']:
                default_deviceType = get_cfg_details_2fa_deviceType()
                if d['deviceType'] == default_deviceType:
                    if default_deviceType == 'SMS':
                        return {'device': d}
            # if no default device found in list
            return {'device': False,
                    'error': 'Jarvis does not hold a default devices that matches those returned by iCloud.'}
        return {'device': False,
                'error': 'iCloud has reported back that 2FA is not required for access to services.'}

    # note that 'device' must be in the correct dict structure
    def request_validation_code(self, device):
        if self._icloud.send_verification_code(device):
            return True
        else:
            return False

    def request_validation_code_default(self):
        #
        device = self._get_2fa_trusted_device_default()
        #
        if device['device']:
            return {'result': self.request_validation_code(device['device'])}
        else:
            return {'result': False,
                    'error': device['error']}

    # note that 'device' must be in the correct dict structure
    def validate_validation_code(self, device, code):
        if self._icloud.validate_verification_code(device, code):
            return True
        else:
            return False

    def validate_validation_code_default(self, code):
        #
        device = self._get_2fa_trusted_device_default()
        #
        if device:
            return self.validate_validation_code(device, code)
        else:
            return False

    # Devices

    def get_devices(self):
        devices = self._icloud.devices
        return devices

    def get_iphone(self):
        devices = self._icloud.iphone
        return devices

    # Contacts

    def get_contacts(self):
        return self._icloud.contacts.all()

    # Calendar - events

    def get_events(self):
        return self._convert_icloud_events(self._icloud.calendar.events())

    def get_events_today(self):
        return self._get_events(date.today(), date.today())

    def get_events_tomorrow(self):
        return self._get_events(date.today() + timedelta(days=1),
                                date.today() + timedelta(days=1))

    def get_events_date(self, _date):
        return self._get_events(_date, _date)

    def get_events_daterange(self, dateFrom, dateTo):
        return self._get_events(dateFrom, dateTo)

    def _get_events(self, from_dt, to_dt):
        _events = self._icloud.calendar.events(from_dt, to_dt)
        _events = self._convert_icloud_events(_events)
        return _events

    # Calendar - birthdays

    def get_birthdays(self):
        contacts = self.get_contacts()
        birthdays = []
        for contact in contacts:
            if 'birthday' in contact.keys():
                #
                b = {'birthday': contact['birthday']}
                #
                if 'firstName' in contact.keys():
                    b['firstName'] = contact['firstName']
                #
                if 'lastName' in contact.keys():
                    b['lastName'] = contact['lastName']
                #
                birthdays.append(b)
        return birthdays

    def get_birthdays_today(self):
        return self._get_birthdays(date.today(), date.today())

    def get_birthdays_tomorrow(self):
        return self._get_birthdays(date.today() + timedelta(days=1),
                                date.today() + timedelta(days=1))

    def get_birthdays_date(self, _date):
        return self._get_birthdays(_date, _date)

    def get_birthdays_daterange(self, dateFrom, dateTo):
        return self._get_birthdays(dateFrom, dateTo)

    def _get_birthdays(self, from_dt, to_dt):
        #
        new_bdays = []
        #
        from_d = from_dt.day
        from_m = from_dt.month
        to_d = to_dt.day
        to_m = to_dt.month
        #
        birthdays = self.get_birthdays()
        for b in birthdays:
            bday_d = datetime.strptime(b['birthday'], '%Y-%m-%d').day
            bday_m = datetime.strptime(b['birthday'], '%Y-%m-%d').month
            #
            if from_m < to_m:
                if (bday_m == from_m and bday_d >= from_d) or \
                        (bday_m == to_m and bday_d <= to_d) or \
                        (from_m <= bday_m <= to_m and from_d <= bday_d <= to_d):
                    new_bdays.append(b)
            elif from_m > to_m:
                if (bday_m == from_m and bday_d <= from_d) or \
                        (bday_m == to_m and bday_d >= to_d) or \
                        (to_m <= bday_m <= from_m and from_d <= bday_d <= to_d):
                    new_bdays.append(b)
            else:
                if from_m == bday_m and from_d <= bday_d <= to_d:
                    new_bdays.append(b)
        #
        return new_bdays

    @staticmethod
    def _get_calendar_details(_event):
        #
        calendar_name = get_cfg_details_calendar_name(_event['pGuid'])
        if not calendar_name:
            calendar_name = ''
        #
        calendar_colour = get_cfg_details_calendar_colour(_event['pGuid'])
        if not calendar_colour:
            calendar_colour = 'none'
        #
        return {'name': calendar_name,
                'colour': calendar_colour}

    # guid = event id that is used in same event even across invitees
    # pGuid = calendar id unique to specific calendar and user

    def _convert_icloud_events(self, _events):
        #
        usedGuids = []
        tempGuids = {}
        for event in _events:
            if event['guid'] in tempGuids.keys():
                tempGuids[event['guid']].append(self._get_calendar_details(event))
            else:
                tempGuids[event['guid']] = [self._get_calendar_details(event)]
        #
        new_events = []
        for event in _events:
            if not event['guid'] in usedGuids:
                # put event in structure for json
                new_e = self._convert_icloud_event(event)
                # find all calendars for this event and add to new_e
                if event['guid'] in tempGuids.keys():
                    new_e['calendars'] = tempGuids[event['guid']]
                #
                new_events.append(new_e)
                usedGuids.append(event['guid'])
        #
        return new_events

    def _convert_icloud_event(self, _event):
        #
        return {'title': _event['title'],
                'location': _event['location'],
                'start': self._convert_datetime_to_string(self._convert_icloud_to_datetime(_event['localStartDate'])),
                'end': self._convert_datetime_to_string(self._convert_icloud_to_datetime(_event['localEndDate'])),
                'duration': _event['duration'],
                'allDay': _event['allDay'],
                'calendars': []
                }

    # Following function will get events for the next 52 weeks and identify all unique calendars
    def get_icloud_calendars(self):
        events = self._icloud.calendar.events(date.today(), date.today() + timedelta(weeks=52))
        tempGuids = {}
        for event in events:
            if not event['pGuid'] in tempGuids.keys():
                tempGuids[event['pGuid']] = self._get_calendar_details(event)
        return tempGuids


    @staticmethod
    def _convert_icloud_to_datetime(_icloud_datetime):
        # datetime(year, month, day, hour=0, minute=0, second=0, microsecond=0)
        return datetime(_icloud_datetime[1], _icloud_datetime[2], _icloud_datetime[3],
                        _icloud_datetime[4], _icloud_datetime[5])

    @staticmethod
    def _convert_datetime_to_string(_datetime):
        return _datetime.strftime('%Y-%m-%d %H-%M')
