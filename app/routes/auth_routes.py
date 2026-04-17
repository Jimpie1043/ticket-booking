from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import bcrypt
from app.extensions import db
from app.models.user import User
from app.utils.security import validate_email, validate_password
from app.utils.auth import login_required

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")
        password_repeat = request.form.get("password_repeat", "")

        if not validate_email(email):
            flash("Format de courriel invalide.", "error")
            return render_template("inscription.html")

        if not validate_password(password):
            flash("Le mot de passe doit contenir au moins 8 caractères.", "error")
            return render_template("inscription.html")

        if password != password_repeat:
            flash("Les mots de passe ne correspondent pas.", "error")
            return render_template("inscription.html")

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash("Cet utilisateur existe déjà.", "error")
            return render_template("inscription.html")

        try:
            hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

            new_user = User(
                email=email,
                password=hashed_pw.decode("utf-8"),
                role="user"
            )
            db.session.add(new_user)
            db.session.commit()

            flash("Inscription réussie ! Vous pouvez maintenant vous connecter.", "success")
            return redirect(url_for("auth.login"))

        except Exception:
            db.session.rollback()
            flash("Erreur serveur lors de la création du compte.", "error")
            return render_template("inscription.html")

    return render_template("inscription.html")


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email", "").strip()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()

        if not user:
            flash("Identifiants invalides.", "error")
            return render_template("connexion.html")

        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")):
            flash("Identifiants invalides.", "error")
            return render_template("connexion.html")

        session["user_id"] = user.id
        session["role"] = user.role
        session["user_email"] = user.email

        flash("Connexion réussie !", "success")
        return redirect(url_for("event.index"))

    return render_template("connexion.html")


@auth.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Vous êtes maintenant déconnecté.", "success")
    return redirect(url_for("event.index"))