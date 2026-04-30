"""
__init__.py — Flask application factory
Author: Siddhi Singh (Full-Stack Lead)
"""
import os
from flask import Flask
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()


def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('SECRET_KEY', 'freshvision-dev-secret-change-in-prod')

    # Init extensions
    bcrypt.init_app(app)

    # Init DB
    from app.models.database import init_db, close_db
    init_db(app)
    app.teardown_appcontext(close_db)

    # Register blueprints
    from app.routes.main    import main_bp
    from app.routes.auth    import auth_bp
    from app.routes.predict import predict_bp
    from app.routes.history import history_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp,    url_prefix='/auth')
    app.register_blueprint(predict_bp)
    app.register_blueprint(history_bp)

    return app
