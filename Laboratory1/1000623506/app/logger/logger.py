import threading
from datetime import datetime

# Clase LoggerSingleton implementa un patrón Singleton para gestionar un registro centralizado de logs.
# Garantiza que solo exista una instancia de la clase, incluso en entornos concurrentes.
class LoggerSingleton:
    _instance = None  # Variable de clase para almacenar la única instancia de LoggerSingleton
    _lock = threading.Lock()  # Lock para garantizar seguridad en entornos multithreading

    def __new__(cls):
        # Método especial para controlar la creación de la instancia única (Singleton)
        if not cls._instance:
            with cls._lock:  # Bloquea el acceso concurrente
                if not cls._instance:  # Verifica nuevamente dentro del lock
                    cls._instance = super().__new__(cls)  # Crea la instancia
                    cls._instance.logs = []  # Inicializa la lista de logs
        return cls._instance

    def log(self, user_name, channel, message, status):
        # Registra un nuevo log con información del usuario, canal, mensaje y estado.
        # Incluye una marca de tiempo para cada entrada.
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        entry = {
            "timestamp": timestamp,
            "user": user_name,
            "channel": channel,
            "message": message,
            "status": status  # Puede ser "success" o "fail"
        }
        self.logs.append(entry)  # Agrega la entrada al registro
        print(f"[LOG] {timestamp} - Usuario: {user_name}, Canal: {channel}, Estado: {status}")

    def get_logs(self):
        # Devuelve todos los logs registrados.
        return self.logs