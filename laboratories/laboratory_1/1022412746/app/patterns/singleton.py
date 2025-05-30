# singleton.py
import threading

class LoggerSingleton:
    _instance = None
    _lock = threading.Lock()

    def __init__(self):
        if LoggerSingleton._instance is not None:
            raise Exception("Este es un singleton, usa get_instance()")
        self.logs = []

    @classmethod
    def get_instance(cls):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = LoggerSingleton()
        return cls._instance

    def log(self, message):
        # Guarda el log en memoria y también lo imprime en consola
        self.logs.append(message)
        print(f"[LOG]: {message}")
