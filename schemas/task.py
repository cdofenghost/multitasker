from pydantic import BaseModel, Field
from datetime import datetime

class TaskSchema(BaseModel):
    id: int = Field()
    name: str = Field(default="Новая задача", max_length=100)
    author_id: int = Field()
    performer_id: int = Field()
    project_id: int = Field()
    deadline: datetime = Field()
    date_created: datetime = Field()
    date_updated: datetime = Field()
    priority: int = Field(ge=1, le=4, default=1)
    status: int = Field(ge=1, le=4, default=1)
    description: str = Field(default="")

class TaskCreateSchema(BaseModel):
    performer_id: int = Field(gt=0)

    name: str = Field(default="Новая задача", max_length=100)
    performer_id: int = Field()
    description: str = Field(default="")
    deadline: datetime = Field()
    priority: int = Field(ge=1, le=4, default=1)

class TaskUpdateSchema(BaseModel):
    performer_id: int = Field(gt=0)
    
    name: str = Field(default="Новая задача", max_length=100)
    description: str = Field(default="")
    deadline: datetime = Field()
    status: int = Field(ge=1, le=4, default=1)
    priority: int = Field(ge=1, le=4, default=1)