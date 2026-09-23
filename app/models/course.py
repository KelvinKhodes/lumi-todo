from sqlalchemy import String, Uuid, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import MappedColumn, Mapped, mapped_column, relationship
from app.models.base import BaseModel
from app.models.course_task import CourseTask
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from app.models.lecturer import Lecturer

class Course(BaseModel):
    __tablename__ = "courses"

    name: MappedColumn[str] = mapped_column(
        String(100),
        nullable=False
    )
    lecturer_id: MappedColumn[Uuid] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("lecturers.id", ondelete="SET NULL"),
        nullable=False,
        index=True
    ) 
    lecturer: Mapped["Lecturer"] = relationship(
        "Lecturer",
        back_populates="courses"
    )
    course_tasks: Mapped[List["CourseTask"]] = relationship(
        "CourseTask",
        back_populates="course",
    )

    