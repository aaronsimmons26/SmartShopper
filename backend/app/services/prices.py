
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

def get_or_create_store(store_name):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id from stores WHERE name = ?", (store_name,))

    query = cursor.fetchone()

    if query is None:
        cursor.execute("""
        INSERT INTO stores (name)
        VALUES (?)
        """, (store_name,))

        conn.commit()
        new_id = cursor.lastrowid
        conn.close()

        return new_id

    store_id = query['id']
    conn.close()

    return store_id

def get_or_create_product(product_name):
    conn = get_connection()
    cursor = conn.cursor()
    new_id = 0
    cursor.execute("SELECT id from products WHERE name = ?", (product_name,))

    query = cursor.fetchone()

    if query is None:
        cursor.execute("""
        INSERT INTO products (name)
        VALUES (?)
        """, (product_name,))

        new_id = cursor.lastrowid

        conn.commit()
        conn.close()
    else:
        new_id = query['id']

    conn.close()

    return new_id


def create_price(store_name, product_name, price):
    store_id = get_or_create_store(store_name)
    product_id = get_or_create_product(product_name)
    now = dt.datetime.now().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO prices (store_id, product_id, price, last_updated)
    VALUES (?, ?, ?, ?)
    """, (store_id, product_id, price, now))

    new_id = cursor.lastrowid

    conn.commit()
    conn.close()

    return get_price_by_id(new_id)

def update_price(id, store_name, product_name, price):
    now = dt.datetime.now().isoformat()

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE prices
    SET store_name = ?, product_name = ?, price = ?, last_updated = ?
    WHERE id = ?
    """, (store_name, product_name, price, now, id))

    updated = cursor.rowcount > 0

    conn.commit()
    conn.close()

    if not updated:
        return None

    return get_price_by_id(id)

def delete_price(id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM prices
    WHERE id = ?
    """, (id,))

    updated = cursor.rowcount > 0

    conn.commit()
    conn.close()

    return updated
