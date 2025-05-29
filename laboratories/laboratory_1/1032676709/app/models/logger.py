class Logger:
    _instance = None # Variable de clase para almacenar la única instancia (Singleton)

    def __new__(cls):
        # Crea una nueva instancia solo si no existe
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = [] # Inicializa la lista de logs
        return cls._instance

    def log(self, message):
        print(message) # Imprime el mensaje en consola
        self.logs.append(message) # Guarda el mensaje en la lista de logs