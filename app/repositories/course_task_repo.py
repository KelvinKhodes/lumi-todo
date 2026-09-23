import uuid

from sqlalchemy import select, ColumnElement
from sqlalchemy.orm import scoped_session
from flask_sqlalchemy.session import Session
from typing import Sequence
from app.models.course_task import CourseTask
from app.models.course import Course

class CourseTaskRepository:
    def __init__(self, session: scoped_session[Session]) -> None:
        self._session = session

    def find_by_id(self, id: uuid.UUID) -> CourseTask | None:
        query = select(CourseTask).where(CourseTask.id == id).join(Course, CourseTask.course_id == Course.id)

        return self._session.execute(query).scalar_one_or_none()

    def create_course_task(self, course_task: CourseTask) -> CourseTask:
        self._session.add(course_task)
        self._session.flush()

        return course_task

    def find_all(self, filters: list[ColumnElement[bool]]) -> Sequence[CourseTask]:
        query = select(CourseTask).where(*filters).join(Course, CourseTask.course_id == Course.id)

        res = self._session.scalars(query).all()

        return res