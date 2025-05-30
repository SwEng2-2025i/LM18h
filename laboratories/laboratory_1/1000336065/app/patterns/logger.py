import datetime
import threading

class AppLogger:
    _instance = None
    _lock = threading.Lock()
    _log_entries = []

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super(AppLogger, cls).__new__(cls)
                    cls._instance._log_entries = [] # Ensure logs are initialized
        return cls._instance

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            cls() # Initialize if not already
        return cls._instance

    def log_attempt(self, user_name: str, channel: str, message: str, status: str, priority: str, details: str = ""):
        timestamp = datetime.datetime.now().isoformat()
        log_entry = {
            "timestamp": timestamp,
            "user_name": user_name,
            "channel": channel,
            "message": message,
            "priority": priority,
            "status": status, # "SUCCESS" or "FAILURE"
            "details": details
        }
        self._log_entries.append(log_entry)
        print(f"LOG: {timestamp} - User: {user_name}, Channel: {channel}, Status: {status}, Priority: {priority}, Msg: '{message}' {details}")

    def get_logs(self, user_name: str = None):
        if user_name:
            return [entry for entry in self._log_entries if entry["user_name"] == user_name]
        return self._log_entries

    def clear_logs(self): # For testing or specific scenarios
        self._log_entries = []

# Example usage (not part of the class, just for testing)
if __name__ == '__main__':
    logger1 = AppLogger.get_instance()
    logger2 = AppLogger.get_instance()

    print(f"Logger1 is Logger2: {logger1 is logger2}")

    logger1.log_attempt("Alice", "email", "Test message 1", "SUCCESS", "high")
    logger2.log_attempt("Bob", "sms", "Test message 2", "FAILURE", "low", "Network error")

    print("\nAll logs:")
    for log in logger1.get_logs():
        print(log)

    print("\nAlice's logs:")
    for log in logger1.get_logs("Alice"):
        print(log)