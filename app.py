# app.py
import os
from flask import Flask, jsonify
from flask_cors import CORS
from extensions import db, jwt

def create_app(test_config=None):
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Podstawowa konfiguracja
    secret = os.getenv("SECRET_KEY", "dev-secret")
    app.config["SECRET_KEY"] = secret
    app.secret_key = secret  # <-- naprawia problem z sesjami

    app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", secret)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv(
        "DATABASE_URL",
        "postgresql://postgres:postgres@localhost:5432/pos_db"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.config["FAKESTORE_API_BASE"] = "https://fakestoreapi.com"

    if test_config:
        app.config.update(test_config)

    # Initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)

    # Optional: global requests session for proxy
    import requests
    app.extensions["http_session"] = requests.Session()

    # Rejestracja blueprintów
    from controllers.auth_controller import auth_bp
    from controllers.category_controller import category_bp
    from controllers.main_controller import main_bp
    from controllers.product_controller import product_controller

    app.register_blueprint(auth_bp)
    app.register_blueprint(category_bp)
    app.register_blueprint(main_bp)
    app.register_blueprint(product_controller)

    # Health check
    @app.route("/_health")
    def health():
        return jsonify({"status": "ok"})

    return app

app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=True)
