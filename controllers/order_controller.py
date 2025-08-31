from flask import Blueprint, request, jsonify

order_controller = Blueprint('order_controller', __name__)

@order_controller.route('/api/order/finalize', methods=['POST'])
def finalize_order():
    """
    Endpoint to finalize an order.
    Expects JSON body with a list of products in the format:
    [
        {"productId": <int>, "count": <int>},
        ...
    ]
    Returns the same list in the response.
    """
    data = request.get_json()
    if not data or not isinstance(data, list):
        return jsonify({"error": "Invalid input format, expected a list of products"}), 400

    # Validate each item has productId and count
    for item in data:
        if 'productId' not in item or 'count' not in item:
            return jsonify({"error": "Each item must have productId and count"}), 400
        if not isinstance(item['productId'], int) or not isinstance(item['count'], int):
            return jsonify({"error": "productId and count must be integers"}), 400

    # Here you could add logic to process the order, e.g. save to DB, check stock, etc.

    return jsonify(data), 200
