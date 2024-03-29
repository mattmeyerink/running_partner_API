"""Contains the create_app function to Initialize and instance of the app."""
import flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
from flask_jwt_extended import JWTManager
from config import Config


# Create instances of the db
db = SQLAlchemy()

def create_app():
    """Creates an instance of the application."""
    # Initialize the app
    app = flask.Flask(__name__)
    
    # Allow cross origin requests while API and App still operating on local machine
    CORS(app)
    
    # Add the config settings
    app.config.from_object(Config)

    # Link the db to the app
    db.init_app(app)

    # Set up JWT
    jwt = JWTManager(app)

    # Register the blueprints
    from .blueprints.authentication import auth_bp
    app.register_blueprint(auth_bp)

    from .blueprints.training_plans import training_bp
    app.register_blueprint(training_bp)
    
    from .blueprints.runs import runs_bp
    app.register_blueprint(runs_bp)

    from .blueprints.weather import weather_bp
    app.register_blueprint(weather_bp)

    # Create the db
    with app.app_context():
        db.create_all()

    return app
