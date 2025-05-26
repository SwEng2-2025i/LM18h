# Task Manager – Hexagonal Architecture

This service allows you to create and list tasks using a hexagonal architecture (ports and adapters). Business logic is decoupled from infrastructure details, such as the web framework or storage.

## 📋 Endpoints disponibles

### ➕ Create a task

Create a new task with a title.

bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender arquitectura hexagonal"}'



### 📄 List all tasks

Returns a list of all created tasks.

bash
curl http://localhost:5000/tasks



### 📄 Mark a task as done

Mark an specific task as done

bash
curl -X PUT http://localhost:5000/tasks/29434134-f66e-4251-9854-6b6ebf2cab8a/done