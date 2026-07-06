
def get_all_prices():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM prices")

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

def get_price_by_id(id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM prices WHERE id = ?", (id,))

    query = cursor.fetchone()

    conn.close()

    if query is None:
        return None

    return {
        'id': query['id'],
        'store_name': query['store_name'],
        'product_name': query['product_name'],
        'price': query['price'],
        'last_updated': query['last_updated']
    }