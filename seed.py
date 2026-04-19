import os
import bcrypt
from dotenv import load_dotenv

from app.extensions import db
from app.models.user import User

load_dotenv()

def run_seed(app):
    with app.app_context():
        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")

        if not admin_email or not admin_password:
            raise ValueError("ADMIN_EMAIL or ADMIN_PASSWORD missing in environment")

        existing_admin = User.query.filter_by(email=admin_email).first()

        if not existing_admin:
            hashed = bcrypt.hashpw(
                admin_password.encode("utf-8"),
                bcrypt.gensalt()
            )

            admin = User(
                email=admin_email,
                password=hashed.decode("utf-8"),
                role="admin"
            )

            db.session.add(admin)
            db.session.commit()
            print("Admin user created")
        else:
            print("Admin already exists")