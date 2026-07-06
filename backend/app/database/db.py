import sqlite3

DATABASE = 'database/smartshopper.db'

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS price_entries (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_name TEXT NOT NULL,
        product_name TEXT NOT NULL,
        price REAL NOT NULL,
        last_updated TEXT NOT NULL
        );
    """)

    conn.commit()
    conn.close()