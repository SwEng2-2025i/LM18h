from flask import Flask, render_template_string

#---------------------------------------------------------
#------------- FRONT-END - SERVIDOR WEB ------------------
#---------------------------------------------------------

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
      border: 1px solid #ddd;
      font-size: 14px;
    }
    button {
      background: #007bff;
      color: white;
      border: none;
      padding: 12px 20px;
      border-radius: 5px;
      cursor: pointer;
      margin-top: 15px;
      font-size: 14px;
      width: 100%;
    }
    button:hover {
      background: #0056b3;
    }
    #result {
      margin-top: 20px;
      padding: 15px;
      border-radius: 5px;
      font-weight: bold;
    }
    .success {
      background: #d4edda;
      color: #155724;
      border: 1px solid #c3e6cb;
    }
    .error {
      background: #f8d7da;
      color: #721c24;
      border: 1px solid #f5c6cb;
    }
    .task-list {
      background: #e9ecef;
      padding: 15px;
      border-radius: 5px;
      margin-top: 15px;
    }
    .task-item {
      background: white;
      padding: 10px;
      margin: 5px 0;
      border-radius: 3px;
      border-left: 4px solid #007bff;
    }
  </style>
</head>
<body>
  <h1>🚀 Laboratorio de Integración - Lab 2</h1>
  
  <div class="card">
    <h2>Crear Usuario</h2>
    <label for="userName">Nombre del Usuario:</label>
    <input type="text" id="userName" placeholder="Ingresa el nombre del usuario">
    <button onclick="createUser()">Crear Usuario</button>
  </div>
  
  <div class="card">
    <h2>Crear Tarea</h2>
    <label for="taskTitle">Título de la Tarea:</label>
    <input type="text" id="taskTitle" placeholder="Ingresa el título de la tarea">
    <label for="taskUserId">ID del Usuario:</label>
    <input type="number" id="taskUserId" placeholder="Ingresa el ID del usuario">
    <button onclick="createTask()">Crear Tarea</button>
  </div>
  
  <div class="card">
    <h2>Ver Tareas</h2>
    <button onclick="loadTasks()">Cargar Tareas</button>
    <div id="tasksList"></div>
  </div>
  
  <div id="result"></div>

  <script>
    function showResult(message, isSuccess = true) {
      const resultDiv = document.getElementById('result');
      resultDiv.textContent = message;
      resultDiv.className = isSuccess ? 'success' : 'error';
    }

    async function createUser() {
      const userName = document.getElementById('userName').value.trim();
      if (!userName) {
        showResult('Por favor ingresa un nombre de usuario.', false);
        return;
      }

      try {
        const response = await fetch('http://localhost:5001/users', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ name: userName })
        });

        if (response.ok) {
          const userData = await response.json();
          showResult(`✅ Usuario creado exitosamente: ID ${userData.id}, Nombre: ${userData.name}`);
          document.getElementById('userName').value = '';
          document.getElementById('taskUserId').value = userData.id; // Auto-completar para crear tarea
        } else {
          const error = await response.json();
          showResult(`❌ Error al crear usuario: ${error.error}`, false);
        }
      } catch (error) {
        showResult(`❌ Error de conexión: ${error.message}`, false);
      }
    }

    async function createTask() {
      const taskTitle = document.getElementById('taskTitle').value.trim();
      const taskUserId = document.getElementById('taskUserId').value.trim();
      
      if (!taskTitle || !taskUserId) {
        showResult('Por favor completa todos los campos para crear la tarea.', false);
        return;
      }

      try {
        const response = await fetch('http://localhost:5002/tasks', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ 
            title: taskTitle, 
            user_id: parseInt(taskUserId) 
          })
        });

        if (response.ok) {
          const taskData = await response.json();
          showResult(`✅ Tarea creada exitosamente: ID ${taskData.id}, Título: ${taskData.title}, Usuario: ${taskData.user_id}`);
          document.getElementById('taskTitle').value = '';
          loadTasks(); // Recargar lista de tareas
        } else {
          const error = await response.json();
          showResult(`❌ Error al crear tarea: ${error.error}`, false);
        }
      } catch (error) {
        showResult(`❌ Error de conexión: ${error.message}`, false);
      }
    }

    async function loadTasks() {
      try {
        const response = await fetch('http://localhost:5002/tasks');
        
        if (response.ok) {
          const tasks = await response.json();
          const tasksListDiv = document.getElementById('tasksList');
          
          if (tasks.length === 0) {
            tasksListDiv.innerHTML = '<p>No hay tareas registradas.</p>';
          } else {
            tasksListDiv.innerHTML = `
              <div class="task-list">
                <h3>📋 Lista de Tareas (${tasks.length})</h3>
                ${tasks.map(task => `
                  <div class="task-item">
                    <strong>ID:</strong> ${task.id} | 
                    <strong>Título:</strong> ${task.title} | 
                    <strong>Usuario ID:</strong> ${task.user_id}
                  </div>
                `).join('')}
              </div>
            `;
          }
          showResult(`✅ Se cargaron ${tasks.length} tareas.`);
        } else {
          showResult('❌ Error al cargar las tareas.', false);
        }
      } catch (error) {
        showResult(`❌ Error de conexión: ${error.message}`, false);
      }
    }

    // Cargar tareas al iniciar la página
    window.onload = loadTasks;
  </script>
</body>
</html>
'''

@frontend.route('/')
def index():
    return render_template_string(HTML)

if __name__ == '__main__':
    frontend.run(port=5003, debug=True)
