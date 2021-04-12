#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# VNDirect market data downloader
# https://github.com/nhuttrung/vndirect

import vndirect

START_DATE =        "2020-01-01"
END_DATE =          "2021-01-01"

# print("----- TEST 1 -------")
df = vndirect.get_ticker_data('FPT', START_DATE, END_DATE)
print(df)

# print("----- TEST 2 -------")
# ref_ticker = 'VNINDEX'
# ticker_list = ['PNJ', 'VNM']
# df = vndirect.get_tickers_data(ref_ticker, ticker_list, START_DATE, END_DATE)
# print(df)

# print("----- TEST 3 -------")
# interest_rate = 0.1   # 10%
# df = vndirect.add_cash(df, interest_rate)
# print(df)
