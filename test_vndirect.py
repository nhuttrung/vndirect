#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
# VNDirect market data downloader
# https://github.com/nhuttrung/vndirect

import vndirect

START_DATE =        "2011-01-01"
END_DATE =          "2021-01-01"

df = vndirect.download('FPT', START_DATE, END_DATE)
print(df)
