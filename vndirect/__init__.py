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

__version__ = "0.2.0"
__author__ = "Trung N. Tran"

from .main import get_tickers_data, get_ticker_data, download

__all__ = ['get_tickers_data', 'get_ticker_data', 'download']
