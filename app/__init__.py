import os
from flask import Flask
from dotenv import load_dotenv

from .config import Config
from .extensions import db, migrate
from app.utils.security import init_security
from flask_wtf.csrf import CSRFProtect

from app.models.user import User
import bcrypt

csrf = CSRFProtect()

load_dotenv()

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    # Crée le instance folder s'il n'existe pas
    instance_path = os.path.join(
        os.path.dirname(__file__),
        "..",
        "instance"
    )
    os.makedirs(instance_path, exist_ok=True)

    app.config.from_object(Config)

    init_security(app)
    csrf.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    # Crée le compte admin s'il n'existe pas
    with app.app_context():
        db.create_all()

        admin_email = os.getenv("ADMIN_EMAIL")
        admin_password = os.getenv("ADMIN_PASSWORD")

        if admin_email and admin_password:
            admin = User.query.filter_by(email=admin_email).first()

            if not admin:
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

    from .routes.auth_routes import auth
    from .routes.event_routes import event
    from .routes.booking_routes import booking
    from .routes.admin_routes import admin
    from .routes.user_routes import user

    app.register_blueprint(auth)
    app.register_blueprint(event)
    app.register_blueprint(booking)
    app.register_blueprint(admin)
    app.register_blueprint(user)

    return app