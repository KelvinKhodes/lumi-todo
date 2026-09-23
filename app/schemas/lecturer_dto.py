from pydantic import BaseModel, EmailStr, ConfigDict
from typing import Optional
import uuid

class LecturerCreateDTO(BaseModel):
    nip: int
    name: str
    email: EmailStr
    contact: Optional[str] = None

class LecturerFilterDTO(BaseModel):
    id: Optional[uuid.UUID] = None
    nip: Optional[int] = None
    name: Optional[str] = None
    email: Optional[str] = None
    contact: Optional[str] = None

class LecturerDTO(BaseModel):
    id: uuid.UUID
    nip: int
    name: str
    email: EmailStr

    model_config = ConfigDict(from_attributes=True)

