from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def homepage():
    return jsonify({'message': 'Home'})

@app.route('/shopping-plan', methods=['POST'])
def post_shopping_plan():
    data = request.get_json()
    return {'message': 'Shopping plan endpoint created',
            'received': data
            }

if __name__ == '__main__':
    app.run(debug=True)