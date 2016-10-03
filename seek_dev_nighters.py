import requests
from pytz import timezone
from datetime import datetime

from functools import reduce

API_URL = 'http://devman.org/api/challenges/solution_attempts/'

EARLY_TIME = datetime.strptime('06:00:00', '%H:%M:%S').time()
LATE_TIME = datetime.strptime('00:00:00', '%H:%M:%S').time()


def get_respose(page):
    r = requests.get(API_URL, params={'page': page})
    if r.status_code == 200:
        return r.json()['records']


def load_attempts():
    r = requests.get(API_URL)
    if r.status_code == 200:
        page_count = r.json()['number_of_pages']
        for page in range(page_count):
            yield get_respose(page + 1)


def is_midighter(user):
    server_time = datetime.utcfromtimestamp(user['timestamp'])
    client_time = timezone(user['timezone']).fromutc(server_time)
    return(EARLY_TIME > client_time.time() > LATE_TIME)


def get_midnighters():
    midnighters = reduce(
        lambda res, x: res + list(filter(is_midighter, x)),
        load_attempts(),
        []
    )
    unique_midnighters = set(map(lambda a: a['username'], midnighters))
    return unique_midnighters


def output_midnighters(midnighters):
    for midnighter in midnighters:
        print(midnighter)

if __name__ == '__main__':
    output_midnighters(get_midnighters())
