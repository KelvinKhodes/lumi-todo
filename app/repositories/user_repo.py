import uuid

from sqlalchemy import select, ColumnElement
from sqlalchemy.orm import scoped_session
from flask_sqlalchemy.session import Session
from typing import Sequence
from app.models.user import User

class UserRepository:
    def __init__(self, session: scoped_session[Session]) -> None:
        self._session = session

    def find_by_id(self, id: uuid.UUID) -> User | None:
        query = select(User).where(User.id == id)

        return self._session.execute(query).scalar_one_or_none()

    def find_by_nim(self, nim: int) -> User | None:
            query = select(User).where(User.nim == nim)
    
            return self._session.execute(query).scalar_one_or_none()
    
    def is_email_or_nim_exist(self, nim: int, email: str) -> bool:
        query = select(User).where(User.email == email or User.nim == nim)
        
        res = self._session.execute(query).one_or_none()

        return res != None
    
    def create_user(self, user: User) -> User:
        self._session.add(user)
        self._session.flush()

        return user

    def find_all(self, filters: list[ColumnElement[bool]]) -> Sequence[User]:
        query = select(User).where(*filters)

        res = self._session.scalars(query).all()

        return res