from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.extensions import db
from app.models.user import User
from app.models.booking import Booking
from app.utils.auth import login_required
from app.utils.security import sanitize_string
from app.utils.security import validate_password
import bcrypt


user = Blueprint("user", __name__)


@user.route("/profile")
@login_required
def user_profile():
    user_obj = User.query.get_or_404(session["user_id"])

    bookings = Booking.query.filter_by(user_id=session["user_id"]).all()

    return render_template(
        "tableau_utilisateur.html",
        user=user_obj,
        bookings=bookings
    )


@user.route("/profile/change-password", methods=["POST"])
@login_required
def change_password():
    user_obj = User.query.get_or_404(session["user_id"])

    current_password = sanitize_string(request.form.get("current_password", ""))
    new_password = sanitize_string(request.form.get("new_password", ""))
    confirm_password = sanitize_string(request.form.get("confirm_password", ""))

    # Performe plusieurs verifications
    if not bcrypt.checkpw(current_password.encode("utf-8"), user_obj.password.encode("utf-8")):
        flash("Mot de passe actuel incorrect.", "error")
        return redirect(url_for("user.user_profile"))
    
    if (new_password == current_password):
        flash("Le nouveau mot de passe ne peut pas être le même que le mot de passe actuel.", "error")
        return redirect(url_for("user.user_profile"))

    if not validate_password(new_password):
        flash("Le nouveau mot de passe doit contenir entre 8 et 64 caractères.", "error")
        return redirect(url_for("user.user_profile"))

    if new_password != confirm_password:
        flash("Les mots de passe ne correspondent pas.", "error")
        return redirect(url_for("user.user_profile"))

    hashed = bcrypt.hashpw(new_password.encode("utf-8"), bcrypt.gensalt())
    user_obj.password = hashed.decode("utf-8")

    db.session.commit()

    flash("Mot de passe mis à jour.", "success")
    return redirect(url_for("user.user_profile"))