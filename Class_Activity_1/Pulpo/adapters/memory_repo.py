from domain.ports import TaskOutputPort
from domain.entities import Task

class InMemoryTaskRepository(TaskOutputPort):
    def __init__(self):
        self.tasks = []

    def save(self, task: Task) -> None:
        self.tasks.append(task)

    def list_all(self) -> list[Task]:
        return self.tasks

    def mark_done(self, task_id: str) -> Task:
        for task in self.tasks:
            if task.id == task_id:
                task.mark_done()
                return task
        raise ValueError("Task not found")