# controllers/auth_controller.py
from flask import Blueprint, request, jsonify, redirect, url_for, render_template, session, current_app
from extensions import db
from flask_jwt_extended import create_access_token
from sqlalchemy import text
import bcrypt
import datetime

auth_bp = Blueprint("auth", __name__)

from flask import session, request

@auth_bp.route("/", methods=["GET"])
def root_redirect():
    if 'user_id' in session:
        return redirect(url_for("auth.main_page"))
    return redirect(url_for("auth.login_page"))

@auth_bp.route("/login", methods=["GET"])
def login_page():
    # Clear session when loading login page
    session.clear()
    return render_template("login.html")

@auth_bp.route("/register", methods=["GET"])
def register_page():
    # Clear session when loading register page
    session.clear()
    return render_template("register.html")

@auth_bp.route("/logout", methods=["GET"])
def logout():
    session.clear()
    return redirect(url_for("auth.login_page"))

@auth_bp.route("/main-page", methods=["GET"])
def main_page():
    return render_template("main.html")

@auth_bp.route("/profile", methods=["GET"])
def profile_page():
    if 'user_id' not in session:
        return redirect(url_for("auth.login_page"))
    return render_template("profile.html")

@auth_bp.route("/api/profile", methods=["GET"])
def get_profile():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user_id = session['user_id']
    try:
        stmt = text("SELECT email, city, street, postal_code FROM customers WHERE id = :id")
        row = db.session.execute(stmt, {"id": user_id}).fetchone()
        if not row:
            return jsonify({"error": "User not found"}), 404
        email, city, street, postal_code = row
        return jsonify({
            "email": email,
            "city": city,
            "street": street,
            "postal_code": postal_code
        })
    except Exception as exc:
        current_app.logger.exception("Failed to fetch profile")
        return jsonify({"error": "Failed to fetch profile"}), 500

@auth_bp.route("/api/profile", methods=["PUT"])
def update_profile():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user_id = session['user_id']
    data = request.get_json()
    email = data.get("email")
    city = data.get("city")
    street = data.get("street")
    postal_code = data.get("postal_code")
    try:
        # Check if email is used by another user
        if email:
            existing = db.session.execute(
                text("SELECT id FROM customers WHERE email = :email AND id != :id"),
                {"email": email, "id": user_id}
            ).fetchone()
            if existing:
                return jsonify({"error": "Email already in use"}), 400
        stmt = text("""
            UPDATE customers SET email = :email, city = :city, street = :street, postal_code = :postal_code
            WHERE id = :id
        """)
        db.session.execute(stmt, {
            "email": email,
            "city": city,
            "street": street,
            "postal_code": postal_code,
            "id": user_id
        })
        db.session.commit()
        return jsonify({"message": "Profile updated"})
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception("Failed to update profile")
        return jsonify({"error": "Failed to update profile"}), 500

@auth_bp.route("/api/profile/password", methods=["PUT"])
def update_password():
    if 'user_id' not in session:
        return jsonify({"error": "Unauthorized"}), 401
    user_id = session['user_id']
    data = request.get_json()
    current_password = data.get("current_password")
    new_password = data.get("new_password")
    if not current_password or not new_password:
        return jsonify({"error": "Current and new password required"}), 400
    try:
        from services.customer_service import CustomerService
        success, error = CustomerService.update_password(user_id, current_password, new_password)
        if not success:
            return jsonify({"error": error}), 400
        return jsonify({"message": "Password updated"})
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception("Failed to update password")
        return jsonify({"error": "Failed to update password"}), 500

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
        # Check if email or login already exists
        existing_user = db.session.execute(
            text("SELECT id FROM customers WHERE email = :email OR login = :login"),
            {"email": params["email"], "login": params["login"]}
        ).fetchone()
        if existing_user:
            return jsonify({"error": "Email or login already exists"}), 400

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

        # Set session on successful registration
        from flask import session
        session['user_id'] = user_id
        session['user_login'] = login

        return jsonify({"access_token": token, "user_id": user_id}), 201
    except Exception as exc:
        db.session.rollback()
        current_app.logger.exception("Registration failed")
        return jsonify({"error": "registration failed", "detail": str(exc)}), 400

@auth_bp.route("/api/login", methods=["POST"])
def api_login():
    from flask import session
    payload = request.get_json() if request.is_json else request.form
    login = payload.get("login", "").strip()
    password = payload.get("password", "")

    if not login or not password:
        return jsonify({"error": "login and password are required"}), 400

    try:
        from services.customer_service import CustomerService
        success, error, user_id, user_login = CustomerService.login_user(login, password)
        if not success:
            return jsonify({"error": error}), 401

        expires = datetime.timedelta(hours=12)
        token = create_access_token(identity=int(user_id), expires_delta=expires)

        # Set session
        session['user_id'] = user_id
        session['user_login'] = user_login

        return jsonify({"access_token": token, "user_id": user_id}), 200
    except Exception as exc:
        current_app.logger.exception("Login failed")
        return jsonify({"error": "login failed", "detail": str(exc)}), 500
