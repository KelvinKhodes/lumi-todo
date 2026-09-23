import uuid

from sqlalchemy import select, ColumnElement
from sqlalchemy.orm import scoped_session
from flask_sqlalchemy.session import Session
from typing import Sequence
from app.models.lecturer import Lecturer

class LecturerRepository:
    def __init__(self, session: scoped_session[Session]) -> None:
        self._session = session

    def find_by_id(self, id: uuid.UUID) -> Lecturer | None:
        query = select(Lecturer).where(Lecturer.id == id)

        return self._session.execute(query).scalar_one_or_none()

    def is_email_or_nim_exist(self, nip: int, email: str) -> bool:
        query = select(Lecturer).where(Lecturer.email == email or Lecturer.nip == nip)
        
        res = self._session.execute(query).one_or_none()

        return res != None
    
    def create_lecturer(self, lecturer: Lecturer) -> Lecturer:
        self._session.add(lecturer)
        self._session.flush()

        return lecturer

    def find_all(self, filters: list[ColumnElement[bool]]) -> Sequence[Lecturer]:
        query = select(Lecturer).where(*filters)

        res = self._session.scalars(query).all()

        return res