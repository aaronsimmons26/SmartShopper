from flask import Flask, jsonify, request

app = Flask(__name__)

stores = [
    {
        "id": 1,
        "name": "Walmart"
    },
    {
        "id": 2,
        "name": "Publix"
    },
    {
        "id": 3,
        "name": "Aldi"
    }
]

products  = [
    {
        "id": 1,
        "name": "Milk"
    },
    {
        "id": 2,
        "name": "Eggs"
    }
]

price = [
    {
        "product": "Milk",
        "store": "Walmart",
        "price": 3.89
    }
]

price_index = [
    {
        "store": "Walmart",
        "price": 3.89
    },
    {
        "store": "Aldi",
        "price": 3.69
    }
]

new_prices = [

        {"product_id": 1, "store": "Walmart", "price": 3.89},

        {"product_id": 1, "store": "Aldi", "price": 3.69},

        {"product_id": 1, "store": "Publix", "price": 4.49},

        {"product_id": 2, "store": "Walmart", "price": 2.99},

        {"product_id": 2, "store": "Aldi", "price": 2.79},

        {"product_id": 2, "store": "Publix", "price": 3.19},

    ]

@app.route('/')
def homepage():
    return jsonify({'message': 'Home'})

@app.route('/stores')
def get_stores():
    return jsonify(stores)

@app.route('/products')
def get_products():
    return jsonify(products)

@app.route('/products/<int:id>')
def get_product(id):
    for product in products:
        if product['id'] == id:
            return jsonify(product)
    return {'message': 'Product not found'}, 404

@app.route('/prices')
def get_prices():
    return jsonify(price)

@app.route('/prices/<int:product_id>')
def get_prices2(product_id):
    product_prices = []
    for pricer in new_prices:
        if pricer['product_id'] == product_id:
            product_prices.append(pricer)

    return product_prices

@app.route('/shopping-plan', methods=['POST'])
def post_shopping_plan():
    data = request.get_json()
    return {'message': 'Shopping plan endpoint created',
            'received': data
            }









if __name__ == '__main__':
    app.run(debug=True)