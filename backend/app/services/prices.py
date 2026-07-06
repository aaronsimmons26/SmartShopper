
def get_all_prices():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM price_entries")

    rows = cursor.fetchall()

    conn.close()

    return [
        {
            'id': row['id'],
            'store_name': row['store_name'],
            'product_name': row['product_name'],
            'price': row['price'],
            'last_updated': row['last_updated']
        }
        for row in rows
    ]