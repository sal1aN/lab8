import uuid
from typing import List
from abc import ABC, abstractmethod
from sqlalchemy.orm import Session
from sqlalchemy import select
from model import Task, TaskStatus


class Repository[T](ABC):
    @abstractmethod
    def get(self, id: uuid.UUID) -> T|None:
        raise NotImplementedError

    @abstractmethod
    def get_all(self) -> List[T]:
        raise NotImplementedError

    @abstractmethod
    def add(self, task: T) -> None:
        raise NotImplementedError

    @abstractmethod
    def update(self) -> None:
        raise NotImplementedError

    @abstractmethod
    def delete(self, task: Task) -> None:
        raise NotImplementedError

    @abstractmethod
    def filter_by_status(self, status: TaskStatus) -> List[T]:
        raise NotImplementedError

class TaskRepository(Repository[Task]):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get(self, id: uuid.UUID) -> Task|None:
        stmt = select(Task).where(Task.id == id)
        return self.session.execute(stmt).scalar_one_or_none()

    def get_all(self) -> List[Task]:
        stmt = select(Task).order_by(Task.id)
        return list(self.session.execute(stmt).scalars().all())

    def add(self, task: Task) -> None:
        self.session.add(task)
        self.session.commit()
        self.session.refresh(task)

    def update(self):
        self.session.commit()

    def delete(self, task: Task) -> None:
        self.session.delete(task)
        self.session.commit()

    def filter_by_status(self, status: TaskStatus) -> List[Task]:
        stmt = select(Task).where(Task.status == status)
        return list(self.session.execute(stmt).scalars().all())

