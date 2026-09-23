from app.schemas.user_dto import UserFilterDTO
from app.schemas.lecturer_dto import LecturerFilterDTO
from app.schemas.course_dto import CourseFilterDTO
from app.schemas.course_task_dto import CourseTaskFilterDTO
from sqlalchemy import ColumnElement
from app.models.user import User
from app.models.lecturer import Lecturer
from app.models.course import Course
from app.models.course_task import CourseTask

class QuerySpecification:

    @staticmethod
    def user_filter(request: UserFilterDTO) -> list[ColumnElement[bool]]:
        filters = []

        if request.id:
            filters.append(User.id == request.id)
        if request.nim:
            filters.append(User.nim == request.nim)
        if request.name:
            filters.append(User.name.ilike(request.name))
        if request.email:
            filters.append(User.email == request.email)
        if request.contact:
            filters.append(User.contact == request.contact)

        return filters

    @staticmethod
    def lecturer_filter(request: LecturerFilterDTO) -> list[ColumnElement[bool]]:
        filters = []
    
        if request.id:
            filters.append(Lecturer.id == request.id)
        if request.nip:
            filters.append(Lecturer.nip == request.nip)
        if request.name:
            filters.append(Lecturer.name.ilike(request.name))
        if request.email:
            filters.append(Lecturer.email == request.email)
        if request.contact:
            filters.append(Lecturer.contact == request.contact)
        
        return filters
    
    @staticmethod
    def course_filter(request: CourseFilterDTO) -> list[ColumnElement[bool]]:
        filters = []
    
        if request.id:
            filters.append(Course.id == request.id)
        if request.name:
            filters.append(Course.name.ilike(request.name))
        if request.lecturer_id:
            filters.append(Course.lecturer_id == request.lecturer_id)
        
        return filters
    
    @staticmethod
    def course_task_filter(request: CourseTaskFilterDTO) -> list[ColumnElement[bool]]:
        filters = []
    
        if request.id:
            filters.append(CourseTask.id == request.id)
        if request.title:
            filters.append(CourseTask.title.ilike(request.title))
        if request.status:
            filters.append(CourseTask.status == request.status)
        if request.user_id:
            filters.append(CourseTask.user_id == request.user_id)
        if request.course_id:
            filters.append(CourseTask.course_id == request.course_id)
        
        return filters