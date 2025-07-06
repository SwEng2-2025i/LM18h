from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import requests

servicio_tareas = Flask(__name__)
CORS(servicio_tareas)

servicio_tareas.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tareas.db'
servicio_tareas.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(servicio_tareas)

class Tarea(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    usuario_id = db.Column(db.Integer, nullable=False)

@servicio_tareas.route('/tareas', methods=['POST'])
def crear_tarea():
    datos = request.get_json()
    if not datos or not datos.get('titulo') or not datos.get('usuario_id'):
        return jsonify({'error': 'Datos inválidos'}), 400
    try:
        verificacion_usuario = requests.get(f'http://localhost:5001/usuarios/{datos["usuario_id"]}')
    except Exception as e:
        return jsonify({'error': f'Error de conexión al verificar usuario: {str(e)}'}), 500

    if verificacion_usuario.status_code != 200:
        return jsonify({'error': 'ID de usuario inválido'}), 400

    nueva_tarea = Tarea(titulo=datos['titulo'], usuario_id=datos['usuario_id'])
    db.session.add(nueva_tarea)
    db.session.commit()
    return jsonify({'id': nueva_tarea.id, 'titulo': nueva_tarea.titulo, 'usuario_id': nueva_tarea.usuario_id}), 201

@servicio_tareas.route('/tareas', methods=['GET'])
def obtener_tareas():
    tareas = Tarea.query.all()
    return jsonify([{'id': t.id, 'titulo': t.titulo, 'usuario_id': t.usuario_id} for t in tareas])

@servicio_tareas.route('/tareas/<int:tarea_id>', methods=['DELETE'])
def eliminar_tarea(tarea_id):
    tarea = Tarea.query.get(tarea_id)
    if tarea is None:
        return jsonify({'error': 'Tarea no encontrada'}), 404
    
    db.session.delete(tarea)
    db.session.commit()
    return jsonify({'mensaje': f'Tarea {tarea_id} eliminada'}), 200

if __name__ == '__main__':
    with servicio_tareas.app_context():
        db.create_all()
    servicio_tareas.run(port=5002)
