from flask import Blueprint, render_template, request, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from app.models.user import User
from app.utils.security import validate_email, validate_password

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        password_repeat = request.form.get("password_repeat", "")

        if not validate_email(email):
            return "Invalid email format", 400

        if not validate_password(password):
            return "Password too short (min 8 chars)", 400

        if password != password_repeat:
            return "Passwords do not match", 400

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return "Email already registered", 409

        try:
            new_user = User(
                email=email,
                password=generate_password_hash(password),
                role="user"
            )
            db.session.add(new_user)
            db.session.commit()
        except Exception:
            db.session.rollback()
            return "Server error while creating user", 500

        return redirect(url_for("auth.login"))

    return render_template("inscription.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user:
            return "Invalid credentials", 401

        if not check_password_hash(user.password, password):
            return "Invalid credentials", 401

        session["user_id"] = user.id
        session["role"] = user.role

        return redirect(url_for("event.index"))

    return render_template("connexion.html")


@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("event.index"))