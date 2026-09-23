from app.repositories.course_repo import CourseRepository
from app.repositories.lecturer_repo import LecturerRepository
from app.schemas.course_dto import CourseCreateDTO, CourseFilterDTO, CourseDTO
from app.models.course import Course
from sqlalchemy.orm import scoped_session
from flask_sqlalchemy.session import Session
from app.exceptions.resource_missing import ResourceMissing
from app.utils.query_specification import QuerySpecification

import uuid

class CourseService:
    def __init__(self, course_repo: CourseRepository, lecturer_repo: LecturerRepository, session: scoped_session[Session]):
        self._course_repo = course_repo
        self._lecturer_repo = lecturer_repo
        self._session = session

    def create_course(self, request: CourseCreateDTO) -> CourseDTO:
        if self._lecturer_repo.find_by_id(request.lecturer_id) is None:
            raise ResourceMissing(f"No such lecturer with id {request.lecturer_id}.")
        
        course = Course(
            name = request.name,
            lecturer_id = request.lecturer_id
        )

        created_course = self._course_repo.create_course(course)
        self._session.commit()

        return CourseDTO.model_validate(created_course)

    def find_course_by_id(self, id: uuid.UUID) -> CourseDTO:
        course = self._course_repo.find_by_id(id)

        if course:
            return CourseDTO.model_validate(course)
        else:
            raise ResourceMissing(f"Course with id: {id} is not exists")

    def find_course_filter(self, request: CourseFilterDTO) -> list[CourseDTO]:
        filters = QuerySpecification.course_filter(request=request)

        list_course = self._course_repo.find_all(filters)
        return [CourseDTO.model_validate(course) for course in list_course]