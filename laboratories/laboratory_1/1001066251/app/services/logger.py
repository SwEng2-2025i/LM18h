class LoggerSingleton:
    _instance = None  # Variable de clase para mantener la única instancia

    def __new__(cls):
        # Si no existe una instancia, se crea
        if cls._instance is None:
            cls._instance = super(LoggerSingleton, cls).__new__(cls)
        return cls._instance  # Siempre devuelve la misma instancia

    def log(self, message):
        # Método para imprimir mensajes de log
        print(f"[LOG]: {message}")
