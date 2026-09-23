from app.exceptions.base_exception import BaseException

class DuplicateEntity(BaseException):
    def __init__ (self, msg: str):
        super().__init__(msg, 400)