from sqlalchemy import String, Text, DateTime, Uuid, ForeignKey, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import MappedColumn, Mapped, mapped_column, relationship
from app.models.base import BaseModel
from typing import TYPE_CHECKING

from datetime import datetime, timezone
from app.models.enums.task_status import TaskStatus

if TYPE_CHECKING:
    from app.models.course import Course
    from app.models.user import User
    

class CourseTask(BaseModel):
    __tablename__ = "course_tasks"

    title: MappedColumn[str] = mapped_column(
        String(100),
        nullable=False
    )
    description: MappedColumn[str] = mapped_column(
        Text(),
        nullable=True
    )
    status: MappedColumn[TaskStatus] = mapped_column(
        Enum(
            TaskStatus,
            name = "task_status",
            values_callable=lambda obj: [e.value for e in obj]
        ),
        default=TaskStatus.PROGRES,
        nullable=False,
        index=True
    )
    course_id: MappedColumn[Uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("courses.id", ondelete="SET NULL"),
        nullable=False,
        index=True
    ) 
    course: Mapped["Course"] = relationship(
        "Course",
        back_populates="course_tasks"
    )
    user_id: MappedColumn[Uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="SET NULL"),
        nullable=False,
        index=True
    ) 
    user: Mapped["User"] = relationship(
        "User",
        back_populates="course_tasks"
    )
    start_at: MappedColumn[DateTime] = mapped_column(
        DateTime(timezone=True), 
        default=lambda: datetime.now(timezone.utc),
        nullable=False
    )
    finish_at: MappedColumn[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=True
    )
    end_at: MappedColumn[DateTime] = mapped_column(
        DateTime(timezone=True),
        nullable=False
    )

    @property
    def course_name(self) -> str:
        return self.course.name

    