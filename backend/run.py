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

@app.route('/')
def homepage():
    return jsonify({'message': 'Home'})

@app.route('/prices')
def get_prices():
    prices = get_all_prices()
    return jsonify(prices)

@app.route('/prices', methods=['POST'])
def add_price():
    data = request.get_json()

    new_price = create_price(
        data['store_name'],
        data['product_name'],
        data['price']
    )

    return jsonify(new_price), 201

@app.route('/prices/<int:id>', methods=['GET'])
def get_price(id):
    price = get_price_by_id(id)

    if price is None:
        return jsonify({'message': 'Price not found'}), 404

    return jsonify(price)

@app.route('/shopping-plan', methods=['POST'])
def post_shopping_plan():
    data = request.get_json()
    return {'message': 'Shopping plan endpoint created',
            'received': data
            }

if __name__ == '__main__':
    app.run(debug=True)