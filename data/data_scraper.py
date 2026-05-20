import os
import pandas as pd
from dotenv import load_dotenv
import time
from massive import RESTClient
from massive.exceptions import BadResponse

load_dotenv()
API_KEY = os.getenv("POLYGON_API_KEY")
client = RESTClient(API_KEY)

ticker_list = []
tickers = client.list_tickers(market="stocks", active=True, limit=1000)

while True:
    try:
        ticker = next(tickers)
        ticker_list.append(ticker)

        if len(ticker_list) % 1000 == 0:
            print(f"Fetched {len(ticker_list)} tickers so far...")
            time.sleep(13)
        
    except StopIteration:
        print("Finished fetching all tickers.")
        break
    

print(f"Total tickers fetched: {len(ticker_list)}")
print("First 10 tickers:")
for i, ticker in enumerate(ticker_list[:10]):
    print(f"{i+1}. {ticker}")