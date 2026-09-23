from app.repositories.user_repo import UserRepository
from app.utils.password_hasher import PasswordHasher
from app.utils.jwt_utils import JwtUtils
from app.schemas.authentication_dto import UserLoginDTO, UserTokenDTO
from sqlalchemy.orm import scoped_session
from flask_sqlalchemy.session import Session
from app.exceptions.resource_missing import ResourceMissing
from app.exceptions.authentication_exception import AuthenticationException

class AuthenticationService:
    def __init__(self, user_repo: UserRepository, password_utils: PasswordHasher, jwt_utils: JwtUtils, session: scoped_session[Session]):
        self._user_repo = user_repo
        self._password_utils = password_utils
        self._jwt_utils = jwt_utils
        self._session = session

    def login(self, request: UserLoginDTO) -> UserTokenDTO:
        user = self._user_repo.find_by_nim(request.nim)
        if user is None:
            raise ResourceMissing(f"No such user with nim {request.nim}.")

        if self._password_utils.verify(request.password, user.password) is False:
            raise AuthenticationException(f"Wrong password, try again.")

        token = self._jwt_utils.get_token(user)
        user.token = token.refresh_token

        self._session.commit()

        return token

    def refresh(self, refresh_token: str) -> str:
        payload = self._jwt_utils.verify(refresh_token)
        user_id = payload.get("sub")

        if user_id is None:
            raise AuthenticationException(f"Invalid JWT.")
        
        user = self._user_repo.find_by_id(user_id)

        if user is None:
            raise ResourceMissing(f"No such user with id {user_id}.")

        if user.token == refresh_token:
            return self._jwt_utils.create_access_token(user)
        else:
            raise AuthenticationException(f"Missing exact token, Invalid JWT.")

    def logout(self, refresh_token: str) -> bool:
        payload = self._jwt_utils.verify(refresh_token)
        user_id = payload.get("sub")
        
        if user_id is None:
            raise AuthenticationException(f"Invalid JWT.")
                
        user = self._user_repo.find_by_id(user_id)
        if user is None:
            raise ResourceMissing(f"No such user with id {user_id}.")

        user.token = None
        self._session.commit()
        
        return True



    