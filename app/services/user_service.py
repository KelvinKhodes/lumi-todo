from app.repositories.user_repo import UserRepository
from app.schemas.user_dto import UserCreateDTO, UserFilterDTO, UserDTO
from app.models.user import User
from app.exceptions.resource_missing import ResourceMissing
from app.exceptions.duplicate_entity import DuplicateEntity
from app.utils.password_hasher import PasswordHasher
from app.utils.query_specification import QuerySpecification
from sqlalchemy.orm import scoped_session
from flask_sqlalchemy.session import Session

import uuid

class UserService:
    def __init__(self, repo: UserRepository, password_utils: PasswordHasher, session: scoped_session[Session]):
        self._repo = repo
        self._password_utils = password_utils
        self._session = session

    def create_user(self, request: UserCreateDTO) -> UserDTO:
        if self._repo.is_email_or_nim_exist(request.nim, request.email):
            raise DuplicateEntity("User with exact email or nim already exists!")

        hashedPassword = self._password_utils.hash_password(request.password)

        user = User(
            nim = request.nim,
            name = request.name,
            email = request.email,
            contact = request.contact,
            password = hashedPassword
        )

        created_user = self._repo.create_user(user)
        self._session.commit()

        return UserDTO.model_validate(created_user)

    def find_user_by_id(self, id: uuid.UUID) -> UserDTO:
        user = self._repo.find_by_id(id)

        if user:
            return UserDTO.model_validate(user)
        else:
            raise ResourceMissing(f"User with id: {id} is not exists")

    def find_user_filter(self, request: UserFilterDTO) -> list[UserDTO]:
        filters = QuerySpecification.user_filter(request=request)

        list_user = self._repo.find_all(filters)
        return [UserDTO.model_validate(user) for user in list_user]