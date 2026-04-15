from flask import Blueprint, render_template, request, session, redirect, url_for, abort
from app.extensions import db
from app.models.event import Event
from app.models.booking import Booking
from app.utils.auth import login_required, admin_required

event = Blueprint("event", __name__)

@event.route("/")
def index():
    events = Event.query.all()
    return render_template("index.html", events=events)


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

    return redirect(url_for("event.index"))


@event.route("/events/delete/<int:event_id>", methods=["POST"])
@admin_required
def delete_event(event_id):
    event_obj = Event.query.get_or_404(event_id)

    db.session.delete(event_obj)
    db.session.commit()

    return redirect(url_for("event.index"))