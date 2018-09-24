import threading
import cache
from service.icloud import ICloud
from service.icloud_update_events import eventUpdater_service
from service.icloud_update_birthdays import birthdayUpdater_service


def start_service():
    #
    cache.cache['_icloud'] = ICloud()
    cache.cache['calendar'] = {}
    #
    thread_event = threading.Thread(target=eventUpdater_service)
    thread_event.start()
    #
    thread_birthday = threading.Thread(target=birthdayUpdater_service)
    thread_birthday.start()