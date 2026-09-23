from flask import Blueprint, request
from app.services.user_service import UserService
from app.schemas.user_dto import UserCreateDTO, UserFilterDTO
from app.routes.wrapper.response_wrapper import wrap_data, wrap_list_data
from app.cores.logging import logger
import uuid

def create_user_bp(user_service: UserService):
    user_bp = Blueprint("users", __name__, url_prefix="/users")

    @user_bp.get("/<uuid:id>")
    def get_user(id: uuid.UUID):
        """Get a user by ID.
        ---
        tags:
          - Users
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
            description: User details.
            schema:
              $ref: '#/definitions/UserResponse'
          404:
            description: User not found.
        """
        logger.info("Get User")
        user = user_service.find_user_by_id(id)

        logger.debug(f"Success retrieve data: {user}")
        return wrap_data(user), 200
    
    @user_bp.get("/search")
    def get_user_filter():
        """Search users.
        ---
        tags:
          - Users
        security:
          - BearerAuth: []
        parameters:
          - in: query
            name: id
            type: string
            format: uuid
          - in: query
            name: nim
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
            description: Matching users.
            schema:
              $ref: '#/definitions/UserListResponse'
        """
        logger.info("Get User by filter")
        params = UserFilterDTO.model_validate(request.args.to_dict())
        list_user = user_service.find_user_filter(params)
    
        logger.debug("Success retrieve data: ", list_user)
        return wrap_list_data(list_user), 200

    @user_bp.post("/")
    def create_user():
        """Create a user.
        ---
        tags:
          - Users
        consumes:
          - application/json
        parameters:
          - in: body
            name: body
            required: true
            schema:
              $ref: '#/definitions/UserCreateDTO'
        responses:
          201:
            description: User created.
            schema:
              $ref: '#/definitions/UserResponse'
          400:
            description: Invalid request payload.
          409:
            description: User already exists.
        """
        payload = request.get_json()
        user_create_dto = UserCreateDTO.model_validate(payload)
        logger.info(f"Creating User with name: {user_create_dto.name}")

        return wrap_data(user_service.create_user(user_create_dto)), 201
    
    return user_bp