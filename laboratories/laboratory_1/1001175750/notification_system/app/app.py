from flask import Flask
from flasgger import Swagger
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from app.routes.user import users_bp
from app.routes.notifications import notifications_bp 
import sys
import os

# Add parent directory to sys.path to ensure imports work correctly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

def create_app():
    app = Flask(__name__)

    # Initialize Swagger for API documentation
    Swagger(app)

    # Initialize Flask-Limiter to rate limit requests (5 per minute per IP)
    Limiter(get_remote_address, app=app, default_limits=["5 per minute"])

    # Register user routes blueprint
    app.register_blueprint(users_bp)

    # Register notifications routes blueprint
    app.register_blueprint(notifications_bp)

    return app

if __name__ == '__main__':
    # Create the app and run it in debug mode
    app = create_app()
    app.run(debug=True)
