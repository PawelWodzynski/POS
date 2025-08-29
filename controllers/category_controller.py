from flask import Blueprint, current_app, jsonify, make_response
import requests

category_bp = Blueprint("category", __name__)

@category_bp.route("/api/categories", methods=["GET"])
def proxy_categories():
    """
    Proxy endpoint that fetches categories from FakeStoreAPI and returns them unchanged.
    GET /api/categories -> forwards to https://fakestoreapi.com/products/categories
    """
    base = current_app.config.get("FAKESTORE_API_BASE", "https://fakestoreapi.com")
    url = f"{base.rstrip('/')}/products/categories"

    # Prefer a shared session if the app set one up
    session = current_app.extensions.get("http_session") if current_app.extensions else None
    try:
        if session and isinstance(session, requests.sessions.Session):
            resp = session.get(url, timeout=10)
        else:
            resp = requests.get(url, timeout=10)

        # If upstream returned non-JSON or error, forward status and text
        try:
            data = resp.json()
            return make_response(jsonify(data), resp.status_code)
        except ValueError:
            return make_response(resp.text, resp.status_code)
    except requests.RequestException as exc:
        current_app.logger.exception("Failed to fetch categories from FakeStoreAPI")
        return make_response(jsonify({"error": "failed to fetch categories", "detail": str(exc)}), 502)
