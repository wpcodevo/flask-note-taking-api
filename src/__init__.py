from src.notes_routes import get_note, get_notes, create_note, update_note, delete_note
from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
import os
from src.models import db, migrate
import src.utils as utils


def handle_error(error):
    response = {
        'status': 'error',
        'message': str(error)
    }
    return response, 500


def create_app():
    app = Flask(__name__, instance_relative_config=True)

    load_dotenv()  # Load environment variables from .env file
    database_uri = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_DATABASE_URI'] = database_uri

    db.app = app
    db.init_app(app)

    migrate.init_app(app, db)
    utils.csrf.init_app(app)

    @app.get('/api/healthchecker')
    def healthchecker():
        return {"status": "success", "message": "Build RESTful API with Flask and SQLAlchemy"}

    app.route('/api/notes', strict_slashes=False, methods=['GET'])(get_notes)
    app.route('/api/notes', strict_slashes=False,
              methods=['POST'])(create_note)
    app.route('/api/notes/<string:note_id>',
              methods=['PATCH'])(update_note)
    app.route('/api/notes/<string:note_id>', methods=['GET'])(get_note)
    app.route('/api/notes/<string:note_id>', methods=['DELETE'])(delete_note)

    CORS(app, resources={r"/*": {"origins": "http://localhost:3000",
                                 "methods": ["GET", "POST", "PATCH", "DELETE"],
                                 "supports_credentials": True}})

    app.register_error_handler(Exception, handle_error)

    @app.errorhandler(404)
    def handle_not_found_error(e):
        response = {
            'status': 'fail',
            'message': f"route: '{request.path}' not found on this server"
        }
        return response, 404

    return app
