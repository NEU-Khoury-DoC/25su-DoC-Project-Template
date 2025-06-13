from flask import Blueprint, jsonify, current_app, make_response, request, Flask
from dotenv import load_dotenv
import os
import logging
from logging.handlers import RotatingFileHandler

from backend.db_connection import db
from backend.routes.mep_routes.mep_routes import meps
from backend.routes.users_routes.users_routes import users
from backend.routes.party_routes.party_routes import parties
from backend.routes.recommender_routes.recommendation_routes import recommendation
from backend.routes.watchlist_routes.watchlist_routes import watchlists
from backend.routes.recommender_routes.recommendation_bp_routes import recommender_bp
from backend.routes.logreg_routes.logreg_routes import logreg_bp



def create_app():
    app = Flask(__name__)

    # Configure logging
    # Create logs directory if it doesn't exist
    setup_logging(app)

    # Load environment variables
    # This function reads all the values from inside
    # the .env file (in the parent folder) so they
    # are available in this file.  See the MySQL setup
    # commands below to see how they're being used.
    load_dotenv()

    # secret key that will be used for securely signing the session
    # cookie and can be used for any other security related needs by
    # extensions or your application
    # app.config['SECRET_KEY'] = 'someCrazyS3cR3T!Key.!'
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

    # # these are for the DB object to be able to connect to MySQL.
    # app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config["MYSQL_DATABASE_USER"] = os.getenv("DB_USER").strip()
    app.config["MYSQL_DATABASE_PASSWORD"] = os.getenv("MYSQL_ROOT_PASSWORD").strip()
    app.config["MYSQL_DATABASE_HOST"] = os.getenv("DB_HOST").strip()
    app.config["MYSQL_DATABASE_PORT"] = int(os.getenv("DB_PORT").strip())
    app.config["MYSQL_DATABASE_DB"] = os.getenv("DB_NAME").strip()

    # Initialize the database object with the settings above.
    app.logger.info("current_app(): starting the database connection")
    db.init_app(app)

    # Route registering
    app.logger.info("create_app(): registering blueprints with Flask app object.")
    app.register_blueprint(meps, url_prefix="/m")
    app.register_blueprint(users, url_prefix="/u")
    app.register_blueprint(parties, url_prefix="/p")
    app.register_blueprint(recommendation, url_prefix='/r')
    app.register_blueprint(watchlists, url_prefix='/w')
    app.register_blueprint(recommender_bp, url_prefix='/b')
    app.register_blueprint(logreg_bp, url_prefix='/l')


    # Don't forget to return the app object
    return app

def setup_logging(app):
    """
    Configure logging for the Flask application in both files and console (Docker Desktop for this project)
    
    Args:
        app: Flask application instance to configure logging for
    """
    if not os.path.exists('logs'):
        os.mkdir('logs')

    ## Set up FILE HANDLER for all levels
    file_handler = RotatingFileHandler(
        'logs/api.log',
        maxBytes=10240,
        backupCount=10
    )
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    
    # Make sure we are capturing all levels of logging into the log files. 
    file_handler.setLevel(logging.DEBUG)  # Capture all levels in file
    app.logger.addHandler(file_handler)

    ## Set up CONSOLE HANDLER for all levels
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s'
    ))
    # Debug level capture makes sure that all log levels are captured
    console_handler.setLevel(logging.DEBUG)
    app.logger.addHandler(console_handler)

    # Set the base logging level to DEBUG to capture everything
    app.logger.setLevel(logging.DEBUG)
    app.logger.info('API startup')
