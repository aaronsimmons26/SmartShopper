import os
import sqlite3

# Build the path from this file's folder so it works no matter where Python is run from
DATABASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'smartshopper.db')

def get_connection():
    conn = sqlite3.connect(DATABASE)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS stores (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL
        );
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS prices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        store_id INTEGER NOT NULL,
        product_id INTEGER NOT NULL,        
        price REAL NOT NULL,
        last_updated TEXT NOT NULL,
        
        FOREIGN KEY(store_id) REFERENCES stores(id),
        FOREIGN KEY(product_id) REFERENCES products(id)
        );
    """)

    conn.commit()
    conn.close()