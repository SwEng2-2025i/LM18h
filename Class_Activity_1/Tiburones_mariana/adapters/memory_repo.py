from domain.ports import TaskOutputPort
from domain.entities import Task

class InMemoryTaskRepository(TaskOutputPort):
    def __init__(self):
        self.tasks = []

    def save(self, task: Task) -> None:
        self.tasks.append(task)

    def list_all(self) -> list[Task]:
        return self.tasks

    def find_by_id(self, task_id: str) -> Task | None:
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update(self, task: Task) -> None:
        for i, t in enumerate(self.tasks):
            if t.id == task.id:
                self.tasks[i] = task
                break