"""
app/__init__.py — Flask application factory
"""
from flask import Flask
from .models.database import init_db


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "change-this-in-production"
    app.config["DATABASE"] = "freshness.db"
    app.config["UPLOAD_FOLDER"] = "app/static/uploads"
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024 * 1024  # 16 MB max upload

    # Initialise SQLite database
    init_db(app)

    # Register Blueprints (routes)
    from .routes.main import main_bp
    from .routes.predict import predict_bp
    from .routes.history import history_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(predict_bp)
    app.register_blueprint(history_bp)

    return app
