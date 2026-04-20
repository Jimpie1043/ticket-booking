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
            "site.db"
        )
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Détection d'environnement (prod/développement)
    ENV = os.getenv("FLASK_ENV", "development")
    IS_PROD = ENV == "production"

    # Sécurité
    SESSION_COOKIE_SAMESITE = "Lax" # Liens fonctionnent, mais seulement avec GET / HEAD, pas POST (protection CSRF)
    # SAMESITE = "Strict" briserait certaines fonctionnalités, ex -> Un utilisateur reçoit un lien de booking mais quand il clique
    # dessus, il n'est plus conencté à son compte.
    
    SESSION_COOKIE_HTTPONLY = True # Cookies inaccessibles sur JS dans le browser (protection XSS)
    SESSION_COOKIE_SECURE = IS_PROD # True en production / False en développement

    FORCE_HTTPS = IS_PROD # True en production / False en développement