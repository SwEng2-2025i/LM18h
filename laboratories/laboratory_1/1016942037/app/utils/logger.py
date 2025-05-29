# Clase Logger implementando el patrón Singleton.
# Se asegura que solo exista una única instancia compartida en toda la aplicación.
class Logger:
    _instance = None  # Variable de clase que guarda la única instancia de Logger

    def __new__(cls):
        # Sobrescribimos __new__ para controlar la creación de instancias
        if cls._instance is None:
            # Si no existe ninguna instancia, se crea una nueva
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = []  # Inicializa la lista de mensajes registrados
        return cls._instance  # Devuelve siempre la misma instancia

    def log(self, message):
        """
        Registra un mensaje tanto en consola como en la lista interna de logs.
        """
        print(message)           # Imprime el mensaje en consola
        self.logs.append(message)  # Guarda el mensaje en la lista interna

    def get_logs(self):
        """
        Retorna todos los mensajes registrados hasta el momento.
        """
        return self.logs
