from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime
from app.models.enums.task_status import TaskStatus
import uuid

class CourseTaskCreateDTO(BaseModel):
    title: str
    description: Optional[str] = None
    course_id: uuid.UUID
    start_at: datetime
    end_at: datetime

class CourseTaskFilterDTO(BaseModel):
    id: Optional[uuid.UUID] = None
    title: Optional[str] = None
    status: Optional[TaskStatus] = None
    user_id: Optional[uuid.UUID] = None
    course_id: Optional[uuid.UUID] = None

class CourseTaskDTO(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    status: TaskStatus
    course_name: str
    start_at: datetime
    finish_at: datetime | None
    end_at: datetime

    model_config = ConfigDict(from_attributes=True)

