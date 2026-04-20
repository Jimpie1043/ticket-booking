from app.extensions import db

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    date = db.Column(db.String(50))
    capacity = db.Column(db.Integer, nullable=False)
    tags = db.Column(db.String(50))

    # Définit une relation entre booking (child) et event (parent)
    bookings = db.relationship(
        "Booking",
        backref="event",
        lazy=True,
        cascade="all, delete-orphan" # Assure la suppression des bookings quand un event est supprime
    )