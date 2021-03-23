# vndirect
VNDirect market data downloader

## Installation
pip install git+https://github.com/nhuttrung/vndirect.git

## Usage
```python
import vndirect

START_DATE =        "2000-01-01"
END_DATE =          "2021-01-01"

print("----- TEST 1 -------")
df = vndirect.download('FPT', START_DATE, END_DATE)
print(df)

print("----- TEST 2 -------")
ref_ticker = 'VNINDEX'
ticker_list = ['PNJ', 'VNM']
df = vndirect.get_tickers_data(ref_ticker, ticker_list, START_DATE, END_DATE)
print(df)
```
