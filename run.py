from app import create_app
from app.extensions import db
from seed import run_seed
import os

app = create_app()

with app.app_context():
    db.drop_all()
    db.create_all()

    run_seed()

if __name__ == "__main__":
    debug = os.getenv("FLASK_ENV") != "production"
    app.run(debug=debug)