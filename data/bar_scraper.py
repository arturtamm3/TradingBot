import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
import time
from massive import RESTClient
from massive.exceptions import BadResponse
import sqlite3


def get_tickers(db_name, limit=10, offset=0):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    
    query = "SELECT id, symbol FROM tickers ORDER BY symbol ASC LIMIT ? OFFSET ?"
    cursor.execute(query, (limit, offset))
    tickers = cursor.fetchall()
    
    conn.close()
    return tickers


def add_bars_to_db(ticker_id, bars, db_name, table_name):
    cleaned_rows = []
    for bar in bars:
        row = (
            ticker_id,
            bar.timestamp,
            bar.open,
            bar.high,
            bar.low,
            bar.close,
            bar.volume
        )
        cleaned_rows.append(row)
    
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    query = f"""INSERT OR IGNORE INTO {table_name} (ticker_id, timestamp, open, high, low, close, volume) 
                VALUES (?, ?, ?, ?, ?, ?, ?)"""
    
    cursor.executemany(query, cleaned_rows)
    conn.commit()
    print(f"Inserted {len(cleaned_rows)} bars for ticker_id {ticker_id} into {table_name}.")
    conn.close()


def fetch_bars(ticker_id, ticker_symbol, db_name, client, table_name):
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=710)
  
    try:
        bars = client.list_aggs(
            ticker=ticker_symbol,
            multiplier=1,
            timespan="minute", 
            from_=start_date.strftime("%Y-%m-%d"),
            to=end_date.strftime("%Y-%m-%d"),
            limit=50000)

        bars_list = [bar for bar in bars]
        
        print(f"Fetched {len(bars_list)} bars for {ticker_symbol}")
        add_bars_to_db(ticker_id, bars_list, db_name, table_name)
    
    except BadResponse as e:
        print(f"Error fetching bars for {ticker_symbol}: {e}")




if __name__ == "__main__":
    load_dotenv()
    db_name = os.getenv("db_name")
    table_name = "stock_bars_1m"
    API_KEY = os.getenv("POLYGON_API_KEY")
    client = RESTClient(API_KEY)

    stocks = get_tickers(db_name, limit=1, offset=0)
    total_stocks = len(stocks)
    print(f"Starting to fetch bars for {total_stocks} stocks...")

    for index, (ticker_id, ticker_symbol) in enumerate(stocks, start=1):
        print(f"--- Processing {index}/{total_stocks}: {ticker_symbol} ---")
        fetch_bars(ticker_id, ticker_symbol, db_name, client, table_name)
        print(f"--- Finished Stock {index}/{total_stocks}: {ticker_symbol} ---\n")
        time.sleep(13)

