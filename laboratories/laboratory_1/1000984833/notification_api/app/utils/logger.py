# app/utils/logger.py

import datetime

class NotificationLogger:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NotificationLogger, cls).__new__(cls)
            cls._instance.logs = []
        return cls._instance

    def log(self, user_name, channel, status):
        entry = {
            "timestamp": datetime.datetime.now().isoformat(),
            "user": user_name,
            "channel": channel,
            "status": status
        }
        print(f"[LOG] {entry}")
        self._instance.logs.append(entry)

    def get_logs(self):
        return self._instance.logs
