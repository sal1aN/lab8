from datetime import datetime, timedelta
from enum import Enum
import uuid
from sqlalchemy import String, DateTime, UUID, Enum as SQLEnum
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class TaskStatus(Enum):
    TODO = "To Do"
    IN_PROGRESS = "In Progress"
    DONE = "Done"


class Task(Base):
    __tablename__ = "tasks"
    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    description: Mapped[str] = mapped_column(String)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now())
    schedule_for: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[TaskStatus] = mapped_column(SQLEnum(TaskStatus), default=TaskStatus.TODO, nullable=False)

    def __str__(self):
        return (
            f"{'ID:':<14}{str(self.id)}\n"
            f"{'Description:':<14}{str(self.description)}\n"
            f"{'Created at:':<14}{str(self.created_at)}\n"
            f"{'Schedule for:':<14}{str(self.schedule_for)}\n"
            f"{'Status:':<14}{str(self.status.value)}\n"
            )

