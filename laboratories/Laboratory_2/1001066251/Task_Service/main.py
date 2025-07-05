from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

service_b = Flask(__name__)
CORS(service_b)

# Configuración de la base de datos
service_b.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
service_b.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(service_b)

# Modelo de la base de datos
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, nullable=False)

# Ruta para crear una tarea
@service_b.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or not data.get('title') or not data.get('user_id'):
        return jsonify({'error': 'Datos inválidos'}), 400

    # Verifica que el usuario exista antes de crear la tarea
    try:
        user_check = requests.get(f'http://localhost:5001/users/{data["user_id"]}')
        if user_check.status_code != 200:
            return jsonify({'error': 'ID de usuario inválido'}), 400
    except requests.exceptions.ConnectionError:
        return jsonify({'error': 'No se pudo conectar al servicio de usuarios'}), 500

    task = Task(title=data['title'], user_id=data['user_id'])
    db.session.add(task)
    db.session.commit()
    return jsonify({'id': task.id, 'title': task.title, 'user_id': task.user_id}), 201

# Ruta para obtener todas las tareas
@service_b.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': t.id, 'title': t.title, 'user_id': t.user_id} for t in tasks])

# Ruta para obtener una tarea específica (útil para la verificación)
@service_b.route('/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get(task_id)
    if task:
        return jsonify({'id': task.id, 'title': task.title, 'user_id': task.user_id})
    return jsonify({'error': 'Task not found'}), 404

# Ruta para borrar una tarea
@service_b.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if not task:
        return jsonify({'error': 'Task not found'}), 404

    # Las dos líneas cruciales para el borrado permanente
    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': f'Task with id {task_id} deleted.'}), 200

# Inicialización de la aplicación
if __name__ == '__main__':
    with service_b.app_context():
        db.create_all()
    service_b.run(port=5002)