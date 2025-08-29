from flask import Blueprint, request, jsonify, redirect, url_for, render_template, current_app
from extensions import db
from flask_jwt_extended import create_access_token
from sqlalchemy import text
import bcrypt
import datetime

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/", methods=["GET"])
def root_redirect():
    return redirect(url_for("auth.main_page"))

@auth_bp.route("/main-page", methods=["GET"])
def main_page():
    return render_template("main.html")

@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("register.html")

@auth_bp.route("/api/register", methods=["POST"])
def api_register():
    payload = request.get_json() if request.is_json else request.form
    login = payload.get("login", "").strip()
    password = payload.get("password", "")
    email = payload.get("email", "").strip()

    if not login or not password or not email:
        return jsonify({"error": "login, password and email are required"}), 400

    # Hashowanie hasła przy użyciu bcrypt
    hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    params = {
        "login": login,
        "password": hashed,
        "email": email,
        "city": payload.get("city"),
        "street": payload.get("street"),
        "postal_code": payload.get("postal_code"),
        "first_name": payload.get("first_name"),
        "last_name": payload.get("last_name"),
        "role_id": 2
    }

    try:
        stmt = text("""
            INSERT INTO customers (login, password, email, city, street, postal_code, first_name, last_name, role_id)
            VALUES (:login, :password, :email, :city, :street, :postal_code, :first_name, :last_name, :role_id)
            RETURNING id
        """)
        res = db.session.execute(stmt, params)
        user_id = res.scalar_one()
        db.session.commit()

        expires = datetime.timedelta(hours=12)
        token = create_access_token(identity=int(user_id), expires_delta=expires)
        return jsonify({"access_token": token, "user_id": user_id}), 201
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception("Registration failed")
        return jsonify({"error": "registration failed", "detail": str(exc)}), 400

@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    payload = request.get_json() if request.is_json else request.form
    login = payload.get("login", "").strip()
    password = payload.get("password", "")

    if not login or not password:
        return jsonify({"error": "login and password are required"}), 400

    try:
        stmt = text("SELECT id, password FROM customers WHERE login = :login LIMIT 1")
        row = db.session.execute(stmt, {"login": login}).fetchone()

        if not row:
            return jsonify({"error": "invalid credentials"}), 401

        user_id, stored_hash = row

        # Weryfikacja hasła przez bcrypt
        if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
            return jsonify({"error": "invalid credentials"}), 401

        expires = datetime.timedelta(hours=12)
        token = create_access_token(identity=int(user_id), expires_delta=expires)
        return jsonify({"access_token": token, "user_id": user_id}), 200

    except Exception as exc:
        current_app.logger.exception("Login failed")
        return jsonify({"error": "login failed", "detail": str(exc)}), 500
