from app.extensions import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), default="user")

    bookings = db.relationship(
        "Booking",
        backref="user",
        lazy=True,
        cascade="all, delete-orphan") # Assure la suppression des bookings quand un utilisateur est supprime