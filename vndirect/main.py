#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# VNDirect market data downloader
# https://github.com/nhuttrung/vndirect
#
# Copyright 2021-2021 Trung N. Tran
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import os
from os import path
from datetime import datetime, timezone
from urllib.request import urlopen
import json
import pandas as pd
import numpy as np

def set_datasets_dir(datasets_dir):
    global DATASETS_DIR
    DATASETS_DIR = datasets_dir

def get_ticker_data(ticker, start_date, end_date):
    global DATASETS_DIR
    if "DATASETS_DIR" not in globals():
        set_datasets_dir("datasets")

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)

    if not os.path.exists(DATASETS_DIR):
        os.makedirs(DATASETS_DIR) 
    dataFile = DATASETS_DIR + "/{}.csv".format(ticker)
    end_date_epoch = _toEpoch(end_date)
    forceDownload = False

    if not path.exists(dataFile):
        forceDownload = True
    else:
        modified_time = path.getmtime(dataFile)
        if (modified_time < end_date_epoch):
            forceDownload = True

    if forceDownload:
        df = download(ticker, start_date, end_date)
        df.to_csv(dataFile, index=False)
        os.utime(dataFile, (end_date_epoch, end_date_epoch))
    else:
        df = pd.read_csv(dataFile)
    
    df['Date'] = pd.to_datetime(df['Date'])
    df.set_index('Date', inplace=True)
    df.index.name = 'Date'
    return df

def get_tickers_data(ref_ticker, ticker_list, start_date, end_date) -> pd.DataFrame:
    """Fetches data from VNDirect
    Parameters
    ----------
    ref_ticker : str
        Reference ticker used for filling missing data
    ticker_list : list
        a list of stock tickers
    start_date : str
        start date of the data
    end_date : str
        end date of the data


    Returns
    -------
    `pd.DataFrame`
        7 columns: A date, open, high, low, close, volume and tick symbol
        for the specified stock ticker
    """

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    data_df = pd.DataFrame()

    # Reference dataframe which contains all trading dates
    ref_df = get_ticker_data(ref_ticker, start_date, end_date)
    ref_df.drop(columns=['Open', 'High', 'Low', 'Close', 'Volume'], inplace=True)
    # print("----- REF -------")
    # print(ref_df)

    for ticker in ticker_list:
        temp_df = get_ticker_data(ticker, start_date, end_date)
        temp_df['Ticker'] = ticker
        # print("----- TEMP -------")
        # print(temp_df)

        temp_df = ref_df.join(temp_df)
        temp_df.fillna(method="ffill", inplace=True)
        temp_df.fillna(method="bfill", inplace=True)
        data_df = data_df.append(temp_df)

    # reset the index, we want to use numbers as index instead of dates
    data_df = data_df.reset_index()
    # create day of the week column (monday = 0)
    data_df['Date'] = pd.to_datetime(data_df['Date'])
    data_df["day"] = data_df['Date'].dt.dayofweek

    data_df = data_df.sort_values(by=['Date', 'Ticker']).reset_index(drop=True)

    return data_df



def _toEpoch(date):
    return int((date - datetime(1970, 1, 1)).total_seconds())

def download(symbol, start, end):
    # print('Fetch prices for ' + symbol)
    start = pd.to_datetime(start)
    end = pd.to_datetime(end)
    epochStart = _toEpoch(start)+1
    epochEnd = _toEpoch(end)

    """ 
    VNDirect limits 1000 records per request. So we fetch multiple times and append the results
    """
    period = 3600*24*365 * 3
    URL_TEMPLATE = "https://dchart-api.vndirect.com.vn/dchart/history?resolution=1D&from={}&to={}&symbol={}"
    df = pd.DataFrame()
    for start in np.arange(epochStart, epochEnd, period):
        end = min(start+period, epochEnd)
        url = URL_TEMPLATE.format(start, end, symbol)
        print('Download URL', url)
        response = urlopen(url)
        prices = json.loads(response.read())
        dates = prices["t"]
        for idx, timestamp in enumerate(dates):
            dates[idx] = datetime.fromtimestamp(timestamp, timezone.utc).strftime("%Y-%m-%d")
        data = {
            'Date': dates,
            'Open': prices["o"],
            'High': prices["h"],
            'Low': prices["l"],
            'Close': prices["c"],
            'Volume': prices["v"]
        }
        df_temp = pd.DataFrame(data)
        df = df.append(df_temp, ignore_index=True)

    df.set_index('Date', inplace=True)
    df.drop_duplicates(inplace=True)
    df.reset_index(inplace=True)
    return df

def add_cash(df, interest_rate) -> pd.DataFrame:
    """ 
    Think of 'CASH' is stock with price increased every by the interest_rate
    """

    # Remove all columns except 'Date' and 'day'
    cash_df = df.filter(['Date', 'day'])
    cash_df.drop_duplicates(inplace=True)

    price = 50
    interest = price * interest_rate/365
    dates = []
    prices = []
    volume = []
    tickers = ["CASH" for x in range(cash_df.shape[0])]
    days = []
    for i in range(0, cash_df.shape[0]):
        dates.append(cash_df.iloc[i]['Date'])
        prices.append(price)
        volume.append(1)
        days.append(cash_df.iloc[i]['day'])
        # price = price + price * interest_rate/365
        price += interest
        
    data = {
      'Date': dates,
      'Open': prices,
      'High': prices,
      'Low': prices,
      'Close': prices,
      'Volume': volume,
      'Ticker': tickers,
      'day': days
    }
    cash_df = pd.DataFrame(data)

    df = df.append(cash_df)
    df = df.sort_values(by=['Date', 'Ticker']).reset_index(drop=True)
    return df
