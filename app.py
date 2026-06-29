from routes.register import register_bp
from routes.auth import auth_bp
from flask import Flask
from models import db
import config

app = Flask(__name__)

app.config.from_object(config)

db.init_app(app)

app.register_blueprint(register_bp)

app.register_blueprint(auth_bp)

with app.app_context():
    db.create_all()


@app.route("/")
def home():
    return {
        "project": "TPM Authentication Server",
        "status": "Running"
    }


if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=True
    )