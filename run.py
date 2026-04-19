from app import create_app
from flask_migrate import upgrade
from seed import run_seed
import os

app = create_app()

if __name__ == "__main__":
    debug = os.getenv("FLASK_ENV") != "production"
    app.run(debug=debug)