import os
import pkgutil
import importlib
from flask import Flask, Blueprint, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
import requests

# Expose commonly-used extensions so other modules can import them from app
db = SQLAlchemy()
jwt = JWTManager()


def register_blueprints(app: Flask, package_name: str = "controllers"):
    """
    Dynamically import modules from the controllers package and register any Flask.Blueprint
    instances found in them. This makes the app resilient to blueprint variable names.
    """
    try:
        package = importlib.import_module(package_name)
    except Exception:
        # controllers package not present or import failed
        return

    if not hasattr(package, "__path__"):
        return

    for finder, name, ispkg in pkgutil.iter_modules(package.__path__):
        # import the module
        module_name = f"{package_name}.{name}"
        try:
            module = importlib.import_module(module_name)
        except Exception:
            # skip modules that fail to import
            continue

        # register any attribute that is a Blueprint
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, Blueprint):
                try:
                    app.register_blueprint(attr)
                except Exception:
                    # ignore registration errors, allow other blueprints to register
                    pass


def create_app(test_config: dict = None) -> Flask:
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Basic configuration with sane defaults — override with environment variables or config.py
    app.config.setdefault("SECRET_KEY", os.getenv("SECRET_KEY", "dev-secret"))
    app.config.setdefault("JWT_SECRET_KEY", os.getenv("JWT_SECRET_KEY", os.getenv("SECRET_KEY", "dev-secret")))
    app.config.setdefault("SQLALCHEMY_DATABASE_URI", os.getenv("DATABASE_URL", "postgresql://postgres:postgres@localhost:5432/pos_db"))
    app.config.setdefault("SQLALCHEMY_TRACK_MODIFICATIONS", False)
    app.config.setdefault("FAKESTORE_API_BASE", os.getenv("FAKESTORE_API_BASE", "https://fakestoreapi.com"))

    # Allow optional config.py to supply configuration (if present in project)
    try:
        import config as project_config  # type: ignore
        # Only load attributes that are UPPERCASE to mimic Flask config.from_object behavior
        for k in dir(project_config):
            if k.isupper():
                app.config[k] = getattr(project_config, k)
    except Exception:
        # no config.py or failed to import — continue with defaults/env
        pass

    if test_config:
        app.config.update(test_config)

    # initialize extensions
    db.init_app(app)
    jwt.init_app(app)
    CORS(app, resources={r"/*": {"origins": "*"}})

    # setup a requests.Session for reuse (used by services talking to FakeStoreAPI)
    session = requests.Session()
    app.extensions["http_session"] = session

    # register controllers / blueprints automatically
    register_blueprints(app, "controllers")

    # simple health endpoint
    @app.route("/_health")
    def health():
        return jsonify({"status": "ok"})

    return app


# create app for WSGI servers
app = create_app()

if __name__ == "__main__":
    # Development server
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)), debug=os.getenv("FLASK_DEBUG", "1") != "0")
