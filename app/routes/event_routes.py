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

    return render_template(
        "event.html",
        event=event_obj,
        booking=user_booking
    )

@event.route("/admin")
def admin_dashboard():
    events = Event.query.all()
    return render_template("tableau_admin.html", events=events)

@event.route("/events/create", methods=["POST"])
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
def delete_event(event_id):
    event_obj = Event.query.get_or_404(event_id)

    db.session.delete(event_obj)
    db.session.commit()

    return redirect(url_for("event.admin_dashboard"))