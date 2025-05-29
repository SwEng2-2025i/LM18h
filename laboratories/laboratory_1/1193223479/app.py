from flask import Flask, request, jsonify
from notification_chain import build_notification_chain
from strategies.factory import get_strategy

app = Flask(__name__)
users = {}
handler_chain = build_notification_chain()

@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    name = data.get('name')
    preferred = data.get('preferred_channel')
    available = data.get('available_channels')

    if not name or not preferred or not available:
        return jsonify({'error': 'Missing required fields'}), 400

    users[name] = {
        'preferred': preferred,
        'available': available
    }

    return jsonify({'message': f'User {name} registered successfully'}), 201

@app.route('/users', methods=['GET'])
def list_users():
    response = []
    for name, info in users.items():
        response.append({
            'name': name,
            'preferred_channel': info['preferred'],
            'available_channels': info['available']
        })
    return jsonify(response), 200

@app.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json()
    user_name = data.get('user_name')
    message = data.get('message')
    priority = data.get('priority', 'normal')

    user = users.get(user_name)
    if not user:
        return jsonify({'error': f'User {user_name} not found'}), 404

    # Use Strategy Pattern to format message
    strategy = get_strategy(priority)
    formatted_message = strategy.format_message(message)

    # Send message using the chain
    success = handler_chain.handle(user, formatted_message)

    if success:
        return jsonify({'message': 'Notification sent successfully'}), 200
    else:
        return jsonify({'error': 'All delivery attempts failed'}), 500

if __name__ == '__main__':
    app.run(debug=True)
