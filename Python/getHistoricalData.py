#!/usr/bin/env python
# coding: utf-8

# This python module is for getting historical data from the
# nse api and storing its volume info into a csv
# this could be extended for further features and more data organization
# but i don't plan to do so in any forseeable future
# i maily made this because my dad asked me to and
# i myself don't do trading
# this gets the historical data for the current nifty 50 symbols
# which themselves are extracted when this script is executed.
# use and modify at your will with no warranty whatsover.

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


# store historical data urls for all symbols
historical_data_urls = []
for stock_symbol in nifty50_symbols:
    if stock_symbol == 'M&M':
        stock_symbol = 'M%26M'
    historical_data_url = "https://www.nseindia.com/api/historical/cm/equity?symbol=" + str(stock_symbol) +     "&series=[%22EQ%22,%22EQ%22]&from="+ str(from_date) +"&to=" + str(to_date) + "&csv=true"
    historical_data_urls.append(historical_data_url)
print("Getting Historical data responses, this may take some time...")


# get historical data response
request_headers['content-type'] = 'text/csv'
historical_data_responses, c = [], True
for n, i in enumerate(historical_data_urls):
    historical_data_response = requests.get(i, headers=request_headers)
    historical_data_response.encoding = 'utf-8'
    if historical_data_response.status_code != 200:
        c = False
    print(f"{n+1}. {nifty50_symbols[n]}: {historical_data_response}")
    historical_data_responses.append(historical_data_response)
if c:
    print("Got all historical data responses successfully!")
else:
    print("There was some error check above log to know which one.")


#prepare data(string) for csv file
print("Writing responses to csv, this should be fast!")
final_csv_file = "'Symbol', '6 months -> 1 month', 'last 5 days/1 week -> 1 day', 'Last Day -> 15 min', 'last Day -> 5 min'\n"
for n, response in enumerate(historical_data_responses):

    #adding symbol to csv
    final_csv_file += nifty50_symbols[n] + ", "


    #getting data in pandas dataframe
    data = pd.read_csv(StringIO(response.text))
    #getting colume column as pandas series
    try:
        volume = data['VOLUME ']
    except:
        volume = [0]

    #adding 6 months -> 1 month
    try:
        temp = sum(volume)/6
    except ZeroDivisionError:
        temp = 0
    final_csv_file += f"{temp:.2f}" + ", "


    #adding last 5 days/1 week -> 1 day
    try:
        temp = sum(volume[:5])/5
    except:
        temp = 0
    final_csv_file += f"{temp:.2f}" + ", "


    #adding last day -> 15 min
    temp = datetime.timedelta(minutes=15)
    try:
        temp = volume[0]/(total_time/temp)
    except:
        temp = 0
    final_csv_file += f"{temp:.2f}" + ", "


    #adding last day -> 5 min
    temp = datetime.timedelta(minutes=5)
    try:
        temp = volume[0]/(total_time/temp)
    except:
        temp = 0
    final_csv_file += f"{temp:.2f}" + "\n"

    print(f"{n+1}. {nifty50_symbols[n]}: Done")


file_name = "Historical-Data-" + current_date_time.strftime("%d-%m-%Y") + ".csv"
with open(file_name, 'w') as f:
    f.write(final_csv_file)

print(f"{file_name} file written successfully!")