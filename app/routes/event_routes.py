from flask import Blueprint, render_template, request, session, redirect, url_for
from app.extensions import db
from app.models.event import Event
from app.models.booking import Booking
import re
from datetime import datetime

event = Blueprint("event", __name__)


@event.route("/")
def index():
    events = Event.query.all()
    return render_template("index.html", events=events)


@event.route("/events")
def all_events():
    events = Event.query.all()
    return render_template("events.html", events=events)


@event.route("/event/<int:event_id>")
def event_page(event_id):
    event_obj = Event.query.get_or_404(event_id) # Si l'event n'existe pas, retourne 404

    # Verifie si le user a un booking
    user_booking = None
    if "user_id" in session:
        user_booking = Booking.query.filter_by(
            event_id=event_id,
            user_id=session["user_id"]
        ).first()

    # Compte le nombre de bookings actifs pour un event
    total_bookings = Booking.query.filter(
        Booking.event_id == event_id,
        Booking.status != "cancelled"
    ).count()

    return render_template(
        "event.html",
        event=event_obj,
        booking=user_booking,
        total_bookings=total_bookings
    )


@event.route("/events/book/<int:event_id>", methods=["POST"])
def book_event(event_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    event_obj = Event.query.get_or_404(event_id)

    existing_booking = Booking.query.filter_by(
        user_id=session["user_id"],
        event_id=event_id
    ).first()

    total_bookings = Booking.query.filter(
        Booking.event_id == event_id,
        Booking.status != "cancelled"
    ).count()

    if total_bookings >= event_obj.capacity:
        return redirect(url_for("event.event_page", event_id=event_id))

    if existing_booking:
        if existing_booking.status == "cancelled":
            existing_booking.status = "pending"
            db.session.commit()
        return redirect(url_for("event.event_page", event_id=event_id))

    new_booking = Booking(
        user_id=session["user_id"],
        event_id=event_id,
        status="pending"
    )

    db.session.add(new_booking)
    db.session.commit()

    return redirect(url_for("event.event_page", event_id=event_id))


# Fonctions pour vérification des inputs de simulation de paiement
def validate_cardholder_name(name: str) -> bool:
    # Filtre pour: lettres, espaces, traits d'union et apostrophes, 2–60 caractères
    return bool(re.fullmatch(r"[A-Za-zÀ-ÿ\s'-]{2,60}", name.strip()))


def validate_card_number(number: str) -> bool:
    # Enlève les espaces et tirets
    number = re.sub(r"[ -]", "", number)

    # Doit être entre 8 et 19 chiffres
    if not re.fullmatch(r"\d{8,19}", number):
        return False
    
    return True


def validate_expiration_date(date_str: str) -> bool:
    # Format MM/YY, filtre les caractères inutiles
    if not re.fullmatch(r"(0[1-9]|1[0-2])\/\d{2}", date_str):
        return False

    month, year = date_str.split("/")
    month = int(month)
    year = int("20" + year)

    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # Vérifie si la carte est expirée
    if year < current_year:
        return False
    if year == current_year and month < current_month:
        return False

    return True


def validate_cvv(cvv: str) -> bool:
    # 3 OU 4 chiffres
    return bool(re.fullmatch(r"\d{3,4}", cvv))


@event.route("/simulation-paiement/<int:event_id>", methods=["GET", "POST"])
def simulation_paiement(event_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    event_obj = Event.query.get_or_404(event_id)

    booking = Booking.query.filter_by(
        event_id=event_id,
        user_id=session["user_id"]
    ).first_or_404()

    errors = {}

    if request.method == "POST":
        cardholder_name = request.form.get("nom_carte", "")
        card_number = request.form.get("numero_carte", "")
        card_expiration_date = request.form.get("expiration", "")
        card_cvv = request.form.get("cvv", "")

        if not validate_cardholder_name(cardholder_name):
            errors["name"] = "Invalid name"

        if not validate_card_number(card_number):
            errors["number"] = "Invalid card number"

        if not validate_expiration_date(card_expiration_date):
            errors["expiration"] = "Invalid or expired date"

        if not validate_cvv(card_cvv):
            errors["cvv"] = "Invalid CVV"

        if not errors:
            booking.status = "paid"
            db.session.commit()
            return redirect(url_for("event.event_page", event_id=event_id))
        
        
    return render_template(
        "simulation_paiement.html",
        event=event_obj,
        booking=booking,
        errors=errors
    )


@event.route("/booking/cancel/<int:event_id>", methods=["POST"])
def cancel_booking(event_id):
    if "user_id" not in session:
        return redirect(url_for("auth.login"))

    booking = Booking.query.filter_by(
        event_id=event_id,
        user_id=session["user_id"]
    ).first_or_404()

    booking.status = "cancelled"
    db.session.commit()

    return redirect(url_for("event.event_page", event_id=event_id))