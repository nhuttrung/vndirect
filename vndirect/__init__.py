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

from urllib.request import urlopen
import pandas as pd
import numpy as np
import json
from datetime import datetime, timezone

__version__ = "0.1.0"
__author__ = "Trung N. Tran"

def download(symbol, start_date, end_date):
    """ 
    Donload market data from VNDirect
    """

    def toEpoch(date):
        return int((date - datetime(1970, 1, 1)).total_seconds())

    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    epochStart = toEpoch(start_date)
    epochEnd = toEpoch(end_date)

    """ 
    VNDirect limits 1000 records per request. 
    So we split into multiple requests and append the results
    """
    fetch_period = 3600*24*365 * 3    # 3 years
    URL_TEMPLATE = "https://dchart-api.vndirect.com.vn/dchart/history?resolution=1D&from={}&to={}&symbol={}"
    df = pd.DataFrame()
    for start in np.arange(epochStart, epochEnd, fetch_period):
        end = min(start + fetch_period, epochEnd)
        url = URL_TEMPLATE.format(start, end, symbol)
        print('Download URL', url)
        response = urlopen(url)
        prices = json.loads(response.read())
        dates = prices["t"]
        for idx, timestamp in enumerate(dates):
            dates[idx] = datetime.fromtimestamp(timestamp, timezone.utc)
        data = {
            'Date': dates,
            'Open': prices["o"],
            'High': prices["h"],
            'Low': prices["l"],
            'Close': prices["c"],
            'Adj Close': prices["c"],
            'Volume': prices["v"]
        }
        df_temp = pd.DataFrame(data)
        df = df.append(df_temp, ignore_index=True)

    df.set_index('Date', inplace=True)
    df.index = pd.to_datetime(df.index)
    df.index.name = "Date"
    df.drop_duplicates(inplace=True)

    return df


__all__ = ['download']
