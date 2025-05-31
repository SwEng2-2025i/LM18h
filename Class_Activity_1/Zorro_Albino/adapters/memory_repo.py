from domain.ports import TaskOutputPort
from domain.entities import Task

class InMemoryTaskRepository(TaskOutputPort):
    """
    An in-memory implementation of the TaskOutputPort.
    This repository stores tasks in a list in memory.
    """
    def __init__(self):
        """Initializes the repository with an empty list of tasks."""
        self.tasks = []

    def save(self, task: Task) -> None:
        """
        Saves a task to the repository.
        Args:
            task: The Task object to save.
        """
        self.tasks.append(task)

    def list_all(self) -> list[Task]:
        """
        Retrieves all tasks from the repository.
        Returns:
            A list of all Task objects.
        """
        return self.tasks
    
    def set_task_done(self, task_id: str) -> Task:
        """
        Marks a task as done.
        Args:
            task_id: The ID of the task to mark as done.
        Returns:
            The updated Task object.
        Raises:
            ValueError: If no task with the given ID is found.
        """
        for task in self.tasks:
            if task.id == task_id:
                task.mark_done()
                return task
        raise ValueError(f"Task with id {task_id} not found")

