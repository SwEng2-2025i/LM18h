import datetime

class Logger:
    _instance = None # Singleton instance placeholder

    def __new__(cls):
        # Ensure only one instance of Logger exists (Singleton pattern)
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance
    
    def log(self, message):
        # Create a timestamped log entry
        timestamp = datetime.datetime.now().isoformat()
        log_entry = f"[{timestamp}] {message}"
        print(log_entry)  
        self.logs.append(log_entry)

    def get_logs(self):
        return self.logs 