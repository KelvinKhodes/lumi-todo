from pydantic import BaseModel, ConfigDict
from typing import Optional
import uuid

class CourseCreateDTO(BaseModel):
    name: str
    lecturer_id: uuid.UUID

class CourseFilterDTO(BaseModel):
    id: Optional[uuid.UUID] = None
    name: Optional[str] = None
    lecturer_id: Optional[uuid.UUID] = None

class CourseDTO(BaseModel):
    id: uuid.UUID
    name: str
    lecturer_id: uuid.UUID

    model_config = ConfigDict(from_attributes=True)

