from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime
from app.extensions import db
from app.models.event import Event
from app.utils.auth import admin_required
from app.utils.security import sanitize_string

admin = Blueprint("admin", __name__)

# Routes qui requièrent un compte admin

def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

@admin.route("/admin")
@admin_required
def admin_dashboard():
    events = Event.query.all()
    return render_template("tableau_admin.html", events=events)

@admin.route("/events/create", methods=["POST"])
@admin_required
def create_event():

    date = sanitize_string(request.form["date"])

    if not validate_date(date):
        return "Format de date invalide. Utiliser YYYY-MM-DD", 400
    
    capacity = int(request.form["capacity"])
    
    if capacity < 0:
        return "Capacité invalide", 400

    new_event = Event(
        title=sanitize_string(request.form["title"]),
        description=sanitize_string(request.form.get("description")) or "Aucune",
        date=date,
        capacity=capacity,
        tags=sanitize_string(request.form.get("tags")) or "Aucun"
    )

    db.session.add(new_event)
    db.session.commit()

    return redirect(url_for("admin.admin_dashboard"))

@admin.route("/events/edit/<int:event_id>", methods=["GET", "POST"])
@admin_required
def edit_event(event_id):

    event_obj = Event.query.get_or_404(event_id)

    if request.method == "POST":

        date = sanitize_string(request.form["date"])

        if not validate_date(date):
            return "Format de date invalide. Utiliser YYYY-MM-DD", 400
        
        capacity = int(request.form["capacity"])
    
        if capacity < 0:
            return "Capacité invalide", 400

        event_obj.title = sanitize_string(request.form["title"])
        event_obj.description = sanitize_string(request.form.get("description")) or "Aucune"
        event_obj.date = sanitize_string(date)
        event_obj.capacity = capacity
        event_obj.tags = sanitize_string(request.form.get("tags")) or "Aucun"

        db.session.commit()

        return redirect(url_for("admin.admin_dashboard")) # Si "POST"

    return render_template("modifier_event.html", event=event_obj) # Si "GET"

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