from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
import uuid

class UserLoginDTO(BaseModel):
    nim: int
    password: str
    
class UserTokenDTO(BaseModel):
    access_token: str
    refresh_token: str


