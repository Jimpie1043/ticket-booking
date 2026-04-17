from flask import Blueprint, redirect, url_for, session
from app.extensions import db
from app.models.booking import Booking
from app.models.event import Event
from app.utils.auth import login_required

booking = Blueprint("booking", __name__)

@booking.route("/book/<int:event_id>")
@login_required
def book(event_id):
    event_obj = Event.query.get_or_404(event_id)

    current = Booking.query.filter_by(event_id=event_id).count()
    if current >= event_obj.capacity:
        return "Événement plein", 400

    existing = Booking.query.filter_by(
        event_id=event_id,
        user_id=session["user_id"]
    ).first()

    if existing:
        return "Déjà booké", 409

    new_booking = Booking(
        user_id=session["user_id"],
        event_id=event_id,
        status="confirmed"
    )

    try:
        db.session.add(new_booking)
        db.session.commit()
    except Exception:
        db.session.rollback()
        return "Booking non-réussi", 500

    return redirect(url_for("event.event_page", event_id=event_id))


@booking.route("/cancel/<int:booking_id>")
@login_required
def cancel_booking(booking_id):
    booking_obj = Booking.query.get_or_404(booking_id)

    if booking_obj.user_id != session["user_id"]:
        return "Interdit", 403

    booking_obj.status = "cancelled"

    try:
        db.session.commit()
    except Exception:
        db.session.rollback()
        return "Annulation non-réussie", 500

    return redirect(url_for("event.event_page", event_id=booking_obj.event_id))