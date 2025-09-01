from flask import Blueprint, session, jsonify, abort, request
import requests

product_controller = Blueprint('product_controller', __name__)

@product_controller.route('/api/products/fakestore', methods=['GET'])
def get_fakestore_products():
    # Check if user is logged in
    if 'user_id' not in session:
        abort(401, description="Unauthorized: Login required")

    try:
        response = requests.get('https://fakestoreapi.com/products')
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": "Failed to fetch products from fakestoreapi", "details": str(e)}), 500

@product_controller.route('/api/carts/fakestore', methods=['POST'])
def post_fakestore_cart():
    # Check if user is logged in
    if 'user_id' not in session:
        abort(401, description="Unauthorized: Login required")

    try:
        payload = request.get_json()
        if not payload:
            return jsonify({"error": "Missing JSON payload"}), 400

        response = requests.post(
            'https://fakestoreapi.com/carts',
            json=payload,
            headers={'Content-Type': 'application/json'}
        )
        response.raise_for_status()
        data = response.json()
        return jsonify(data)
    except requests.RequestException as e:
        return jsonify({"error": "Failed to post cart to fakestoreapi", "details": str(e)}), 500

@product_controller.route('/api/products/sort_by_category', methods=['GET'])
def sort_products_by_category():
    # Check if user is logged in
    if 'user_id' not in session:
        abort(401, description="Unauthorized: Login required")

    category = request.args.get('category')
    if not category:
        return jsonify({"error": "Missing category parameter"}), 400

    # For now, just return the category name as requested
    return jsonify({"category": category})

@product_controller.route('/api/products/search', methods=['POST'])
def search_product():
    if 'user_id' not in session:
        abort(401, description="Unauthorized: Login required")

    data = request.get_json()
    product_name = data.get('product_name')
    if not product_name:
        return jsonify({'error': 'Product name is required'}), 400
    return jsonify({'product_name': product_name})

@product_controller.route('/api/products/get_by_id', methods=['POST'])
def get_product_by_id():
    if 'user_id' not in session:
        abort(401, description="Unauthorized: Login required")

    data = request.get_json()
    product_id = data.get('id')
    if not product_id:
        return jsonify({'error': 'Product ID is required'}), 400
    # For now, just echo back the product ID as requested
    return jsonify({'id': product_id})

@product_controller.route('/api/cart/update_product', methods=['POST'])
def update_product_in_cart():
    if 'user_id' not in session:
        abort(401, description="Unauthorized: Login required")

    data = request.get_json()
    product_id = data.get('productId')
    quantity = data.get('quantity')

    if product_id is None or quantity is None:
        return jsonify({'error': 'Product ID and quantity are required'}), 400

    # Here you would update the product quantity in the user's cart in your database or session
    # For demonstration, just echo back the productId and quantity

    return jsonify({'productId': product_id, 'quantity': quantity})

@product_controller.route('/api/cart/remove_product', methods=['DELETE'])
def remove_product_from_cart():
    if 'user_id' not in session:
        abort(401, description="Unauthorized: Login required")

    data = request.get_json()
    product_id = data.get('productId')

    if product_id is None:
        return jsonify({'error': 'Product ID is required'}), 400

    # Here you would remove the product from the user's cart in your database or session
    # For demonstration, just echo back the productId

    return jsonify({'productId': product_id})

@product_controller.route('/api/cart/add_product', methods=['PUT'])
def add_product_to_cart():
    if 'user_id' not in session:
        abort(401, description="Unauthorized: Login required")

    data = request.get_json()
    product_id = data.get('productId')
    quantity = data.get('quantity')

    if product_id is None or quantity is None:
        return jsonify({'error': 'Product ID and quantity are required'}), 400

    # Here you would add the product with quantity to the user's cart in your database or session
    # For demonstration, just echo back the productId and quantity

    return jsonify({'productId': product_id, 'quantity': quantity})

@product_controller.route('/api/cart/update_cart', methods=['POST'])
def update_cart():
    if 'user_id' not in session:
        abort(401, description="Unauthorized: Login required")

    data = request.get_json()
    if not data or not isinstance(data, dict):
        return jsonify({'error': 'Invalid cart data'}), 400

    # Here you would update the entire cart for the user in your database or session
    # For demonstration, just echo back the received cart data

    return jsonify(data)

@product_controller.route('/api/products/add_products_simulation', methods=['POST'])
def add_products_simulation():
    if 'user_id' not in session:
        abort(401, description="Unauthorized: Login required")

    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({'error': 'Invalid input, expected a list of productID:count objects'}), 400

    # Just echo back the received data as a simulation
    return jsonify(data)
