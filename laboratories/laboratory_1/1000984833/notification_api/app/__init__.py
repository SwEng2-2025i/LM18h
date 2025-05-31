from flask import Flask
from flasgger import Swagger
from app.routes.user_routes import user_bp
from app.routes.notification_routes import notification_bp

def create_app():
    app = Flask(__name__)

    # Configurar Swagger
    swagger = Swagger(app)

    app.register_blueprint(user_bp)
    app.register_blueprint(notification_bp)

    @app.route('/')
    def home():
        return "Running"

    return app
