from flask import jsonify, request
from notification_system.application.use_cases import UserUseCases, NotificationUseCases
from notification_system.application.dto import UserDTO, NotificationDTO


class UserController:
    def __init__(self, user_use_cases: UserUseCases):
        self.user_use_cases = user_use_cases
    
    def register_user(self):
        data = request.get_json()
        try:
            user = self.user_use_cases.register_user(
                name=data['name'],
                preferred_channel=data['preferred_channel'],
                available_channels=data['available_channels']
            )
            return jsonify(UserDTO.from_domain(user).to_dict()), 201
        except Exception as e:
            return jsonify({'error': str(e)}), 400
    
    def list_users(self):
        users = self.user_use_cases.list_users()
        return jsonify([UserDTO.from_domain(user).to_dict() for user in users])

class NotificationController:
    def __init__(self, notification_use_cases: NotificationUseCases):
        self.notification_use_cases = notification_use_cases
    
    def send_notification(self):
        data = request.get_json()
        try:
            notification = self.notification_use_cases.send_notification(
                user_name=data['user_name'],
                message=data['message'],
                priority=data.get('priority', 'medium')
            )
            return jsonify(NotificationDTO.from_domain(notification).to_dict())
        except Exception as e:
            return jsonify({'error': str(e)}), 400