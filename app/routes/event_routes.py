from flask import Blueprint, render_template, request, session, redirect, url_for
from app.extensions import db
from app.models.event import Event
from app.utils.auth import admin_required

event = Blueprint("event", __name__)

@event.route("/")
def index():
    events = Event.query.all()
    return render_template("index.html", events=events)


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