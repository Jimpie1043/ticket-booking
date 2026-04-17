from flask import Blueprint, render_template, request, session, redirect, url_for
from app.extensions import db
from app.models.event import Event
from app.models.booking import Booking

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
    event_obj = Event.query.get_or_404(event_id)

    user_booking = None
    if "user_id" in session:
        user_booking = Booking.query.filter_by(
            event_id=event_id,
            user_id=session["user_id"]
        ).first()

    total_bookings = Booking.query.filter_by(event_id=event_id).count()

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

    if existing_booking:
        return redirect(url_for("event.event_page", event_id=event_id))

    total_bookings = Booking.query.filter_by(event_id=event_id).count()

    if total_bookings >= event_obj.capacity:
        return redirect(url_for("event.event_page", event_id=event_id))

    new_booking = Booking(
        user_id=session["user_id"],
        event_id=event_id
    )

    db.session.add(new_booking)
    db.session.commit()

    return redirect(url_for("event.event_page", event_id=event_id))