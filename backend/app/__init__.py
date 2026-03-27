from flask import Flask
from .db import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    CORS(
        app,
        resources={r"/api/*": {"origins": "http://localhost:5173"}},
        supports_credentials=True
    )

    # Import Blueprints
    from app.routes.auth_routes import auth_bp
    from app.routes.onboarding_routes import onboarding_bp
    from app.routes.dashboard_routes import dashboard_bp
    from app.routes.application_routes import applications_bp
    from app.routes.admin import admin_bp

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(applications_bp, url_prefix="/api/applications")
    app.register_blueprint(onboarding_bp, url_prefix="/api/onboarding")
    app.register_blueprint(dashboard_bp, url_prefix="/api/dashboard")
    app.register_blueprint(admin_bp, url_prefix="/api/admin")

    @app.route("/")
    def home():
        return "Agentic Banking Backend Running Successfully"

    return app