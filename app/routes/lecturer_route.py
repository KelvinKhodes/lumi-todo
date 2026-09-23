from flask import Blueprint, request
from app.services.lecturer_service import LecturerService
from app.schemas.lecturer_dto import LecturerCreateDTO, LecturerFilterDTO
from app.routes.wrapper.response_wrapper import wrap_data, wrap_list_data
from app.cores.logging import logger
import uuid

def create_lecturer_bp(lecturer_service: LecturerService):
    lecturer_bp = Blueprint("lecturers", __name__, url_prefix="/lecturers")

    @lecturer_bp.get("/<uuid:id>")
    def get_lecturer(id: uuid.UUID):
        """Get a lecturer by ID.
        ---
        tags:
          - Lecturers
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
            description: Lecturer details.
            schema:
              $ref: '#/definitions/LecturerResponse'
          404:
            description: Lecturer not found.
        """
        logger.info("Get Lecturer")
        lecturer = lecturer_service.find_lecturer_by_id(id)

        logger.debug(f"Success retrieve data: {lecturer}")
        return wrap_data(lecturer), 200
    
    @lecturer_bp.get("/search")
    def get_lecturer_filter():
        """Search lecturers.
        ---
        tags:
          - Lecturers
        security:
          - BearerAuth: []
        parameters:
          - in: query
            name: id
            type: string
            format: uuid
          - in: query
            name: nip
            type: integer
          - in: query
            name: name
            type: string
          - in: query
            name: email
            type: string
          - in: query
            name: contact
            type: string
        responses:
          200:
            description: Matching lecturers.
            schema:
              $ref: '#/definitions/LecturerListResponse'
        """
        logger.info("Get Lecturer by filter")
        params = LecturerFilterDTO.model_validate(request.args.to_dict())
        list_lecturer = lecturer_service.find_lecturer_filter(params)
    
        logger.debug("Success retrieve data: ", list_lecturer)
        return wrap_list_data(list_lecturer), 200

    @lecturer_bp.post("/")
    def create_lecturer():
        """Create a lecturer.
        ---
        tags:
          - Lecturers
        security:
          - BearerAuth: []
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/LecturerCreateDTO'
        responses:
          201:
            description: Lecturer created.
            schema:
              $ref: '#/definitions/LecturerResponse'
          400:
            description: Invalid request payload.
          409:
            description: Lecturer already exists.
        """
        payload = request.get_json()
        lecturer_create_dto = LecturerCreateDTO.model_validate(payload)
        logger.info(f"Creating Lecturer with name: {lecturer_create_dto.name}")

        return wrap_data(lecturer_service.create_lecturer(lecturer_create_dto)), 201
    
    return lecturer_bp