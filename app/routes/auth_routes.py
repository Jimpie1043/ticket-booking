from flask import Blueprint, render_template, request, redirect, url_for, session, flash
import bcrypt
from app.extensions import db
from app.models.user import User
from app.utils.security import validate_email, validate_password
from app.utils.auth import login_required
from app.utils.security import sanitize_string

auth = Blueprint("auth", __name__)

@auth.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        email = sanitize_string(request.form.get("email", "").strip())
        password = sanitize_string(request.form.get("password", ""))
        password_repeat = sanitize_string(request.form.get("password_repeat", ""))

        # Performe plusieurs validation d'inputs
        if not validate_email(email):
            flash("Format de courriel invalide.", "error")
            return render_template("inscription.html")

        if not validate_password(password):
            flash("Le mot de passe doit contenir entre 8 et 64 caractères.", "error")
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
            db.session.add(new_user) # Ajoute l'utilisateur a la db
            db.session.commit()

            flash("Inscription réussie ! Vous pouvez maintenant vous connecter.", "success")
            return redirect(url_for("auth.login")) # Si "POST"

        except Exception:
            db.session.rollback()
            flash("Erreur serveur lors de la création du compte.", "error")
            return render_template("inscription.html") # Sur erreur

    return render_template("inscription.html") # Si "GET"


@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = sanitize_string(request.form.get("email", "").strip())
        password = sanitize_string(request.form.get("password", ""))

        user = User.query.filter_by(email=email).first() # Cherche la db pour trouver le user auquel le email correspond

        if not user: # Si l'utilisateur n'existe pas
            flash("Identifiants invalides.", "error")
            return render_template("connexion.html")

        if not bcrypt.checkpw(password.encode("utf-8"), user.password.encode("utf-8")): # Si le mdp est mauvais
            flash("Identifiants invalides.", "error")
            return render_template("connexion.html")

        # Sinon, initialise la session
        session["user_id"] = user.id
        session["role"] = user.role
        session["user_email"] = user.email

        flash("Connexion réussie !", "success")
        return redirect(url_for("event.index")) # Si "POST"

    return render_template("connexion.html") # Si "GET"


@auth.route("/logout")
@login_required
def logout():
    session.clear()
    flash("Vous êtes maintenant déconnecté.", "success")
    return redirect(url_for("event.index"))