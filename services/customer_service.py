from repositories.customer_repository import CustomerRepository
from flask import current_app
import bcrypt

class CustomerService:
    @staticmethod
    def get_profile(user_id):
        try:
            return CustomerRepository.get_customer_by_id(user_id)
        except Exception as exc:
            current_app.logger.exception("Failed to fetch profile")
            raise

    @staticmethod
    def update_profile(user_id, email, city, street, postal_code):
        try:
            if email and CustomerRepository.check_email_exists(email, exclude_id=user_id):
                return False, "Email already in use"
            CustomerRepository.update_profile(user_id, email, city, street, postal_code)
            return True, None
        except Exception as exc:
            current_app.logger.exception("Failed to update profile")
            raise

    @staticmethod
    def update_password(user_id, current_password, new_password):
        try:
            customer = CustomerRepository.get_customer_by_id(user_id)
            if not customer:
                return False, "User not found"
            stored_hash = customer.password
            if not bcrypt.checkpw(current_password.encode("utf-8"), stored_hash.encode("utf-8")):
                return False, "Current password incorrect"
            new_hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")
            CustomerRepository.update_password(user_id, new_hashed)
            return True, None
        except Exception as exc:
            current_app.logger.exception("Failed to update password")
            raise

    @staticmethod
    def register_user(data):
        login = data.get("login", "").strip()
        password = data.get("password", "")
        email = data.get("email", "").strip()
        city = data.get("city")
        street = data.get("street")
        postal_code = data.get("postal_code")
        first_name = data.get("first_name")
        last_name = data.get("last_name")

        if not login or not password or not email:
            return False, "login, password and email are required", None

        hashed = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

        params = {
            "login": login,
            "password": hashed,
            "email": email,
            "city": city,
            "street": street,
            "postal_code": postal_code,
            "first_name": first_name,
            "last_name": last_name,
            "role_id": 2
        }

        try:
            existing_user = CustomerRepository.get_customer_by_login(login)
            if existing_user:
                return False, "Email or login already exists", None

            user_id = CustomerRepository.insert_customer(params)
            return True, None, user_id
        except Exception as exc:
            current_app.logger.exception("Registration failed")
            return False, "registration failed", None

    @staticmethod
    def login_user(login, password):
        try:
            customer = CustomerRepository.get_customer_by_login(login)
            if not customer:
                return False, "invalid credentials", None, None
            user_id = customer.id
            user_login = customer.login
            stored_hash = customer.password
            if not stored_hash or not (stored_hash.startswith("pbkdf2:") or stored_hash.startswith("$2a$") or stored_hash.startswith("$2b$") or stored_hash.startswith("$2y$") or stored_hash.startswith("scrypt:") or stored_hash.startswith("$2b$") or stored_hash.startswith("$2x$") or stored_hash.startswith("$2y$")):
                current_app.logger.error(f"Invalid password hash for user {login}")
                return False, "invalid credentials", None, None
            if not bcrypt.checkpw(password.encode("utf-8"), stored_hash.encode("utf-8")):
                return False, "invalid credentials", None, None
            return True, None, user_id, user_login
        except Exception as exc:
            current_app.logger.exception("Login failed")
            return False, "login failed", None, None
