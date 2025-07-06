from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests
import sys
import os

# Ruta absoluta al directorio raíz (1000256311)
BASE_DIRECTION = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Agregar la carpeta "Test" al path
sys.path.append(os.path.join(BASE_DIRECTION, "Test"))
sys.path.append(os.path.join(BASE_DIRECTION, "Test/Logs"))
from LogSaver import Logger
import Logs

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
        Logger.add_to_log("warn", f"Datos inválidos recibidos: {data}")
        return jsonify({'error': 'Datos inválidos'}), 400
    try:
        user_check = requests.get(f'http://localhost:5001/users/{data["user_id"]}')
    except Exception as e:
        Logger.add_to_log("error", f"Fallo al verificar usuario remoto: {str(e)}")
        return jsonify({'error': f'Error de conexión al verificar usuario: {str(e)}'}), 500

    if user_check.status_code != 200:
        Logger.add_to_log("warn", f"ID de usuario inválido: {data['user_id']}")
        return jsonify({'error': 'ID de usuario inválido'}), 400

    task = Task(title=data['title'], user_id=data['user_id'])
    db.session.add(task)
    db.session.commit()
    Logger.add_to_log("info", f"Tarea creada: título='{task.title}', usuario_id={task.user_id}")
    return jsonify({'id': task.id, 'title': task.title, 'user_id': task.user_id}), 201

@service_b.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    Logger.add_to_log("info", f"Tareas obtenidas: {len(tasks)}")
    return jsonify([{'id': t.id, 'title': t.title, 'user_id': t.user_id} for t in tasks])

@service_b.route('/tasks/<id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    db.session.delete(task)
    Logger.add_to_log("info", f"Tarea eliminada: ID={id}")
    db.session.commit()
    return jsonify({'message': 'Tarea eliminada'}), 200

if __name__ == '__main__':
    with service_b.app_context():
        db.create_all()
    service_b.run(port=5002)
