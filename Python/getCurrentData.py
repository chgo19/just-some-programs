#!/usr/bin/env python
# coding: utf-8

# this module is made for getting the curent day volume info
# and structuring it with 5min and 15min interval
# which is then stored in a csv.
# gets the present nifty50 symbols and extracts for them
# use and modify at your will with no garantees whatsover.

# importing required libraries
import csv
import requests
import datetime
import pandas as pd
from io import StringIO
from dateutil.relativedelta import relativedelta


# define headers for web requests
request_headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:77.0) Gecko/20100101 Firefox/77.0',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.5'
    }


# setting date and time
current_date_time = datetime.datetime.now()
current_date = current_date_time.date()
current_time = current_date_time.time()
print(f"current_date: {current_date}\ncurrent_time: {current_time}")


#setting start and market end time, time gone and full duration
start_time = datetime.time(9, 15)
end_time = datetime.time(15, 30)
# today_start_time = datetime.datetime.combine(current_date, start_time)
# today_end_time = datetime.datetime.combine(current_date, end_time)
full_duration = datetime.datetime.combine(current_date, end_time) - datetime.datetime.combine(current_date, start_time)
time_gone = datetime.datetime.combine(current_date, current_time) - datetime.datetime.combine(current_date, start_time)
total_time = datetime.timedelta(hours=6, minutes=15, seconds=0)

# dates for fetching historical data
date_format = "%d-%m-%Y"
from_date = (current_date - relativedelta(months=6)).strftime(date_format)
to_date = (current_date).strftime(date_format)
print(f"from_date: {from_date}\nto_date: {to_date}")


# getting nifty fifty company symbols
nifty50_url = "https://www.nseindia.com/api/market-data-pre-open?key=NIFTY"
nifty50_response = requests.get(nifty50_url, headers=request_headers)
nifty50_json = nifty50_response.json()
nifty50_symbols = []
for symbol in nifty50_json['data']:
    nifty50_symbols.append(symbol['metadata']['symbol'])
print(f"nifty50: [{nifty50_symbols[0]}...{nifty50_symbols[-1]}]\ntotal: {len(nifty50_symbols)}")


#store trade info urls for all symbols
trade_info_urls = []
for stock_symbol in nifty50_symbols:
    if stock_symbol == 'M&M':
        stock_symbol = 'M%26M'
    trade_info_url = "https://www.nseindia.com/api/quote-equity?symbol=" + str(stock_symbol) + "&section=trade_info"
    trade_info_urls.append(trade_info_url)
print("Getting trade info responses, this might take a minute...")

# get trade info response
trade_info_responses, c = [], True
for n, i in enumerate(trade_info_urls):
    trade_info_response = requests.get(i, headers=request_headers)
    if trade_info_response.status_code != 200:
        c = False
    print(f"{n+1}. {nifty50_symbols[n]}: {trade_info_response}")
    trade_info_responses.append(trade_info_response)
if c:
    print("Got all trade info responses successfully!")
else:
    print("Some problems were encountered, check above for more.")


#prepare data(string) for csv file
print("Writing into csv file, this should be relatively fast!")
final_csv_file = "'Symbol', 'Current Day till now -> 15 min', 'Current Day till now -> 5 min'\n"
for n, response in enumerate(trade_info_responses):

    #adding symbol to csv
    final_csv_file += nifty50_symbols[n] + ", "

    # getting trade info json and its total_traded_volume
    trade_info_json = response.json()
    try:
        total_traded_volume = int(trade_info_json['marketDeptOrderBook']['tradeInfo']['totalTradedVolume'])
    except:
        total_traded_volume = 0

    #adding current day till now-> 15 min
    temp = datetime.timedelta(minutes=15)
    try:
        if start_time < current_time < end_time:
            temp = total_traded_volume/(time_gone/temp)
        else:
            temp = total_traded_volume/(full_duration/temp)
    except:
        temp = 0
    final_csv_file += f"{temp:.2f}" + ", "


    #adding current day till now-> 5 min
    temp = datetime.timedelta(minutes=5)
    try:
        if start_time < current_time < end_time:
            temp = total_traded_volume/(time_gone/temp)
        else:
            temp = total_traded_volume/(full_duration/temp)
    except:
        temp = 0
    final_csv_file += f"{temp:.2f}" + "\n"

    print(f"{n+1}. {nifty50_symbols[n]}: Done")


file_name = "Current-data-" + current_date_time.strftime("D%d-%m-%Y T%H-%M-%S") + ".csv"
with open(file_name, 'w') as f:
    f.write(final_csv_file)

print(f"{file_name} file written successfully!")