from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS  # 👈 Agregado
import sys
import os

# Ruta absoluta al directorio raíz (1000256311)
BASE_DIRECTION = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

# Agregar la carpeta "Test" al path
sys.path.append(os.path.join(BASE_DIRECTION, "Test"))
sys.path.append(os.path.join(BASE_DIRECTION, "Test/Logs"))
from LogSaver import Logger
import Logs
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
        Logger.add_to_log("warn", "Intento de creación de usuario sin nombre válido.")
        return jsonify({'error': 'El nombre es requerido'}), 400

    user = User(name=data['name'].strip())
    db.session.add(user)
    db.session.commit()
    print({'id': user.id, 'name': user.name})
    Logger.add_to_log("info", f"Usuario creado: ID={user.id}, Nombre={user.name}")
    return jsonify({'id': user.id, 'name': user.name}), 201

@service_a.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({'id': user.id, 'name': user.name})
    Logger.add_to_log("warn", f"Usuario con ID={user_id} no encontrado.")
    return jsonify({'error': 'User not found'}), 404

@service_a.route('/users', methods=['GET'])
def list_users():
    users = User.query.all()
    return jsonify([{'id': user.id, 'name': user.name} for user in users])

@service_a.route('/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        Logger.add_to_log("info", f"Usuario eliminado: ID={user.id}")
        return jsonify({'result': 'deleted'})
    Logger.add_to_log("warn", f"Intento de eliminar usuario inexistente: ID={user_id}")
    return jsonify({'error': 'User not found'}), 404

if __name__ == '__main__':
    print("Servicio A iniciado.")
    Logger.add_to_log("info", "Servicio A iniciado.")
    with service_a.app_context():
        db.create_all()
    service_a.run(port=5001)
