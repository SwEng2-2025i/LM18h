# Task Manager – Hexagonal Architecture

This service allows you to create and list tasks using a hexagonal architecture (ports and adapters). Business logic is decoupled from infrastructure details, such as the web framework or storage.

## 📋 Endpoints disponibles

### ➕ Create a task

Create a new task with a title.

#### Using curl (Windows):
```bash
curl -X POST http://localhost:5000/tasks -H "Content-Type: application/json" -d "{\"title\": \"Aprender arquitectura hexagonal\"}"
```

#### Using curl (Linux/Mac):
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Aprender arquitectura hexagonal"}'
```

#### Using Postman:
1. Create new request
2. Set method to `POST`
3. Enter URL: `http://localhost:5000/tasks`
4. Go to "Body" tab
5. Select "raw" and "JSON"
6. Enter JSON:
```json
{
    "title": "Aprender arquitectura hexagonal"
}
```
7. Click "Send"

### 📄 List all tasks

Returns a list of all created tasks.

#### Using curl:
```bash
curl http://localhost:5000/tasks
```

#### Using Postman:
1. Create new request
2. Set method to `GET`
3. Enter URL: `http://localhost:5000/tasks`
4. Click "Send"

### ✅ Mark task as done

Mark a specific task as completed.

#### Using curl (Windows):
```bash
curl -X PUT http://localhost:5000/tasks/<task_id>/done
```

#### Using curl (Linux/Mac):
```bash
curl -X PUT http://localhost:5000/tasks/<task_id>/done
```

#### Using Postman:
1. Create new request
2. Set method to `PUT`
3. Enter URL: `http://localhost:5000/tasks/<task_id>/done`
   (Replace `<task_id>` with the actual task ID)
4. Click "Send"

## 🚀 Running the application

1. Install dependencies:
```bash
pip install flask==2.0.1 werkzeug==2.0.1
```

2. Run the application:
```bash
python main.py
```

The server will start at `http://localhost:5000`