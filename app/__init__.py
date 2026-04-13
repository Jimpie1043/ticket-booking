from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from .config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__,
                template_folder="templates",
                static_folder="static")

    app.config.from_object(Config)

    db.init_app(app)

    from .routes.auth_routes import auth
    from .routes.event_routes import event
    from .routes.booking_routes import booking

    app.register_blueprint(auth)
    app.register_blueprint(event)
    app.register_blueprint(booking)

    return app