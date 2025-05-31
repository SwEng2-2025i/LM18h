# Importa Flask y otros módulos necesarios
from flask import Flask
from controllers.users_controller import users_bp  # Blueprint para rutas de usuarios
from controllers.notifications_controller import notifications_bp  # Blueprint para notificaciones
from utils.swagger import swagger_ui  # Documentación Swagger
from flask_cors import CORS  # Permite solicitudes desde otros orígenes (CORS)

# Crea la aplicación Flask
app = Flask(__name__)

# Registra los blueprints de usuarios, notificaciones y documentación
app.register_blueprint(users_bp)
app.register_blueprint(notifications_bp)
app.register_blueprint(swagger_ui, url_prefix='/docs')  # Swagger accesible en /docs

# Habilita CORS para toda la aplicación
CORS(app)

# Ejecuta la aplicación en modo debug
if __name__ == '__main__':
    app.run(debug=True)
