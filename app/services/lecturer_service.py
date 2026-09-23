from app.repositories.lecturer_repo import LecturerRepository
from app.schemas.lecturer_dto import LecturerCreateDTO, LecturerFilterDTO, LecturerDTO
from app.models.lecturer import Lecturer
from sqlalchemy.orm import scoped_session
from flask_sqlalchemy.session import Session
from app.exceptions.resource_missing import ResourceMissing
from app.exceptions.duplicate_entity import DuplicateEntity
from app.utils.query_specification import QuerySpecification

import uuid

class LecturerService:
    def __init__(self, repo: LecturerRepository, session: scoped_session[Session]):
        self._repo = repo
        self._session = session

    def create_lecturer(self, request: LecturerCreateDTO) -> LecturerDTO:
        if self._repo.is_email_or_nim_exist(request.nip, request.email):
            raise DuplicateEntity("Lecturer with exact email or nim already exists!")

        lecturer = Lecturer(
            nip = request.nip,
            name = request.name,
            email = request.email,
            contact = request.contact
        )

        created_lecturer = self._repo.create_lecturer(lecturer)
        self._session.commit()

        return LecturerDTO.model_validate(created_lecturer)

    def find_lecturer_by_id(self, id: uuid.UUID) -> LecturerDTO:
        lecturer = self._repo.find_by_id(id)

        if lecturer:
            return LecturerDTO.model_validate(lecturer)
        else:
            raise ResourceMissing(f"Lecturer with id: {id} is not exists")

    def find_lecturer_filter(self, request: LecturerFilterDTO) -> list[LecturerDTO]:
        filters = QuerySpecification.lecturer_filter(request=request)

        list_lecturer = self._repo.find_all(filters)
        return [LecturerDTO.model_validate(lecturer) for lecturer in list_lecturer]