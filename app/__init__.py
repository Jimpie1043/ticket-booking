from flask import Flask
from .config import Config
from .extensions import db, migrate
from app.utils.security import init_security
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect()

def create_app():
    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )
    
    app.config.from_object(Config)
    
    init_security(app)
    csrf.init_app(app)

    db.init_app(app)
    migrate.init_app(app, db)

    from .routes.auth_routes import auth
    from .routes.event_routes import event
    from .routes.booking_routes import booking

    app.register_blueprint(auth)
    app.register_blueprint(event)
    app.register_blueprint(booking)

    return app