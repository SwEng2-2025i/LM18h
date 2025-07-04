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
    .danger-button {
      background: #f44336;
      margin-top: 10px;
    }
    .danger-button:hover {
      background: #d32f2f;
    }
    .admin-section {
      border-top: 2px solid #ff9800;
      padding-top: 20px;
      margin-top: 20px;
    }
    .admin-section h3 {
      color: #ff9800;
      margin-bottom: 10px;
    }
    .warning-text {
      color: #ff5722;
      font-size: 14px;
      margin-bottom: 15px;
      font-style: italic;
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
  </style>
</head>
<body>
  <h1>🔧 Laboratorio de Integración</h1>

  <div class="card">
    <h2>👤 Crear Usuario</h2>
    <label>Nombre:</label>
    <input id='username' placeholder='Ej: Ana'>
    <button onclick='crearUsuario()'>Crear Usuario</button>
    <div id="user-result" class="result"></div>
  </div>

  <div class="card">
    <h2>📝 Crear Tarea</h2>
    <label>ID de Usuario:</label>
    <input id='userid' placeholder='Ej: 1'>
    <label>Título de la tarea:</label>
    <input id='task' placeholder='Ej: Terminar laboratorio'>
    <button onclick='crearTarea()'>Crear Tarea</button>
    <div id="task-result" class="result"></div>
  </div>

  <div class="card">
    <h2>📋 Tareas</h2>
    <button onclick='verTareas()'>Actualizar lista de tareas</button>
    <ul id='tasks'></ul>
  </div>

  <div class="card">
    <div class="admin-section">
      <h3>⚠️ Administración - Zona Peligrosa</h3>
      <p class="warning-text">¡CUIDADO! Estos botones eliminarán TODOS los datos permanentemente.</p>
      
      <button class="danger-button" onclick='borrarTodasLasTareas()'>
        🗑️ Borrar TODAS las Tareas
      </button>
      <div id="clear-tasks-result" class="result"></div>
      
      <button class="danger-button" onclick='borrarTodosLosUsuarios()'>
        🗑️ Borrar TODOS los Usuarios
      </button>
      <div id="clear-users-result" class="result"></div>
      
      <button class="danger-button" onclick='borrarTodo()'>
        💥 Borrar TODO (Tareas + Usuarios)
      </button>
      <div id="clear-all-result" class="result"></div>
    </div>
  </div>

<script>
function crearUsuario() {
  const name = document.getElementById('username').value;
  fetch('http://localhost:5001/users', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({name})
  }).then(r => r.json()).then(data => {
    const result = document.getElementById('user-result');
    if (data.id) {
      result.textContent = `✅ Usuario creado con ID ${data.id}`;
      result.className = 'result';
    } else {
      result.textContent = `❌ Error: ${data.error}`;
      result.className = 'error';
    }
  });
}

function crearTarea() {
  const title = document.getElementById('task').value;
  const user_id = document.getElementById('userid').value;
  fetch('http://localhost:5002/tasks', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({title, user_id})
  }).then(r => r.json()).then(data => {
    const result = document.getElementById('task-result');
    if (data.id) {
      result.textContent = `✅ Tarea creada con ID ${data.id}`;
      result.className = 'result';
    } else {
      result.textContent = `❌ Error: ${data.error}`;
      result.className = 'error';
    }
  });
}

function verTareas() {
  fetch('http://localhost:5002/tasks')
    .then(r => r.json())
    .then(data => {
      let ul = document.getElementById('tasks');
      ul.innerHTML = '';
      data.forEach(t => {
        let li = document.createElement('li');
        li.innerText = `${t.title} (Usuario ID: ${t.user_id})`;
        ul.appendChild(li);
      });
    });
}

function borrarTodasLasTareas() {
  if (!confirm('⚠️ ¿Estás seguro de que quieres borrar TODAS las tareas? Esta acción no se puede deshacer.')) {
    return;
  }
  
  fetch('http://localhost:5002/tasks/clear', {
    method: 'DELETE',
    headers: {'Content-Type': 'application/json'}
  }).then(r => r.json()).then(data => {
    const result = document.getElementById('clear-tasks-result');
    if (data.message) {
      result.textContent = `✅ ${data.message}`;
      result.className = 'result';
      // Actualizar la lista de tareas
      verTareas();
    } else {
      result.textContent = `❌ Error: ${data.error}`;
      result.className = 'error';
    }
  }).catch(error => {
    const result = document.getElementById('clear-tasks-result');
    result.textContent = `❌ Error de conexión: ${error.message}`;
    result.className = 'error';
  });
}

function borrarTodosLosUsuarios() {
  if (!confirm('⚠️ ¿Estás seguro de que quieres borrar TODOS los usuarios? Esta acción no se puede deshacer.')) {
    return;
  }
  
  fetch('http://localhost:5001/users/clear', {
    method: 'DELETE',
    headers: {'Content-Type': 'application/json'}
  }).then(r => r.json()).then(data => {
    const result = document.getElementById('clear-users-result');
    if (data.message) {
      result.textContent = `✅ ${data.message}`;
      result.className = 'result';
    } else {
      result.textContent = `❌ Error: ${data.error}`;
      result.className = 'error';
    }
  }).catch(error => {
    const result = document.getElementById('clear-users-result');
    result.textContent = `❌ Error de conexión: ${error.message}`;
    result.className = 'error';
  });
}

function borrarTodo() {
  if (!confirm('🚨 ¿Estás COMPLETAMENTE seguro? Esto borrará TODOS los usuarios Y TODAS las tareas. ¡No hay vuelta atrás!')) {
    return;
  }
  
  const result = document.getElementById('clear-all-result');
  result.textContent = '🧹 Borrando todos los datos...';
  result.className = 'result';
  
  // Primero borrar tareas (por dependencias de FK)
  fetch('http://localhost:5002/tasks/clear', {
    method: 'DELETE',
    headers: {'Content-Type': 'application/json'}
  }).then(r => r.json()).then(taskData => {
    if (taskData.message) {
      // Luego borrar usuarios
      return fetch('http://localhost:5001/users/clear', {
        method: 'DELETE',
        headers: {'Content-Type': 'application/json'}
      });
    } else {
      throw new Error(`Error borrando tareas: ${taskData.error}`);
    }
  }).then(r => r.json()).then(userData => {
    if (userData.message) {
      result.textContent = '✅ ¡TODO borrado exitosamente!';
      result.className = 'result';
      // Actualizar la lista de tareas
      verTareas();
    } else {
      result.textContent = `❌ Error borrando usuarios: ${userData.error}`;
      result.className = 'error';
    }
  }).catch(error => {
    result.textContent = `❌ Error: ${error.message}`;
    result.className = 'error';
  });
}
</script>
</body>
</html>
'''

@frontend.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    frontend.run(port=5000)
