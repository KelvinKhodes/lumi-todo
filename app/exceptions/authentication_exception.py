from app.exceptions.base_exception import BaseException

class AuthenticationException(BaseException):
    def __init__ (self, msg: str):
        super().__init__(msg, 401)
        