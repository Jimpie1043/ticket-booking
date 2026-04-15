from flask import Flask
from .config import Config
from .extensions import db, migrate

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.auth_routes import auth
    from .routes.event_routes import event
    from .routes.booking_routes import booking

    app.register_blueprint(auth)
    app.register_blueprint(event)
    app.register_blueprint(booking)

    return app