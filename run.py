from app import create_app
from dotenv import load_dotenv
import os

from flask_migrate import upgrade

from seed import run_seed

load_dotenv()

app = create_app()

with app.app_context():
    # Migration de données
    upgrade()

    # Seeding de la db
    run_seed(app)

if __name__ == "__main__":
    debug = os.getenv("FLASK_ENV") != "production"
    app.run(debug=debug)