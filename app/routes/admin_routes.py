from flask import Blueprint, render_template, request, redirect, url_for
from app.extensions import db
from app.models.event import Event
from app.utils.auth import admin_required

admin = Blueprint("admin", __name__)

# Routes qui requièrent un compte admin

@admin.route("/admin")
@admin_required
def admin_dashboard():
    events = Event.query.all()
    return render_template("tableau_admin.html", events=events)

@admin.route("/events/create", methods=["POST"])
@admin_required
def create_event():
    new_event = Event(
        title=request.form["title"],
        description=request.form.get("description"),
        date=request.form["date"],
        capacity=int(request.form["capacity"]),
        tags=request.form.get("tags") or "Aucun"
    )

    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for("admin.admin_dashboard"))

@admin.route("/events/edit/<int:event_id>", methods=["GET", "POST"])
@admin_required
def edit_event(event_id):
    # Cherche l'événement avec son id et retourne 404 s'il n'est pas trouvé
    event_obj = Event.query.get_or_404(event_id)

    if request.method == "POST":
        event_obj.title = request.form["title"]
        event_obj.description = request.form.get("description")
        event_obj.date = request.form["date"]
        event_obj.capacity = int(request.form["capacity"])
        event_obj.tags = request.form.get("tags") or "Aucun"

        db.session.commit()

        return redirect(url_for("admin.admin_dashboard"))

    return render_template("modifier_event.html", event=event_obj)

@admin.route("/events/delete/<int:event_id>", methods=["POST"])
@admin_required
def delete_event(event_id):
    event_obj = Event.query.get_or_404(event_id)

    try:
        db.session.delete(event_obj)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(e)

    return redirect(url_for("admin.admin_dashboard"))