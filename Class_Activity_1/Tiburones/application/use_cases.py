import uuid
from domain.entities import Task
from domain.ports import TaskInputPort, TaskOutputPort

class TaskUseCase(TaskInputPort):
    def __init__(self, repo: TaskOutputPort):
        self.repo = repo

    def create_task(self, title: str) -> Task:
        task = Task(id=str(uuid.uuid4()), title=title)
        self.repo.save(task)
        return task

    def get_all_tasks(self) -> list[Task]:
        return self.repo.list_all()
    
    def get_task(self, id):
        tasks = self.get_all_tasks()
        for task in tasks:
            if task.id == id:
                return task
    
    def update_task(self, id:str) -> Task:
        task = self.get_task(id)
        task.mark_done()
        return self.repo.update_task(task)
