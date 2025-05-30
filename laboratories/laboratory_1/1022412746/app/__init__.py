from flask import Flask

def create_app():
    # Crear instancia de la app Flask
    app = Flask(__name__)

    # Importar y registrar los blueprints de rutas
    from app.routes.users import users_bp
    from app.routes.notifications import notifications_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(notifications_bp)

    return app
