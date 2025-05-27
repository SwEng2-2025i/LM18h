# Task Manager – Hexagonal Architecture

This service allows you to create, list, and manage tasks using a hexagonal architecture (ports and adapters). Business logic is decoupled from infrastructure details, such as the web framework or storage.

## 🏗️ Architecture Overview

The application follows the Hexagonal Architecture pattern (also known as Ports and Adapters) with the following components:

- **Domain Layer**: Contains the core business logic and entities
  - `Task` entity with properties: id, title, and done status
  - Ports (interfaces) for input and output operations

- **Application Layer**: Implements use cases using the domain entities
  - Task creation
  - Task listing
  - Task status updates

- **Adapters Layer**: Implements the ports for external interactions
  - HTTP adapter for REST API endpoints
  - In-memory repository for data storage

## 🚀 Getting Started

### Prerequisites
- Python 3.x
- Flask

### Installation

1. Install the required dependencies:
```bash
pip install flask
```

2. Run the application:
```bash
python main.py
```

The server will start on `http://localhost:5002`

## 📋 Available Endpoints

### ➕ Create a Task
Creates a new task with the specified title.

```bash
curl -X POST http://localhost:5002/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn hexagonal architecture"}'
```

Response (201 Created):
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Learn hexagonal architecture",
    "done": false
}
```

### 📄 List All Tasks
Returns a list of all created tasks.

```bash
curl http://localhost:5002/tasks
```

Response (200 OK):
```json
[
    {
        "id": "550e8400-e29b-41d4-a716-446655440000",
        "title": "Learn hexagonal architecture",
        "done": false
    }
]
```

### 🔍 Get Task by ID
Retrieves a specific task by its ID.

```bash
curl http://localhost:5002/tasks/{task_id}
```

Response (200 OK):
```json
{
    "id": "550e8400-e29b-41d4-a716-446655440000",
    "title": "Learn hexagonal architecture",
    "done": false
}
```

### ✅ Mark Task as Done
Marks a specific task as completed.

```bash
curl -X POST http://localhost:5002/tasks/mark_done/{task_id}
```

Response (200 OK):
```json
{
    "message": "Task marked as done"
}
```

## 🔧 Error Handling

The API returns appropriate HTTP status codes:
- 201: Task created successfully
- 200: Operation successful
- 400: Invalid request (missing required fields)
- 404: Task not found
- 500: Internal server error

## 📁 Project Structure

```
Example 4 - Hexagonal Architecture/
├── adapters/
│   ├── http_handler.py    # HTTP adapter for REST API
│   └── memory_repo.py     # In-memory storage implementation
├── application/
│   └── use_cases.py       # Business logic implementation
├── domain/
│   ├── entities.py        # Task entity definition
│   └── ports.py           # Input/output port interfaces
└── main.py                # Application entry point
```

## 🔄 Development

The application is built with extensibility in mind. To add new features:

1. Define new ports in `domain/ports.py`
2. Implement use cases in `application/use_cases.py`
3. Add new adapters in the `adapters` directory
4. Update the HTTP handler in `adapters/http_handler.py`

## 📝 License

This project is open source and available under the MIT License.