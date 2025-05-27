import uuid
from dataclasses import dataclass

@dataclass
class Task:
    """
    Represents a task with an ID, title, and completion status.
    """
    id: str
    title: str
    done: bool = False

    def mark_done(self):
        """Marks the task as done."""
        self.done = True

