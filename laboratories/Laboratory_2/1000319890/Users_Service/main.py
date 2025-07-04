from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 👈 Agregado

service_a = Flask(__name__)
CORS(service_a)  # 👈 Habilita CORS

service_a.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
service_a.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(service_a)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

@service_a.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'name' not in data or not data['name'].strip():
        return jsonify({'error': 'El nombre es requerido'}), 400

    user = User(name=data['name'].strip())
    db.session.add(user)
    db.session.commit()
    print({'id': user.id, 'name': user.name})
    return jsonify({'id': user.id, 'name': user.name}), 201

@service_a.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])

@service_a.route('/users/cleanup', methods=['DELETE'])
def cleanup_users():
    """Delete all users - used for test cleanup"""
    try:
        num_deleted = User.query.delete()
        db.session.commit()
        return jsonify({'message': f'Deleted {num_deleted} users'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@service_a.route('/users/cleanup-specific', methods=['DELETE'])
def cleanup_specific_users():
    """Delete specific users by IDs - used for test cleanup"""
    try:
        data = request.get_json()
        if not data or 'user_ids' not in data:
            return jsonify({'error': 'user_ids list is required'}), 400
        
        user_ids = data['user_ids']
        if not isinstance(user_ids, list):
            return jsonify({'error': 'user_ids must be a list'}), 400
        
        deleted_count = 0
        for user_id in user_ids:
            user = User.query.get(user_id)
            if user:
                db.session.delete(user)
                deleted_count += 1
        
        db.session.commit()
        return jsonify({'message': f'Deleted {deleted_count} specific users'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@service_a.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'name': user.name})
    return jsonify({'error': 'User not found'}), 404

@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return jsonify({'message': f'User {user_id} deleted successfully'}), 200
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    with service_a.app_context():
        db.create_all()
    service_a.run(port=5001)
