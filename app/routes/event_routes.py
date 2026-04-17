from flask import Blueprint, render_template, request, session, redirect, url_for
from app.extensions import db
from app.models.event import Event
from app.models.booking import Booking
from app.utils.auth import admin_required

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

@event.route("/admin")
@admin_required
def admin_dashboard():
    events = Event.query.all()
    return render_template("tableau_admin.html", events=events)

@event.route("/events/create", methods=["POST"])
@admin_required
def create_event():
    new_event = Event(
        title=request.form["title"],
        description=request.form.get("description"),
        date=request.form["date"],
        capacity=int(request.form["capacity"])
    )

    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for("event.admin_dashboard"))

@event.route("/events/edit/<int:event_id>", methods=["GET", "POST"])
@admin_required
def edit_event(event_id):
    event_obj = Event.query.get_or_404(event_id)

    if request.method == "POST":
        event_obj.title = request.form["title"]
        event_obj.description = request.form.get("description")
        event_obj.date = request.form["date"]
        event_obj.capacity = int(request.form["capacity"])

        db.session.commit()

        return redirect(url_for("event.admin_dashboard"))

    return render_template("modifier_event.html", event=event_obj)

@event.route("/events/delete/<int:event_id>", methods=["POST"])
@admin_required
def delete_event(event_id):
    event_obj = Event.query.get_or_404(event_id)

    try:
        db.session.delete(event_obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

    return redirect(url_for("event.admin_dashboard"))