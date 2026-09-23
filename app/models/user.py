from sqlalchemy import Integer, String
from sqlalchemy.orm import MappedColumn, mapped_column, relationship, Mapped
from app.models.base import BaseModel
from app.models.course_task import CourseTask
from typing import Optional, List

class User(BaseModel):
    __tablename__ = "users"

    nim: MappedColumn[int] = mapped_column(
        Integer,
        unique=True,
        nullable=False
    )
    name: MappedColumn[str] = mapped_column(
        String(100),
        nullable=False
    )
    email: MappedColumn[str] = mapped_column(
        String(100),
        unique=True,
        nullable=False
    )
    contact: MappedColumn[str] = mapped_column(
        String(100),
        nullable=True
    )
    password: MappedColumn[str] = mapped_column(
        String(100),
        nullable=False
    )
    token: MappedColumn[Optional[str]] = mapped_column(
        String(250),
        nullable=True
    )
    course_tasks: Mapped[List["CourseTask"]] = relationship(
        "CourseTask",
        back_populates="user",
    )

    