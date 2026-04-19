import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "devkey")

    SQLALCHEMY_DATABASE_URI = (
        "sqlite:///" + os.path.join(
            os.path.abspath(os.path.dirname(__file__)),
            "..",
            "instance",
            "site_v2.db"
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Détection d'environnement (prod/développement)
    ENV = os.getenv("FLASK_ENV", "development")
    IS_PROD = ENV == "production"

    # Sécurité
    SESSION_COOKIE_SAMESITE = "Lax"
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = IS_PROD

    FORCE_HTTPS = IS_PROD