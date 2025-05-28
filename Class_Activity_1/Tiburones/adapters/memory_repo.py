from domain.ports import TaskOutputPort
from domain.entities import Task

class InMemoryTaskRepository(TaskOutputPort):
    def __init__(self):
        self.tasks = []

    def save(self, task: Task) -> None:
        self.tasks.append(task)

    def list_all(self) -> list[Task]:
        return self.tasks
    
    def update_task(self, task: Task) -> None:
        for task1 in self.tasks:
            if task1.id == task.id:
                self.tasks.remove(task1)
                self.tasks.append(task)
                
