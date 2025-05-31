# Almacenamiento en memoria para usuarios y notificaciones
users = []
notifications = []
notification_history = []

def add_user(user):
    users.append(user)
    return user

def get_user_by_name(name):
    return next((u for u in users if u["name"] == name), None)

def add_notification(notification):
    notifications.append(notification)
    notification_history.append(notification)
    return notification

def get_all_users():
    return users

def get_all_notifications():
    return notifications

def get_notification_history():
    return notification_history

def get_notification_stats():
    total_notifications = len(notification_history)
    successful_notifications = sum(1 for n in notification_history if n["result"]["success"])
    
    return {
        "total_notifications": total_notifications,
        "successful_notifications": successful_notifications,
        "failed_notifications": total_notifications - successful_notifications,
        "success_rate": (successful_notifications / total_notifications * 100) if total_notifications > 0 else 0,
        "pattern_type": "Strategy and Chain of Responsibility Patterns"
    } 