import threading

class Logger:
    _instance = None
    _lock = threading.Lock()

    # Implementación del patrón Singleton con seguridad de hilos (thread-safe)
    def __new__(cls):
        # Verifica si ya existe una instancia
        if not cls._instance:
            with cls._lock:  # Bloquea el acceso concurrente
                if not cls._instance:
                    # Si aún no se ha creado la instancia, la crea
                    cls._instance = super().__new__(cls)
                    cls._instance._initialize()  # Inicializa los atributos internos
        return cls._instance

    def _initialize(self):
        # Inicializa una lista para guardar los logs
        self.logs = []

    def log(self, message):
        # Agrega el mensaje a la lista de logs
        self.logs.append(message)
        # Muestra el mensaje por consola para mayor visibilidad
        print(f"LOG: {message}")


