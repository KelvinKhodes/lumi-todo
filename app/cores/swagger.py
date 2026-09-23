from typing import Type

from pydantic import BaseModel

from app.schemas.authentication_dto import UserLoginDTO, UserTokenDTO
from app.schemas.course_dto import CourseCreateDTO, CourseDTO, CourseFilterDTO
from app.schemas.course_task_dto import (
    CourseTaskCreateDTO,
    CourseTaskDTO,
    CourseTaskFilterDTO,
)
from app.schemas.lecturer_dto import LecturerCreateDTO, LecturerDTO, LecturerFilterDTO
from app.schemas.user_dto import UserCreateDTO, UserDTO, UserFilterDTO


def _schema(model: Type[BaseModel]) -> dict:
    schema = model.model_json_schema(ref_template="#/definitions/{model}")
    schema.pop("$defs", None)
    return schema


def _response_schema(data_ref: str, is_list: bool = False) -> dict:
    data_schema = {"type": "array", "items": {"$ref": data_ref}} if is_list else {"$ref": data_ref}
    return {
        "type": "object",
        "properties": {
            "data": data_schema,
            "errors": {"type": "string", "nullable": True},
            "request_id": {"type": "string"},
        },
    }


def build_swagger_template() -> dict:
    models = {
        "UserCreateDTO": UserCreateDTO,
        "UserFilterDTO": UserFilterDTO,
        "UserDTO": UserDTO,
        "UserLoginDTO": UserLoginDTO,
        "UserTokenDTO": UserTokenDTO,
        "LecturerCreateDTO": LecturerCreateDTO,
        "LecturerFilterDTO": LecturerFilterDTO,
        "LecturerDTO": LecturerDTO,
        "CourseCreateDTO": CourseCreateDTO,
        "CourseFilterDTO": CourseFilterDTO,
        "CourseDTO": CourseDTO,
        "CourseTaskCreateDTO": CourseTaskCreateDTO,
        "CourseTaskFilterDTO": CourseTaskFilterDTO,
        "CourseTaskDTO": CourseTaskDTO,
    }
    definitions = {name: _schema(model) for name, model in models.items()}
    definitions.update(
        {
            "UserResponse": _response_schema("#/definitions/UserDTO"),
            "UserListResponse": _response_schema("#/definitions/UserDTO", True),
            "LecturerResponse": _response_schema("#/definitions/LecturerDTO"),
            "LecturerListResponse": _response_schema("#/definitions/LecturerDTO", True),
            "CourseResponse": _response_schema("#/definitions/CourseDTO"),
            "CourseListResponse": _response_schema("#/definitions/CourseDTO", True),
            "CourseTaskResponse": _response_schema("#/definitions/CourseTaskDTO"),
            "CourseTaskListResponse": _response_schema("#/definitions/CourseTaskDTO", True),
            "TokenResponse": _response_schema("#/definitions/UserTokenDTO"),
        }
    )

    return {
        "swagger": "2.0",
        "info": {
            "title": "Lumi API",
            "description": "API specification for users, lecturers, courses, tasks, and authentication.",
            "version": "1.0.0",
        },
        "basePath": "/",
        "schemes": ["http", "https"],
        "securityDefinitions": {
            "BearerAuth": {
                "type": "apiKey",
                "name": "Authorization",
                "in": "header",
                "description": "Use the format: Bearer <access_token>",
            }
        },
        "definitions": definitions,
    }