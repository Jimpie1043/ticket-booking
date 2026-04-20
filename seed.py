import os
import bcrypt
from dotenv import load_dotenv

from app import create_app
from app.extensions import db
from app.models.user import User

load_dotenv()

app = create_app()

def run_seed():
    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")

    if not admin_email or not admin_password:
        raise ValueError("ADMIN_EMAIL and/or ADMIN_PASSWORD missing in environment")

    with app.app_context():
        existing_admin = User.query.filter_by(email=admin_email, role="admin").first()

        if existing_admin:
            print("Admin already exists")
            return

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

if __name__ == "__main__":
    run_seed()