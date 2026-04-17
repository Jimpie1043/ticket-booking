from app.extensions import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.String(50))
    capacity = db.Column(db.Integer, nullable=False)

    bookings = db.relationship(
        "Booking",
        backref="event",
        lazy=True,
        cascade="all, delete-orphan"
    )