import os
from app import create_app
from app.extensions import db
from seed import run_seed

app = create_app()

DB_PATH = os.path.join(
    os.path.dirname(__file__),
    "instance",
    "site.db"
)

with app.app_context():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)

    db.create_all()
    run_seed(app)