from flask import Blueprint, redirect, url_for, session
from app import db
from app.models.booking import Booking

booking = Blueprint('booking', __name__)

@booking.route('/book/<int:event_id>')
def book(event_id):
    if 'user_id' not in session:
        return redirect(url_for('auth.login'))

    new_booking = Booking(
        user_id=session['user_id'],
        event_id=event_id
    )

    db.session.add(new_booking)
    db.session.commit()

    return redirect(url_for('event.index'))