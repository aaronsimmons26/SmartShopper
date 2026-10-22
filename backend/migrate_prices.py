import os
import sys
from app.database.db import get_connection, DATABASE

# One-time migration: converts the old prices table (store_name, product_name)
# into the normalized schema (store_id, product_id) used by app/services/prices.py.
#
# Safety rules:
# - The backup must exist before anything changes.
# - Everything runs in one transaction; any failed check rolls it all back.
# - The old table is kept as prices_old instead of being deleted.
# - Running the script again does nothing once the migration has finished.

BACKUP = os.path.join(os.path.dirname(DATABASE), 'smartshopper_backup.db')

if not os.path.exists(BACKUP):
    sys.exit(f"Backup not found at {BACKUP}. Create it before migrating.")

conn = get_connection()
cursor = conn.cursor()

# Stop if the migration already ran (prices already has a store_id column)
cursor.execute("PRAGMA table_info(prices)")
price_columns = [column["name"] for column in cursor.fetchall()]

if "store_id" in price_columns:
    conn.close()
    sys.exit("prices table already uses store_id. Migration already done, nothing to do.")

conn.execute("BEGIN")

try:
    cursor.execute("SELECT * FROM prices")
    old_prices = cursor.fetchall()

    print("Records found:", len(old_prices))

    cursor.execute("SELECT DISTINCT store_name FROM prices")
    old_stores = cursor.fetchall()

    print('Unique stores found:', len(old_stores))

    for store in old_stores:
        cursor.execute(
            "INSERT INTO stores (name) VALUES (?)",
            (store["store_name"],)
        )

    cursor.execute("SELECT DISTINCT product_name FROM prices")
    old_products = cursor.fetchall()

    print("Unique products found:", len(old_products))

    for product in old_products:
        cursor.execute(
            "INSERT INTO products (name) VALUES (?)",
            (product["product_name"],)
        )

    cursor.execute("""
        CREATE TABLE prices_new (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            store_id INTEGER NOT NULL,
            product_id INTEGER NOT NULL,
            price REAL NOT NULL,
            last_updated TEXT NOT NULL,
            FOREIGN KEY(store_id) REFERENCES stores(id),
            FOREIGN KEY(product_id) REFERENCES products(id)
        )
    """)

    # Copy every old row, swapping the names for the matching store and product ids.
    # The id is copied too, so existing price ids stay the same.
    cursor.execute("""
        INSERT INTO prices_new (id, store_id, product_id, price, last_updated)
        SELECT
            prices.id,
            stores.id,
            products.id,
            prices.price,
            prices.last_updated
        FROM prices
        JOIN stores ON prices.store_name = stores.name
        JOIN products ON prices.product_name = products.name
    """)

    # Check 1: no rows were lost by the JOINs
    cursor.execute("SELECT COUNT(*) FROM prices_new")
    migrated_count = cursor.fetchone()[0]
    print("Records migrated:", migrated_count)

    if migrated_count != len(old_prices):
        raise Exception(f"Expected {len(old_prices)} records but migrated {migrated_count}")

    # Check 2: every store_id and product_id points at a real row
    cursor.execute("PRAGMA foreign_key_check(prices_new)")
    broken_links = cursor.fetchall()

    if broken_links:
        raise Exception(f"Found {len(broken_links)} broken foreign keys")

    # Check 3: each new row matches its old row (same names, price and timestamp)
    cursor.execute("""
        SELECT COUNT(*)
        FROM prices_new
        JOIN prices ON prices.id = prices_new.id
        JOIN stores ON stores.id = prices_new.store_id
        JOIN products ON products.id = prices_new.product_id
        WHERE stores.name = prices.store_name
          AND products.name = prices.product_name
          AND prices_new.price = prices.price
          AND prices_new.last_updated = prices.last_updated
    """)
    matching_count = cursor.fetchone()[0]

    if matching_count != len(old_prices):
        raise Exception(f"Only {matching_count} of {len(old_prices)} records match the original data")

    print("All checks passed.")

    # Swap the tables: keep the old one as prices_old, new one becomes prices
    cursor.execute("ALTER TABLE prices RENAME TO prices_old")
    cursor.execute("ALTER TABLE prices_new RENAME TO prices")

    conn.commit()
    print("Migration committed.")

except Exception as error:
    conn.rollback()
    print("Migration failed, all changes rolled back:", error)
    sys.exit(1)

finally:
    conn.close()
