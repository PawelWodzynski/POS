from flask import Blueprint, request, jsonify, session, redirect, url_for

category_bp = Blueprint("category", __name__)

@category_bp.route("/api/categories", methods=["GET"])
def proxy_categories():
    """
    Proxy endpoint that fetches categories from FakeStoreAPI and returns them unchanged.
    GET /api/categories -> forwards to https://fakestoreapi.com/products/categories
    """
    base = "https://fakestoreapi.com"
    url = f"{base.rstrip('/')}/products/categories"

    # Check if user is logged in
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    import requests
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        data = resp.json()
        return jsonify(data)
    except requests.RequestException as exc:
        return jsonify({"error": "failed to fetch categories", "detail": str(exc)}), 502

@category_bp.route("/api/categories", methods=["POST"])
def create_category():
    """
    Simulated endpoint to create a category.
    Accepts JSON with 'category' field and returns it in response.
    Only accessible to logged-in users.
    """
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401

    data = request.get_json()
    category_name = data.get("category")
    if not category_name or category_name.strip() == "":
        return jsonify({"error": "Category name cannot be empty"}), 400

    # Simulate creation by returning the category name
    return jsonify({"category": category_name}), 201
