# Task Manager – Hexagonal Architecture

A clean and maintainable task management service built with hexagonal architecture (ports and adapters pattern) using Python and Flask. This architecture ensures business logic remains decoupled from infrastructure concerns like web frameworks, databases, and external services.

## 🏗️ Architecture Overview

The hexagonal architecture separates the application into three main layers:

- **Domain Layer**: Contains business logic, entities, and ports (interfaces)
- **Application Layer**: Contains use cases that orchestrate business logic
- **Infrastructure Layer**: Contains adapters that implement the ports (HTTP handlers, repositories, etc.)

```
┌─────────────────────────────────────────────────────────┐
│              Infrastructure Layer                       │
│  ┌─────────────┐              ┌──────────────────────┐ │
│  │    HTTP     │              │   InMemoryTask       │ │
│  │   Handler   │              │    Repository        │ │
│  │  (Flask)    │              │                      │ │
│  └─────────────┘              └──────────────────────┘ │
└─────────────────┬─────────────────────────┬─────────────┘
                  │                         │
┌─────────────────┴─────────────────────────┴─────────────┐
│                Application Layer                        │
│              TaskUseCase                                │
│        (Implements TaskInputPort)                       │
└─────────────────────┬───────────────────────────────────┘
                      │
┌─────────────────────┴───────────────────────────────────┐
│                  Domain Layer                          │
│     Task Entity  +  TaskInputPort  +  TaskOutputPort   │
└─────────────────────────────────────────────────────────┘
```

## 📋 API Endpoints

### ➕ Create a Task
Creates a new task with the specified title.

**Request:**
```bash
curl -X POST http://localhost:5000/tasks \
  -H "Content-Type: application/json" \
  -d '{"title": "Learn hexagonal architecture"}'
```

**Response:**
```json
{
  "id": "29434134-f66e-4251-9854-6b6ebf2cab8a",
  "title": "Learn hexagonal architecture",
  "done": false
}
```

### 📄 List All Tasks
Retrieves all created tasks.

**Request:**
```bash
curl http://localhost:5000/tasks
```

**Response:**
```json
[
  {
    "id": "29434134-f66e-4251-9854-6b6ebf2cab8a",
    "title": "Learn hexagonal architecture",
    "done": false
  },
  {
    "id": "f7d8e9a1-2b3c-4d5e-6f7g-8h9i0j1k2l3m",
    "title": "Implement unit tests",
    "done": true
  }
]
```

### ✅ Mark Task as Done
Marks a specific task as completed.

**Request:**
```bash
curl -X PUT http://localhost:5000/tasks/29434134-f66e-4251-9854-6b6ebf2cab8a/done
```

**Response:**
```json
{
  "id": "29434134-f66e-4251-9854-6b6ebf2cab8a",
  "title": "Learn hexagonal architecture",
  "done": true
}
```

## 🚀 Getting Started

### Prerequisites
- Python 
- pip (Python package manager)

The API will be available at `http://localhost:5000`

## 📁 Project Structure

```
Cobras/
├── domain/
│   ├── entities.py          # Task entity
│   └── ports.py             # TaskInputPort & TaskOutputPort interfaces
├── application/
│   └── use_cases.py         # TaskUseCase implementation
├── adapters/
│   ├── http_handler.py      # Flask HTTP adapter
│   └── memory_repo.py       # InMemoryTaskRepository
├── main.py                  # Application entry point
└── README.md
```
