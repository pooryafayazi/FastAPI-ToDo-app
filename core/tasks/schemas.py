from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class TaskBaseSchema(BaseModel):
    title: str = Field(..., min_length=3, max_length=150, description="this is title")
    description: Optional[str] = Field(None, min_length=3, max_length=500, description="this is description")
    is_completed: bool = False
    

class TaskCreateSchema(TaskBaseSchema):
    pass


class TaskUpdateSchema(TaskBaseSchema):
    pass


class TaskResponseSchema(BaseModel):
    id: int
    title: str
    description: str | None = None
    is_completed: bool
    create_date: datetime | None = None
    updated_date: datetime | None = None

    model_config = {"from_attributes": True}
