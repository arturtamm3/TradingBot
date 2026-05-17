import sqlite3
from dotenv import load_dotenv
import os

load_dotenv()

def check_database():
    db_name = os.getenv("db_name")
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    print("Tables in the database:")
    for t in tables:
        print(f"Table name - {t[0]}")
        check_table(cursor, t[0])
    
    conn.close()

def check_table(cursor, table_name):
    cursor.execute(f"PRAGMA table_info({table_name});")
    columns = cursor.fetchall()
    print(f"Columns in {table_name}:")
    for col in columns:
        print(f"Column name - {col[1]}, Type - {col[2]}")
       
    
if __name__ == "__main__":
    check_database()