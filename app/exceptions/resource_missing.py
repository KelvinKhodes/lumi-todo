from app.exceptions.base_exception import BaseException

class ResourceMissing(BaseException):
    def __init__ (self, msg: str):
            super().__init__(msg, 404)
        