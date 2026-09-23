from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
import uuid

class UserCreateDTO(BaseModel):
    nim: int
    name: str
    email: EmailStr
    contact: Optional[str] = None
    password: str

class UserFilterDTO(BaseModel):
    id: Optional[uuid.UUID] = None
    nim: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    contact: Optional[str] = None

class UserDTO(BaseModel):
    id: uuid.UUID
    nim: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

