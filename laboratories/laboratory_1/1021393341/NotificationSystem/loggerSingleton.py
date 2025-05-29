import datetime

class Logger:
    _instance = None  

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
            cls._instance.logs = []  
        return cls._instance

    def log(self, user, channel, status, message):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": user,
            "channel": channel,
            "status": status,  
            "message": message
        }
        print(f"LOG: {entry}")
        self.logs.append(entry)

    def get_logs(self):
        return self.logs
