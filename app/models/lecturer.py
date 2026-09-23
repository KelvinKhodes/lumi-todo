from sqlalchemy import Integer, String
from sqlalchemy.orm import MappedColumn, Mapped, mapped_column, relationship
from app.models.base import BaseModel
from typing import List, TYPE_CHECKING

if TYPE_CHECKING:
    from app.models.course import Course

class Lecturer(BaseModel):
    __tablename__ = "lecturers"

    nip: MappedColumn[int] = mapped_column(
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
    courses: Mapped[List["Course"]] = relationship(
        "Course",
        back_populates="lecturer",
    )

    

