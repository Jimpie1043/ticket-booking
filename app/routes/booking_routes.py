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
        return "Event full", 400

    new_booking = Booking(
        user_id=session["user_id"],
        event_id=event_id,
        status="confirmed"
    )

    db.session.add(new_booking)
    db.session.commit()

    return redirect(url_for("event.index"))


@booking.route("/cancel/<int:booking_id>")
@login_required
def cancel_booking(booking_id):
    booking_obj = Booking.query.get_or_404(booking_id)

    if booking_obj.user_id != session["user_id"]:
        return "Forbidden", 403

    booking_obj.status = "cancelled"
    db.session.commit()

    return redirect(url_for("event.index"))