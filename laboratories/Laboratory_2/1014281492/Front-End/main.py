from flask import Flask, render_template_string

frontend = Flask(__name__)

HTML = '''
<!DOCTYPE html>
<html lang="es">
<head>
  <meta charset="UTF-8">
  <title>Laboratorio de Integración</title>
  <style>
    * {
      box-sizing: border-box;
    }
    body {
      font-family: 'Segoe UI', sans-serif;
      background: #f0f2f5;
      margin: 0;
      padding: 40px;
      display: flex;
      flex-direction: column;
      align-items: center;
    }
    h1 {
      margin-bottom: 30px;
      color: #333;
    }
    .card {
      background: white;
      border-radius: 10px;
      padding: 20px 30px;
      margin-bottom: 30px;
      width: 100%;
      max-width: 500px;
      box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    }
    label {
      font-weight: bold;
      display: block;
      margin-top: 15px;
    }
    input {
      width: 100%;
      padding: 10px;
      margin-top: 5px;
      border-radius: 5px;
      border: 1px solid #ccc;
    }
    button {
      width: 100%;
      margin-top: 20px;
      padding: 10px;
      background: #4CAF50;
      color: white;
      font-size: 16px;
      border: none;
      border-radius: 5px;
      cursor: pointer;
      transition: background 0.3s;
    }
    button:hover {
      background: #45a049;
    }
    .result {
      margin-top: 10px;
      color: green;
      font-weight: bold;
    }
    .error {
      margin-top: 10px;
      color: red;
      font-weight: bold;
    }
    ul {
      padding-left: 20px;
      margin-top: 10px;
    }
    li {
      margin-bottom: 6px;
    }
    .delete-section {
      background: #fff3cd;
      border: 1px solid #ffeaa7;
    }
    .delete-section button {
      background: #dc3545;
    }
    .delete-section button:hover {
      background: #c82333;
    }
  </style>
</head>
<body>
  <h1>🔧 Laboratorio de Integración</h1>

  <div class="card">
    <h2>👤 Crear Usuario</h2>
    <label>Nombre:</label>
    <input id='nombre_usuario' placeholder='Ej: Ana'>
    <button onclick='crearUsuario()'>Crear Usuario</button>
    <div id="resultado_usuario" class="result"></div>
  </div>

  <div class="card">
    <h2>📝 Crear Tarea</h2>
    <label>ID de Usuario:</label>
    <input id='id_usuario' placeholder='Ej: 1'>
    <label>Título de la tarea:</label>
    <input id='titulo_tarea' placeholder='Ej: Terminar laboratorio'>
    <button onclick='crearTarea()'>Crear Tarea</button>
    <div id="resultado_tarea" class="result"></div>
  </div>

  <div class="card">
    <h2>📋 Tareas</h2>
    <button onclick='verTareas()'>Actualizar lista de tareas</button>
    <ul id='lista_tareas'></ul>
  </div>

  <div class="card delete-section">
    <h2>🗑️ Eliminar Datos</h2>
    <label>ID de Tarea a eliminar:</label>
    <input id='tarea-id-eliminar' placeholder='Ej: 1'>
    <button onclick='eliminarTarea()'>Eliminar Tarea</button>
    <div id="resultado-eliminar-tarea" class="result"></div>
    
    <label>ID de Usuario a eliminar:</label>
    <input id='usuario-id-eliminar' placeholder='Ej: 1'>
    <button onclick='eliminarUsuario()'>Eliminar Usuario</button>
    <div id="resultado-eliminar-usuario" class="result"></div>
  </div>

<script>
function crearUsuario() {
  const nombre = document.getElementById('nombre_usuario').value;
  fetch('http://localhost:5001/usuarios', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({nombre})
  }).then(r => r.json()).then(datos => {
    const resultado = document.getElementById('resultado_usuario');
    if (datos.id) {
      resultado.textContent = `✅ Usuario creado con ID ${datos.id}`;
      resultado.className = 'result';
    } else {
      resultado.textContent = `❌ Error: ${datos.error}`;
      resultado.className = 'error';
    }
  });
}

function crearTarea() {
  const titulo = document.getElementById('titulo_tarea').value;
  const usuario_id = document.getElementById('id_usuario').value;
  fetch('http://localhost:5002/tareas', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({titulo, usuario_id})
  }).then(r => r.json()).then(datos => {
    const resultado = document.getElementById('resultado_tarea');
    if (datos.id) {
      resultado.textContent = `✅ Tarea creada con ID ${datos.id}`;
      resultado.className = 'result';
    } else {
      resultado.textContent = `❌ Error: ${datos.error}`;
      resultado.className = 'error';
    }
  });
}

function verTareas() {
  fetch('http://localhost:5002/tareas')
    .then(r => r.json())
    .then(datos => {
      let ul = document.getElementById('lista_tareas');
      ul.innerHTML = '';
      datos.forEach(t => {
        let li = document.createElement('li');
        li.innerText = `${t.titulo} (Usuario ID: ${t.usuario_id})`;
        ul.appendChild(li);
      });
    });
}

function eliminarTarea() {
  const tarea_id = document.getElementById('tarea-id-eliminar').value;
  fetch(`http://localhost:5002/tareas/${tarea_id}`, {
    method: 'DELETE'
  }).then(r => r.json()).then(datos => {
    const resultado = document.getElementById('resultado-eliminar-tarea');
    if (r.ok) {
      resultado.textContent = `✅ Tarea ${tarea_id} eliminada exitosamente`;
      resultado.className = 'result';
    } else {
      resultado.textContent = `❌ Error: ${datos.error}`;
      resultado.className = 'error';
    }
  });
}

function eliminarUsuario() {
  const usuario_id = document.getElementById('usuario-id-eliminar').value;
  fetch(`http://localhost:5001/usuarios/${usuario_id}`, {
    method: 'DELETE'
  }).then(r => r.json()).then(datos => {
    const resultado = document.getElementById('resultado-eliminar-usuario');
    if (r.ok) {
      resultado.textContent = `✅ Usuario ${usuario_id} eliminado exitosamente`;
      resultado.className = 'result';
    } else {
      resultado.textContent = `❌ Error: ${datos.error}`;
      resultado.className = 'error';
    }
  });
}
</script>
</body>
</html>
'''

@frontend.route('/')
def inicio():
    return render_template_string(HTML)

if __name__ == '__main__':
    frontend.run(port=5000)
