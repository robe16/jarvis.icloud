from datetime import datetime, date, timedelta
import cache


def get_birthdays_today():
    return _get_birthdays(date.today(), date.today())


def get_birthdays_tomorrow():
    return _get_birthdays(date.today() + timedelta(days=1),
                          date.today() + timedelta(days=1))


def get_birthdays_date(_date):
    return _get_birthdays(_date, _date)


def get_birthdays_daterange(dateFrom, dateTo):
    return _get_birthdays(dateFrom, dateTo)


def _get_birthdays(from_dt, to_dt):
    #
    new_bdays = []
    #
    from_d = from_dt.day
    from_m = from_dt.month
    to_d = to_dt.day
    to_m = to_dt.month
    #
    birthdays = cache.cache['birthdays']
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