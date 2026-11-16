"""Small task management domain model used in the quality and CI labs."""

from dataclasses import dataclass, field
from datetime import date
from enum import StrEnum


class Status(StrEnum):
    IN_PROGRESS = "In progress"
    DONE = "Done"


@dataclass
class Task:
    task_id: int
    title: str
    due_date: date
    status: Status = Status.IN_PROGRESS
    tags: list[str] = field(default_factory=list)


class TaskManager:
    def __init__(self) -> None:
        self._tasks: dict[int, Task] = {}

    def create(self, task: Task) -> None:
        if task.task_id in self._tasks:
            raise ValueError("A task with this ID already exists")
        if not task.title.strip():
            raise ValueError("Task title cannot be empty")
        task.title = task.title.strip()
        self._tasks[task.task_id] = task

    def update_title(self, task_id: int, title: str) -> Task:
        task = self.get(task_id)
        if not title.strip():
            raise ValueError("Task title cannot be empty")
        task.title = title.strip()
        return task

    def set_status(self, task_id: int, status: Status) -> Task:
        task = self.get(task_id)
        if not isinstance(status, Status):
            raise ValueError("Unknown status")
        task.status = status
        return task

    def delete(self, task_id: int) -> Task:
        try:
            return self._tasks.pop(task_id)
        except KeyError as error:
            raise KeyError(f"Task {task_id} was not found") from error

    def get(self, task_id: int) -> Task:
        try:
            return self._tasks[task_id]
        except KeyError as error:
            raise KeyError(f"Task {task_id} was not found") from error

    def list_tasks(self) -> list[Task]:
        return sorted(self._tasks.values(), key=lambda task: task.due_date)

    def search_by_title(self, query: str) -> list[Task]:
        term = query.strip().casefold()
        if not term:
            return []
        return [task for task in self.list_tasks() if term in task.title.casefold()]

    def set_tags(self, task_id: int, tags: list[str]) -> Task:
        task = self.get(task_id)
        task.tags = list(dict.fromkeys(tag.strip() for tag in tags if tag.strip()))
        return task

    def filter_by_status(self, status: Status) -> list[Task]:
        return [task for task in self.list_tasks() if task.status is status]

    def overdue(self, today: date) -> list[Task]:
        return [
            task
            for task in self._tasks.values()
            if task.status is Status.IN_PROGRESS and task.due_date < today
        ]
