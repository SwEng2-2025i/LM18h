import uuid
from domain.entities import Task
from domain.ports import TaskInputPort, TaskOutputPort

class TaskUseCase(TaskInputPort):
    """
    Implements the use cases for task management.
    This class acts as an input port, handling application logic.
    """
    def __init__(self, repo: TaskOutputPort):
        """
        Initializes the TaskUseCase with a repository.

        Args:
            repo: An instance of a class that implements TaskOutputPort,
                  used for data persistence.
        """
        self.repo = repo

    def create_task(self, title: str) -> Task:
        """
        Creates a new task.

        Args:
            title: The title of the task.

        Returns:
            The created Task object.
        """
        task = Task(id=str(uuid.uuid4()), title=title)
        self.repo.save(task)
        return task

    def get_all_tasks(self) -> list[Task]:
        """
        Retrieves all tasks.

        Returns:
            A list of all Task objects.
        """
        return self.repo.list_all()
    
    def set_task_done(self, task_id: str) -> Task:
        """
        Marks a specific task as done.

        Args:
            task_id: The ID of the task to mark as done.

        Returns:
            The updated Task object.

        Raises:
            ValueError: If no task with the given ID is found.
        """
        tasks = self.repo.list_all()
        for task in tasks:
            if task.id == task_id:
                task.mark_done()
                self.repo.save(task)
                return task
        raise ValueError(f"Task with id {task_id} not found")