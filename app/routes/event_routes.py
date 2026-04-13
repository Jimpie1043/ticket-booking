from flask import Blueprint, render_template
from app.models.event import Event

event = Blueprint('event', __name__)

@event.route('/')
def index():
    events = Event.query.all()
    return render_template('index.html', events=events)