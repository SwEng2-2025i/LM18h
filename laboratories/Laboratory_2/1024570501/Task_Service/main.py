from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

service_b = Flask(__name__)
CORS(service_b)

service_b.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
service_b.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(service_b)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

@service_b.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('user_id'):
        return jsonify({'error': 'Datos inválidos'}), 400
    
    try:
        # Convert user_id to integer
        user_id = int(data["user_id"])
    except (ValueError, TypeError):
        return jsonify({'error': 'ID de usuario inválido'}), 400
    
    try:
        user_check = requests.get(f'http://localhost:5001/users/{user_id}', timeout=2)
    except Exception as e:
        return jsonify({'error': f'Error de conexión: {str(e)}'}), 500

    if user_check.status_code != 200:
        return jsonify({'error': 'Usuario no existe'}), 400

    task = Task(title=data['title'], user_id=user_id)
    db.session.add(task)
    db.session.commit()
    
    # Return complete task information
    return jsonify({
        'id': task.id,
        'title': task.title,
        'user_id': task.user_id
    }), 201

@service_b.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': t.id, 'title': t.title, 'user_id': t.user_id} for t in tasks])

@service_b.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify({'id': task.id, 'title': task.title, 'user_id': task.user_id})
    return jsonify({'error': 'Task not found'}), 404

@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404
    
    # Delete the task and commit immediately
    db.session.delete(task)
    db.session.commit()
    
    # Verify deletion
    deleted_task = Task.query.get(task_id)
    if deleted_task:
        return jsonify({'error': 'Task deletion failed'}), 500
    
    return jsonify({'message': f'Task {task_id} deleted'}), 200

if __name__ == '__main__':
    with service_b.app_context():
        db.create_all()
    service_b.run(port=5002)
