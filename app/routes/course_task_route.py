from flask import Blueprint, request
from app.services.course_task_service import CourseTaskService
from app.schemas.course_task_dto import CourseTaskCreateDTO, CourseTaskFilterDTO
from app.routes.wrapper.response_wrapper import wrap_data, wrap_list_data
from app.cores.logging import logger
import uuid

def create_course_task_bp(course_task_service: CourseTaskService):
    course_task_bp = Blueprint("course_tasks", __name__, url_prefix="/course_tasks")

    @course_task_bp.get("/<uuid:id>")
    def get_course_task(id: uuid.UUID):
        """Get a course task by ID.
        ---
        tags:
          - Course Tasks
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
            description: Course task details.
            schema:
              $ref: '#/definitions/CourseTaskResponse'
          404:
            description: Course task not found.
        """
        logger.info("Get CourseTask")
        course_task = course_task_service.find_course_task_by_id(id)

        logger.debug(f"Success retrieve data: {course_task}")
        return wrap_data(course_task), 200
    
    @course_task_bp.get("/search")
    def get_course_task_filter():
        """Search course tasks.
        ---
        tags:
          - Course Tasks
        security:
          - BearerAuth: []
        parameters:
          - in: query
            name: id
            type: string
            format: uuid
          - in: query
            name: title
            type: string
          - in: query
            name: status
            type: string
            enum: [PROGRES, FINISHED, OVERDUE]
          - in: query
            name: user_id
            type: string
            format: uuid
          - in: query
            name: course_id
            type: string
            format: uuid
        responses:
          200:
            description: Matching course tasks.
            schema:
              $ref: '#/definitions/CourseTaskListResponse'
        """
        logger.info("Get CourseTask by filter")
        params = CourseTaskFilterDTO.model_validate(request.args.to_dict())
        list_course_task = course_task_service.find_course_task_filter(params)
    
        logger.debug("Success retrieve data: ", list_course_task)
        return wrap_list_data(list_course_task), 200

    @course_task_bp.post("/")
    def create_course_task():
        """Create a course task.
        ---
        tags:
          - Course Tasks
        security:
          - BearerAuth: []
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/CourseTaskCreateDTO'
        responses:
          201:
            description: Course task created.
            schema:
              $ref: '#/definitions/CourseTaskResponse'
          400:
            description: Invalid request payload.
          404:
            description: Course not found.
        """
        payload = request.get_json()
        course_task_create_dto = CourseTaskCreateDTO.model_validate(payload)
        logger.info(f"Creating CourseTask with title: {course_task_create_dto.title}")

        return wrap_data(course_task_service.create_course_task(course_task_create_dto)), 201
    
    return course_task_bp
