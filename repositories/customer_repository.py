from extensions import db
from sqlalchemy import text
from flask import current_app

class CustomerRepository:
    @staticmethod
    def get_customer_by_id(user_id):
        try:
            stmt = text("SELECT id, login, email, city, street, postal_code, first_name, last_name, password FROM customers WHERE id = :id")
            row = db.session.execute(stmt, {"id": user_id}).fetchone()
            return row
        except Exception as exc:
            current_app.logger.exception("Failed to get customer by id")
            raise

    @staticmethod
    def get_customer_by_login(login):
        try:
            stmt = text("SELECT id, login, email, city, street, postal_code, first_name, last_name, password FROM customers WHERE login = :login")
            row = db.session.execute(stmt, {"login": login}).fetchone()
            return row
        except Exception as exc:
            current_app.logger.exception("Failed to get customer by login")
            raise

    @staticmethod
    def check_email_exists(email, exclude_id=None):
        try:
            if exclude_id:
                stmt = text("SELECT id FROM customers WHERE email = :email AND id != :id")
                row = db.session.execute(stmt, {"email": email, "id": exclude_id}).fetchone()
            else:
                stmt = text("SELECT id FROM customers WHERE email = :email")
                row = db.session.execute(stmt, {"email": email}).fetchone()
            return row is not None
        except Exception as exc:
            current_app.logger.exception("Failed to check email existence")
            raise

    @staticmethod
    def insert_customer(params):
        try:
            stmt = text("""
                INSERT INTO customers (login, password, email, city, street, postal_code, first_name, last_name, role_id)
                VALUES (:login, :password, :email, :city, :street, :postal_code, :first_name, :last_name, :role_id)
                RETURNING id
            """)
            res = db.session.execute(stmt, params)
            user_id = res.scalar_one()
            db.session.commit()
            return user_id
        except Exception as exc:
            db.session.rollback()
            current_app.logger.exception("Failed to insert customer")
            raise

    @staticmethod
    def update_profile(user_id, email, city, street, postal_code):
        try:
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
        except Exception as exc:
            db.session.rollback()
            current_app.logger.exception("Failed to update profile")
            raise

    @staticmethod
    def update_password(user_id, new_hashed_password):
        try:
            stmt = text("UPDATE customers SET password = :password WHERE id = :id")
            db.session.execute(stmt, {"password": new_hashed_password, "id": user_id})
            db.session.commit()
        except Exception as exc:
            db.session.rollback()
            current_app.logger.exception("Failed to update password")
            raise
