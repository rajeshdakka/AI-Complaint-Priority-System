# Step 2: Update app/__init__.py

from flask import Flask
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import os

bcrypt = Bcrypt()


def create_app():
    load_dotenv()

    app = Flask(
        __name__,
        template_folder="../templates",
        static_folder="../static"
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    app.config["UPLOAD_FOLDER"] = "static/uploads"

    os.makedirs(
        app.config["UPLOAD_FOLDER"],
        exist_ok=True
    )

    bcrypt.init_app(app)

    # Import Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.report_routes import report_bp
    from app.routes.admin_routes import admin_bp
    from app.routes.pdf_routes import pdf_bp   # NEW

    # Register Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(report_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(pdf_bp)
    
    from init_db import create_tables

    create_tables()

    return app