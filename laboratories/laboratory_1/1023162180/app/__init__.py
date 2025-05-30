from flask import Flask
from flask_restx import Api
from app.routes.users import api as users_ns
from app.routes.notifications import api as notifications_ns

# Esta función crea y configura la aplicación Flask
def create_app():
    app = Flask(__name__)  # Se instancia la aplicación Flask

    # Se configura la extensión Flask-RESTX para documentar y estructurar la API REST.
    # Se define un título, una descripción y la ruta donde estará la documentación Swagger (/docs)
    api = Api(
        app,
        title="Notification REST-API",
        description="Simulated notification system with fallback channels",
        doc="/docs"
    )

    # Se agregan los espacios de nombres (namespaces), que organizan los endpoints:
    # - users_ns contiene los endpoints relacionados con los usuarios (/users)
    # - notifications_ns contiene los endpoints para enviar notificaciones (/notifications)
    api.add_namespace(users_ns)         # Registra el namespace de usuarios en la API
    api.add_namespace(notifications_ns) # Registra el namespace de notificaciones en la API

    return app  # Se retorna la aplicación ya configurada
