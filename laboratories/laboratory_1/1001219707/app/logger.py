import datetime

class Logger:
    """
    Clase Logger que sigue el patrón Singleton.
    Se asegura de que solo exista una única instancia durante toda la ejecución.
    Registra todos los intentos de envío de notificaciones.
    """
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            # Se crea la única instancia y se inicializa la lista de logs
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, message):
        """
        Registra un mensaje con marca de tiempo y lo imprime.
        """
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        full_message = f"[{timestamp}] {message}"
        self.logs.append(full_message)
        print(full_message)

    def get_logs(self):
        """
        Retorna la lista de logs registrados.
        """
        return self.logs