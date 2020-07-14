#!/usr/bin/env python
# coding: utf-8

# new nifty notify fetching data from the new nse website
# getting price change for nifty 50 and nifty bank
# for a specified interval and value

import os
import time
import requests
import datetime
from plyer import notification

# Notification timeout time in seconds
NOTIFICATION_TIMEOUT = 30


# function for showing notification given a symbol name and change
def _notify_now(symbol, change, duration=NOTIFICATION_TIMEOUT):
    title = f"{symbol} Alert!"
    message = f"{change} change is detected"
    icon = "python.ico"

    if not os.path.isfile(icon):
        icon = None

    notification.notify(
        title=title,
        message=message,
        app_icon=icon,
        timeout=duration
    )


# basic response headers
def _get_headers():
    request_headers = {
        'User-Agent': ('Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:78.0) '
                       + 'Gecko/20100101 Firefox/78.0'),
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.5'
    }
    return request_headers


# get json data
def _get_json_response(url):
    headers = _get_headers()
    headers['Content-type'] = 'application/json; charset=utf-8'
    response = requests.get(url, headers=headers)
    return response.json()


# get data from nse
def get_indices_info():
    url = 'https://www.nseindia.com/api/allIndices'
    json = _get_json_response(url)
    json = {i['indexSymbol']: dict(i) for i in json['data']}
    return json


# get start time
def _get_start_time():
    today, start_time = datetime.date.today(), datetime.time(9, 15)
    return datetime.datetime.combine(today, start_time)


# get end time
def _get_end_time():
    today, end_time = datetime.date.today(), datetime.time(15, 30)
    return datetime.datetime.combine(today, end_time)


# sleep time
def _check_for_sleep(check_time, start_time=_get_start_time(), end_time=_get_end_time()):
    sleep_time, current_time = 0, datetime.datetime.now()
    check_interval = datetime.timedelta(minutes=check_time)

    if current_time < start_time:
        sleep_time = (start_time - current_time).seconds

    elif current_time + check_interval > end_time:
        sleep_time = (end_time - current_time).seconds

    else:
        sleep_time = (check_time - current_time.minute % check_time) * 60
        sleep_time -= current_time.second

    return sleep_time


def _get_data():
    data = get_indices_info()
    return data['NIFTY 50']['last'], data['NIFTY BANK']['last']


def main():
    # Price change to be notified for
    print("Nifty 50 Change (Default is 25): ", end="")
    watch50 = int(input() or '25')

    print("Nifty Bank Change (Default is 100): ", end="")
    watch_bank = int(input() or '100')

    # Volume checking time in minutes
    print("Checking time(in minutes) (Default is 5): ", end="")
    check_time = int(input() or '5')

    current_time, end_time = datetime.datetime.now(), _get_end_time()

    if current_time.weekday() > 4 or current_time > end_time:
        print('\nMarket not active, get some rest!\n')
        return
    else:
        print(f'\nWelcome, printing {check_time}min changes..\n')

    first_fetch = True
    last50, last_bank = 0, 0

    if not (current_time.minute / check_time).is_integer():
        sleep_time = _check_for_sleep(check_time)
    else:
        sleep_time = 0

    while True:

        if first_fetch:
            print(f'Starting in {sleep_time // 60}m {sleep_time % 60}s.')

        time.sleep(sleep_time)
        current_time = datetime.datetime.now()

        # try getting data, exit if connection error
        try:
            # first fetch
            if first_fetch:
                last50, last_bank = _get_data()
                print(f'{current_time.strftime("%I:%M")}'
                      + f' --- First Fetch ----> Nifty50: {last50:.2f}'
                      + f' --- Nifty Bank: {last_bank:.2f}')
                first_fetch = False
                sleep_time = _check_for_sleep(check_time)
                continue

            # check changes
            now50, now_bank = _get_data()
            c50, c_bank = now50 - last50, now_bank - last_bank
            print(f"{current_time.strftime('%I:%M')}"
                  + f" --- Change Detected ----> Nifty50: {c50:.2f}"
                  + f" --- Nifty Bank: {c_bank:.2f}")

            # send notification if defined change detected
            if abs(c50) >= watch50:
                _notify_now('NIFTY 50', int(c50))
            if abs(c_bank) >= watch_bank:
                _notify_now('NIFTY BANK', int(c_bank))

            if current_time >= end_time:
                break

            # update last
            last50, last_bank = now50, now_bank

            sleep_time = _check_for_sleep(check_time)

        except:
            print(f"{current_time.strftime('%I:%M')}"
                  + " -----> Unable to fetch data!!"
                  + " --- Check if internet is working and run again.")
            return


if __name__ == '__main__':
    main()
