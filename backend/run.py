from flask import Flask, jsonify, request

from app.database.db import initialize_database
from app.services.prices import (
    get_all_prices,
    get_price_by_id,
    create_price,
    update_price,
    delete_price
)

initialize_database()

app = Flask(__name__)

def validate_price_data(data):
    """Return an error message if the request body is invalid, otherwise None."""
    if not isinstance(data, dict):
        return 'Request body must be a JSON object'

    for field in ('store_name', 'product_name'):
        value = data.get(field)
        if not isinstance(value, str) or not value.strip():
            return f'{field} is required and must be a non-empty string'

    price = data.get('price')
    # bool is a subclass of int in Python, so rule it out explicitly
    if isinstance(price, bool) or not isinstance(price, (int, float)):
        return 'price is required and must be a number'

    if price <= 0:
        return 'price must be greater than 0'

    return None

@app.route('/')
def homepage():
    return jsonify({'message': 'Home'})

@app.route('/prices', methods=['GET'])
def get_prices():
    prices = get_all_prices()
    return jsonify(prices)

@app.route('/prices', methods=['POST'])
def add_price():
    data = request.get_json(silent=True)

    error = validate_price_data(data)
    if error:
        return jsonify({'message': error}), 400

    new_price = create_price(
        data['store_name'].strip(),
        data['product_name'].strip(),
        data['price']
    )

    return jsonify(new_price), 201

@app.route('/prices/<int:id>', methods=['GET'])
def get_price(id):
    price = get_price_by_id(id)

    if price is None:
        return jsonify({'message': 'Price not found'}), 404

    return jsonify(price)

@app.route('/prices/<int:id>', methods=['PUT'])
def modify_price(id):
    data = request.get_json(silent=True)

    error = validate_price_data(data)
    if error:
        return jsonify({'message': error}), 400

    price = update_price(
        id,
        data['store_name'].strip(),
        data['product_name'].strip(),
        data['price']
    )

    if price is None:
        return jsonify({'message': 'Price not found'}), 404

    return jsonify(price)

@app.route('/prices/<int:id>', methods=['DELETE'])
def remove_price(id):
    price = delete_price(id)

    if price is False:
        return jsonify({'message': 'Price not found'}), 404

    return jsonify({'message': 'Price deleted successfully'})

@app.route('/shopping-plan', methods=['POST'])
def post_shopping_plan():
    data = request.get_json()
    return {'message': 'Shopping plan endpoint created',
            'received': data
            }

if __name__ == '__main__':
    app.run(debug=True)