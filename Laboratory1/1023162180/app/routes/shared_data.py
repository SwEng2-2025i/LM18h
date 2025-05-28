from flask_restx import Namespace, Resource, fields
from app.models.user import User

# Esta lista actuará como una base de datos en memoria.
# Aquí se almacenan todos los usuarios registrados durante la ejecución de la aplicación.
# Dado que no se utiliza una base de datos real, los datos se pierden al reiniciar el servidor.
users = []
