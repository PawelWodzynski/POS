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
