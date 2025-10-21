from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from config import Config

# ------------------- Initialize Core Extensions -------------------
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()  # Handles DB migrations

# ------------------- App Factory -------------------
def create_app():
    """
    Application Factory Pattern:
    Initializes Flask app, extensions, blueprints, and login manager.
    """
    app = Flask(__name__)
    app.config.from_object(Config)

    # ------------------- Initialize Extensions -------------------
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'  # Redirect unauthorized users

    # ------------------- Register Blueprints -------------------
    from routes.authRoutes import auth
    from routes.patientRoute import patient_bp
    app.register_blueprint(patient_bp)
    app.register_blueprint(auth)

    # ------------------- Import Models -------------------
    from models import User  # Import models after db initialization

    # ------------------- Flask-Login User Loader -------------------
    @login_manager.user_loader
    def load_user(user_id):
        """
        Given a user ID, return the User object from the database.
        Required by Flask-Login to manage user sessions.
        """
        return User.query.get(int(user_id))

    # ------------------- Error Handlers -------------------
    @app.errorhandler(404)
    def page_not_found(e):
        return jsonify({"error": "Resource not found"}), 404

    @app.errorhandler(500)
    def internal_error(e):
        return jsonify({"error": "Internal server error"}), 500

    # ------------------- Default Route -------------------
    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Hospital Management System Backend!"})

    return app