import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

def create_database(db_name, stock_bars):
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()

    cursor.execute("PRAGMA foreign_keys = ON;")

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tickers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL UNIQUE,
            exchange TEXT,
            currency TEXT
        )
    ''')

    create_stock_bars_table(cursor, stock_bars)

    conn.commit()
    conn.close()

def create_stock_bars_table(cursor, stock_bars):
    cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS {stock_bars} (
            ticker_id INTEGER,
            timestamp INTEGER NOT NULL,
            open REAL NOT NULL,
            high REAL NOT NULL,
            low REAL NOT NULL,
            close REAL NOT NULL,
            volume INTEGER NOT NULL,
            PRIMARY KEY (ticker_id, timestamp),
            FOREIGN KEY (ticker_id) REFERENCES tickers(id) ON DELETE CASCADE
        )
    ''')
    cursor.execute(f"CREATE INDEX IF NOT EXISTS idx_{stock_bars}_ticker_id ON {stock_bars}(ticker_id, timestamp);")


if __name__ == "__main__":
    db_name = os.getenv("db_name")
    stock_bars = "stock_bars_1m"
    create_database(db_name, stock_bars)
