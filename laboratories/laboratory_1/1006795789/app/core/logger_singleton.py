# logger_singleton.py
# Módulo que implementa un logger Singleton para registrar eventos de notificación.

import threading

class Logger:
    """
    Logger Singleton para registrar logs de notificaciones.
    Garantiza que solo exista una instancia y es seguro para hilos.
    """
    _instance = None
    _lock = threading.Lock()  # Lock para asegurar acceso concurrente seguro

    def __new__(cls):
        """
        Implementación del patrón Singleton.
        Si no existe una instancia, la crea; si existe, la retorna.
        """
        with cls._lock:
            if cls._instance is None:
                cls._instance = super().__new__(cls)
                cls._instance.logs = []  # Lista para almacenar los logs
        return cls._instance

    def log(self, user_name, channel, message, status):
        """
        Registra un evento de notificación en la lista de logs y lo imprime por consola.
        :param user_name: Nombre del usuario
        :param channel: Canal utilizado
        :param message: Mensaje enviado
        :param status: Estado del envío (attempt, success, failed)
        """
        entry = f"[{status.upper()}] user={user_name} channel={channel} msg=\"{message}\""
        print(entry)
        self.logs.append(entry)

    def get_logs(self):
        """
        Devuelve una copia de la lista de logs registrados.
        :return: Lista de logs
        """
        return list(self.logs)
