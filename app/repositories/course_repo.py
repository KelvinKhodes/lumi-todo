import uuid

from sqlalchemy import select, ColumnElement
from sqlalchemy.orm import scoped_session
from flask_sqlalchemy.session import Session
from typing import Sequence
from app.models.course import Course

class CourseRepository:
    def __init__(self, session: scoped_session[Session]) -> None:
        self._session = session

    def find_by_id(self, id: uuid.UUID) -> Course | None:
        query = select(Course).where(Course.id == id)

        return self._session.execute(query).scalar_one_or_none()

    def create_course(self, course: Course) -> Course:
        self._session.add(course)
        self._session.flush()

        return course

    def find_all(self, filters: list[ColumnElement[bool]]) -> Sequence[Course]:
        query = select(Course).where(*filters)

        res = self._session.scalars(query).all()

        return res