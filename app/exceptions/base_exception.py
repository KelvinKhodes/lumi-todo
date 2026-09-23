class BaseException(Exception):
   def __init__ (self, msg: str, status_code: int):
        super().__init__
        self.message = msg
        self.status_code = status_code 