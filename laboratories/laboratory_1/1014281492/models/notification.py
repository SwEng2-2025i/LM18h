class Notification:
    def __init__(self, user_name, message, priority="normal"):
        self.user_name = user_name
        self.message = message
        self.priority = priority
        self.status = "pending"
        self.delivery_attempts = []

    def add_delivery_attempt(self, channel, success):
        self.delivery_attempts.append({
            "channel": channel,
            "success": success
        })
        if success:
            self.status = "delivered"

    def to_dict(self):
        return {
            "user_name": self.user_name,
            "message": self.message,
            "priority": self.priority,
            "status": self.status,
            "delivery_attempts": self.delivery_attempts
        } 