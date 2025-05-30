class Logger:
    """
    Singleton Logger Class
    This class implements a singleton pattern for logging messages. 
    It ensures that only one instance of the logger exists throughout the application.
    """
    _instance = None
    
    def __new__(cls):
        if cls._instance is None: 
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance

    def log(self, message):
        print(f"[LOG] {message}")
