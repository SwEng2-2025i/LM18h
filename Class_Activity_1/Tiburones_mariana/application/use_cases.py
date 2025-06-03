import uuid
from domain.entities import Task
from domain.ports import TaskInputPort, TaskOutputPort

class TaskNotFoundError(Exception):
    pass

class TaskUseCase(TaskInputPort):
    def __init__(self, repo: TaskOutputPort):
        self.repo = repo

    def create_task(self, title: str) -> Task:
        task = Task(id=str(uuid.uuid4()), title=title)
        self.repo.save(task)
        return task

    def get_all_tasks(self) -> list[Task]:
        return self.repo.list_all()

    def update_task(self, task_id: str, done: bool = None) -> Task:
        task = self.repo.find_by_id(task_id)
        
        if task is None:
            raise TaskNotFoundError(f"Task with id {task_id} not found")
            
        if done is not None:
            task.done = done
            
        self.repo.update(task)
        return task

    