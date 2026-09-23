from flask import Blueprint, request
from app.services.course_service import CourseService
from app.schemas.course_dto import CourseCreateDTO, CourseFilterDTO
from app.routes.wrapper.response_wrapper import wrap_data, wrap_list_data
from app.cores.logging import logger
import uuid

def create_course_bp(course_service: CourseService):
    course_bp = Blueprint("courses", __name__, url_prefix="/courses")

    @course_bp.get("/<uuid:id>")
    def get_course(id: uuid.UUID):
        """Get a course by ID.
        ---
        tags:
          - Courses
        security:
          - BearerAuth: []
        parameters:
          - in: path
            name: id
            type: string
            format: uuid
            required: true
        responses:
          200:
            description: Course details.
            schema:
              $ref: '#/definitions/CourseResponse'
          404:
            description: Course not found.
        """
        logger.info("Get Course")
        course = course_service.find_course_by_id(id)

        logger.debug(f"Success retrieve data: {course}")
        return wrap_data(course), 200
    
    @course_bp.get("/search")
    def get_course_filter():
        """Search courses.
        ---
        tags:
          - Courses
        security:
          - BearerAuth: []
        parameters:
          - in: query
            name: id
            type: string
            format: uuid
          - in: query
            name: name
            type: string
          - in: query
            name: lecturer_id
            type: string
            format: uuid
        responses:
          200:
            description: Matching courses.
            schema:
              $ref: '#/definitions/CourseListResponse'
        """
        logger.info("Get Course by filter")
        params = CourseFilterDTO.model_validate(request.args.to_dict())
        list_course = course_service.find_course_filter(params)
    
        logger.debug("Success retrieve data: ", list_course)
        return wrap_list_data(list_course), 200

    @course_bp.post("/")
    def create_course():
        """Create a course.
        ---
        tags:
          - Courses
        security:
          - BearerAuth: []
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/CourseCreateDTO'
        responses:
          201:
            description: Course created.
            schema:
              $ref: '#/definitions/CourseResponse'
          400:
            description: Invalid request payload.
          404:
            description: Lecturer not found.
        """
        payload = request.get_json()
        course_create_dto = CourseCreateDTO.model_validate(payload)
        logger.info(f"Creating Course with name: {course_create_dto.name}")

        return wrap_data(course_service.create_course(course_create_dto)), 201
    
    return course_bp
