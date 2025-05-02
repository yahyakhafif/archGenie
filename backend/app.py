from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from config.db import init_db
from middleware.errorHandler import register_error_handlers
from routes.auth import auth_bp
from routes.users import users_bp
from routes.styles import styles_bp

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)
    app.url_map.strict_slashes = False

    CORS(app)

    if test_config:
        app.config.update(test_config)

    init_db(app)

    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(users_bp, url_prefix='/api/users')
    app.register_blueprint(styles_bp, url_prefix='/api/styles')

    register_error_handlers(app)

    return app


app = create_app()
