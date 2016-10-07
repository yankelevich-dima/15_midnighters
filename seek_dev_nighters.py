import requests
from pytz import timezone
from datetime import datetime


API_URL = 'http://devman.org/api/challenges/solution_attempts/'

EARLY_TIME = datetime.strptime('06:00:00', '%H:%M:%S').time()
LATE_TIME = datetime.strptime('00:00:00', '%H:%M:%S').time()


def load_attempts():
    r = requests.get(API_URL)
    if r.status_code == requests.codes.ok:
        page_count = r.json()['number_of_pages']
        for page in range(page_count):
            r = requests.get(API_URL, params={'page': page + 1})
            if r.status_code == requests.codes.ok:
                for user in r.json()['records']:
                    yield user


def is_midighter(user):
    if user['timestamp'] is None:
        return False
    server_time = datetime.utcfromtimestamp(user['timestamp'])
    client_time = timezone(user['timezone']).fromutc(server_time)
    return (EARLY_TIME > client_time.time() > LATE_TIME)


def get_midnighters():
    midnighters = [x['username'] for x in load_attempts() if is_midighter(x)]
    return set(midnighters)


def output_midnighters(midnighters):
    for midnighter in midnighters:
        print(midnighter)

if __name__ == '__main__':
    output_midnighters(get_midnighters())
