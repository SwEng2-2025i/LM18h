from flask import Flask, request, jsonify
from flasgger import Swagger
from channels.factory import ChannelFactory

app = Flask(__name__)
Swagger(app)

# In-memory user store
users = []

# Endpoint to register a new user
@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json(force=True)
    user = {
        'name': data['name'],
        'preferred': [data['preferred_channel']],
        'available': data['available_channels']
    }
    users.append(user)
    return jsonify({'message': 'User registered'}), 200

# Endpoint to list all users
@app.route('/users', methods=['GET'])
def list_users():
    return jsonify(users), 200

# Endpoint to send a notification
@app.route('/notifications/send', methods=['POST'])
def send_notification():
    data = request.get_json(force=True)
    user = next((u for u in users if u['name'] == data['user_name']), None)
    if not user:
        return jsonify({'error': 'User not found'}), 404

    channels = [*user['preferred'], *[c for c in user['available'] if c not in user['preferred']]]
    chain = None
    prev = None
    for ch in channels:
        node = ChannelFactory.create(ch)
        if chain is None:
            chain = node
        else:
            prev.set_next(node)
        prev = node

    success, result = chain.handle(user, data['message'], data['priority'])
    status = 'success' if success else 'failure'
    return jsonify({'status': status, 'detail': result}), 200

if __name__ == '__main__':
    app.run(debug=True)
