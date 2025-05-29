from flask_restx import Namespace, Resource
from app.logger.logger import LoggerSingleton

# Definición del namespace para las operaciones relacionadas con los logs.
# Este namespace agrupa las rutas y operaciones de la API relacionadas con los registros de notificaciones.
api = Namespace('logs', description='Logs de notificaciones')

@api.route('')
class Logs(Resource):
    def get(self):
        """
        Obtiene todos los logs registrados en el sistema.
        Utiliza el LoggerSingleton para acceder al registro centralizado de logs.
        Retorna una lista con todas las entradas de log.
        """
        logger = LoggerSingleton()  # Obtiene la instancia única del logger
        return logger.get_logs()  # Devuelve los logs registrados