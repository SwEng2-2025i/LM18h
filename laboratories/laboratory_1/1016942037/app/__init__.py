from flask import Flask #crear la instancia principal de la aplicación
from flasgger import Swagger #documentar automáticamente la API

# Función factory para crear y configurar la aplicación Flask
def create_app():
    app = Flask(__name__)  # Crea la instancia principal de Flask

    Swagger(app)  # Inicializa Swagger para habilitar la documentación en /apidocs

    # Importamos los blueprints de rutas para modularizar el sistema
    from app.routes.users import users_bp  # Blueprint de rutas relacionadas con usuarios
    from app.routes.notifications import notifications_bp  # Blueprint para enviar notificaciones

    # Registramos los blueprints en la app principal
    app.register_blueprint(users_bp)
    app.register_blueprint(notifications_bp)

    return app  # Retorna la app ya configurada
