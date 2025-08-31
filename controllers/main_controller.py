from flask import Blueprint, render_template, redirect, url_for, session

main_bp = Blueprint("main", __name__)

@main_bp.route("/", methods=["GET"])
def root_redirect():
    return redirect(url_for("main.main_page"))

@main_bp.route("/main-page", methods=["GET"])
def main_page():
    return render_template("main.html")

@main_bp.route("/cart", methods=["GET"])
def cart_page():
    if not session.get("user_id"):
        return redirect(url_for("auth.login_page"))
    return render_template("cart.html")
