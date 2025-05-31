from config.app import create_app
from api.resources import (
    UsersResource,
    NotificationsResource,
    NotificationHistoryResource,
    NotificationStatsResource
)
from flask import jsonify

app, api = create_app()

# Ruta raíz
@app.route('/')
def index():
    return jsonify({
        'message': 'API de Notificaciones',
        'endpoints': {
            'users': '/users/',
            'send_notification': '/notifications/send',
            'notification_history': '/notifications/history',
            'notification_stats': '/notifications/stats'
        }
    })

# Registrar recursos
api.add_resource(UsersResource, '/users/')
api.add_resource(NotificationsResource, '/notifications/send')
api.add_resource(NotificationHistoryResource, '/notifications/history')
api.add_resource(NotificationStatsResource, '/notifications/stats')

if __name__ == '__main__':
    app.run(debug=True) 