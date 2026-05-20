import os
from dotenv import load_dotenv
import time
from massive import RESTClient
from massive.exceptions import BadResponse
import sqlite3

def fetch_tickers(tickers):
    ticker_list = []
    while True:
        try:
            ticker = next(tickers)
            ticker_list.append(ticker)

            if len(ticker_list) % 1000 == 0:
                print(f"Fetched {len(ticker_list)} tickers so far...")
                time.sleep(13)
        
        except StopIteration:
            print("Finished fetching all tickers.")
            return ticker_list

def add_ticker_to_db(ticker_list, db_name):
    clean_list = []
    for ticker in ticker_list:
        row = (ticker.ticker, getattr(ticker, "primary_exchange", ""), getattr(ticker, "currency_name", "USD"))
        clean_list.append(row)
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    query = "INSERT OR IGNORE INTO tickers (symbol, exchange, currency) VALUES (?, ?, ?)"
    cursor.executemany(query, clean_list)
    
    conn.commit()

    cursor.execute("SELECT COUNT(*) FROM tickers")
    count = cursor.fetchone()[0]
    
    print(f"Total tickers in database: {count}")
    conn.close()

if __name__ == "__main__":
    load_dotenv()
    db_name = os.getenv("db_name")
    API_KEY = os.getenv("POLYGON_API_KEY")
    client = RESTClient(API_KEY)

    tickers = client.list_tickers(market="stocks", active=True, type="CS", limit=1000)

    ticker_list = fetch_tickers(tickers)

    add_ticker_to_db(ticker_list, db_name)
    print("Ticker data has been added to the database.")
