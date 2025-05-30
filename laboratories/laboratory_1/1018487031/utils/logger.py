from datetime import datetime
from typing import List

class Logger:
    """Singleton Logger for tracking system events"""
    
    _instance = None
    _logs = []
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def log(self, message: str, level: str = "INFO"):
        """Log a message with timestamp"""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_entry = f"[{timestamp}] [{level}] {message}"
        self._logs.append(log_entry)
        print(log_entry)  
    
    def get_logs(self) -> List[str]:
        """Get all logged messages"""
        return self._logs.copy()
    
    def clear_logs(self):
        """Clear all logs"""
        self._logs.clear()
    
    def error(self, message: str):
        """Log an error message"""
        self.log(message, "ERROR")
    
    def warning(self, message: str):
        """Log a warning message"""
        self.log(message, "WARNING")
    
    def debug(self, message: str):
        """Log a debug message"""
        self.log(message, "DEBUG")
