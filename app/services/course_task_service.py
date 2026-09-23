from flask import g
from app.models.enums.task_status import TaskStatus
from app.models.course_task import CourseTask
from app.repositories.course_task_repo import CourseTaskRepository
from app.repositories.course_repo import CourseRepository
from app.schemas.course_task_dto import CourseTaskCreateDTO, CourseTaskFilterDTO, CourseTaskDTO

from sqlalchemy.orm import scoped_session
from flask_sqlalchemy.session import Session
from app.exceptions.resource_missing import ResourceMissing
from app.utils.query_specification import QuerySpecification

import uuid

class CourseTaskService:
    def __init__(self, course_task_repo: CourseTaskRepository, course_repo: CourseRepository, session: scoped_session[Session]):
        self._course_task_repo = course_task_repo
        self._course_repo = course_repo
        self._session = session

    def create_course_task(self, request: CourseTaskCreateDTO) -> CourseTaskDTO:
        course = self._course_repo.find_by_id(request.course_id)
        if course is None:
            raise ResourceMissing(f"No such course with id {request.course_id}.")
        
        course_task = CourseTask(
            title = request.title,
            description = request.description,
            course_id = request.course_id,
            status = TaskStatus.PROGRES,
            user_id = g.user_id,
            start_at = request.start_at,
            end_at = request.end_at
        )

        created_course_task = self._course_task_repo.create_course_task(course_task)
        self._session.commit()

        created_course_task.course = course
        return CourseTaskDTO.model_validate(created_course_task)

    def find_course_task_by_id(self, id: uuid.UUID) -> CourseTaskDTO:
        course_task = self._course_task_repo.find_by_id(id)

        if course_task:
            return CourseTaskDTO.model_validate(course_task)
        else:
            raise ResourceMissing(f"CourseTask with id: {id} is not exists")

    def find_course_task_filter(self, request: CourseTaskFilterDTO) -> list[CourseTaskDTO]:
        request.user_id = g.user_id
        filters = QuerySpecification.course_task_filter(request=request)

        list_course_task = self._course_task_repo.find_all(filters)
        return [CourseTaskDTO.model_validate(course_task) for course_task in list_course_task]