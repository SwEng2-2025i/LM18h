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
  <h2>🗑️ Eliminar Tarea</h2>
  <label>ID de Tarea:</label>
  <input id='delete-task-id' placeholder='Ej: 10'>
  <label>ID de Usuario:</label>
  <input id='delete-task-user-id' placeholder='Ej: 3'>
  <button onclick='eliminarTarea()'>Eliminar Tarea</button>
  <div id="delete-task-result" class="result"></div>
</div>

<div class="card">
  <h2>❌ Eliminar Usuario</h2>
  <label>ID de Usuario:</label>
  <input id='delete-user-id' placeholder='Ej: 3'>
  <button onclick='eliminarUsuario()'>Eliminar Usuario</button>
  <div id="delete-user-result" class="result"></div>
</div>

  <div class="card">
    <h2>📋 Tareas</h2>
    <button onclick='verTareas()'>Actualizar lista de tareas</button>
    <ul id='tasks'></ul>
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
        li.innerText = `${t.title} (ID: ${t.id}, Usuario ID: ${t.user_id})`;  // 👈 agrega el ID aquí
        ul.appendChild(li);
      });
    });
}

function eliminarTarea() {
  const task_id = document.getElementById('delete-task-id').value;
  const user_id = document.getElementById('delete-task-user-id').value;
  const result = document.getElementById('delete-task-result');

  fetch(`http://localhost:5002/tasks/${task_id}`, {
    method: 'DELETE',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ user_id })
  })
  .then(async res => {
    const text = await res.text();
    let data = {};
    try {
      data = JSON.parse(text);
    } catch (e) {
      result.textContent = '❌ Respuesta inválida del servidor';
      result.className = 'error';
      return;
    }

    result.textContent = data.message || data.error || '❌ Error desconocido';
    result.className = res.ok ? 'result' : 'error';
  })
  .catch(() => {
    result.textContent = '❌ Error de red';
    result.className = 'error';
  });
}





function eliminarUsuario() {
  const user_id = document.getElementById('delete-user-id').value;

  fetch(`http://localhost:5001/users/${user_id}`, {
    method: 'DELETE'
  })
  .then(res => {
    const result = document.getElementById('delete-user-result');
    if (res.status === 200) {
      result.textContent = `✅ Usuario con ID ${user_id} eliminado correctamente`;
      result.className = 'result';
    } else if (res.status === 404) {
      result.textContent = `❌ Usuario con ID ${user_id} no encontrado`;
      result.className = 'error';
    } else {
      result.textContent = `❌ Error al eliminar el usuario`;
      result.className = 'error';
    }
  }).catch(err => {
    document.getElementById('delete-user-result').textContent = `❌ Error de red`;
    document.getElementById('delete-user-result').className = 'error';
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
