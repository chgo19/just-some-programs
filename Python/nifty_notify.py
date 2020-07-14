#!/usr/bin/env python
# coding: utf-8

# this ones for dad too, fetches from old nse website.
# This module is made to notify users using windows 10 if
# there is a specified jump in price in nifty50 or nifty_bank
# in a given amount of time by fetching data from nse

# pip install plyer nsetools
# download the python.ico file for a nice icon in notifications

import os
import datetime
import time

from nsetools import Nse
from plyer import notification

# Price change to be notified for
print("Nifty 50 Change (Default is 25): ", end="")
change_nifty50 = int(input() or '25')

print("Nifty Bank Change (Default is 100): ", end="")
change_nifty_bank = int(input() or '100')

# Volume checking time in minutes
print("Checking time(in minutes) (Default is 5): ", end="")
fetch_time = int(input() or '5')

# Notification timeout time in seconds
NOTIFICATION_TIMEOUT = 30


# function for showing notification given a symbol name
def notify_now(symbol, change, duration=NOTIFICATION_TIMEOUT):
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


current_time = datetime.datetime.now()

start_time = datetime.time(9, 15)
start_time = datetime.datetime.combine(current_time.date(), start_time)

end_time = datetime.time(15, 30)
end_time = datetime.datetime.combine(current_time.date(), end_time)

check_time = datetime.timedelta(minutes=fetch_time)


# don't run if weekend or time greater than
run = True
if current_time.weekday() > 4 or current_time > end_time:
    run = False
    print("\nMarket not active, get some rest!\n")
else:
    print(f"\nWelcome, printing {fetch_time}min changes..\n")


# initialize Nse class for fetching data
nse = Nse()


# fetching getting nse data
def get_data():
    get50 = nse.get_index_quote("nifty 50")
    get_bank = nse.get_index_quote("nifty bank")

    return get50['lastPrice'], get_bank['lastPrice']


# start only after start time and perfectly divisible time
if run and not (current_time.minute / fetch_time).is_integer():
    if current_time < start_time:
        sleep_time = (start_time - current_time).seconds
    else:
        sleep_time = ((fetch_time - current_time.minute % fetch_time) * 60
                      - current_time.second)

    print(f"First fetch to be done in: {sleep_time // 60}m {sleep_time % 60}s")
    time.sleep(sleep_time)

current_time = datetime.datetime.now()


last_nifty50 = -1
last_nifty_bank = -1


# first fetch
if run:
    try:
        last_nifty50, last_nifty_bank = get_data()

        print(f"{current_time.strftime('%I:%M')}"
              + f" --- First Fetch ----> Nifty50: {int(last_nifty50)}"
              + f" --- Nifty Bank: {int(last_nifty_bank)}")

    except ConnectionError:
        # on fetch fail, due to network probably
        print(f"{current_time.strftime('%I:%M')}"
              + "-----> Unable to fetch data!!"
              + " --- Check if internet is working and run again.")


while run and current_time < end_time:

    try:
        nifty50, nifty_bank = get_data()

        c1 = nifty50 - last_nifty50
        c2 = nifty_bank - last_nifty_bank

        print(f"{current_time.strftime('%I:%M')}"
              + f" --- Change ----> Nifty50: {c1:.2f} --- Nifty Bank: {c2:.2f}")

        if abs(c1) >= change_nifty50:
            notify_now("Nifty50", c1)

        if abs(c2) >= change_nifty_bank:
            notify_now("Nifty Bank", c2)

        last_nifty_bank, last_nifty50 = nifty_bank, nifty50

    except:
        # on network or any other error to fetch data
        print(f"{current_time.strftime('%I:%M')}"
              + "-----> Unable to fetch data!!"
              + " --- Check if internet is working.")

    if current_time + check_time > end_time:
        time.sleep((end_time - current_time).seconds)
    else:
        time.sleep((fetch_time - current_time.minute % fetch_time) * 60
                   - current_time.second)

    current_time = datetime.datetime.now()


# last fetch changes
if run:
    fifty, bank = get_data()
    print(f"{end_time.strftime('%I:%M')} --- Last Change "
          + f"----> Nifty50: {fifty - last_nifty50}"
          + f" --- Nifty Bank: {bank - last_nifty_bank}")
