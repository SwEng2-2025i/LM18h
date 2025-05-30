class Logger: # singleton para registrar mensajes de la aplicación web
    _instance = None

    def __init__(self):
        if Logger._instance is not None:
            raise Exception("Use get_instance()")
        self.logs = []

    @staticmethod
    def get_instance():
        if Logger._instance is None:
            Logger._instance = Logger()
        return Logger._instance

    def log(self, message: str):
        print(f"LOG: {message}")
        self.logs.append(message)
