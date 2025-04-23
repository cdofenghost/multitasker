from pydantic import BaseModel, Field
from datetime import datetime

class SubtaskSchema(BaseModel):
    id: int = Field()
    name: str = Field(default="Новая задача", max_length=100)
    author_id: int = Field()
    performer_id: int = Field()
    task_id: int = Field()
    deadline: datetime = Field()
    date_created: datetime = Field()
    date_updated: datetime = Field()
    priority: int = Field(ge=1, le=4, default=1)
    status: int = Field(ge=1, le=4, default=1)
    description: str = Field(default="")

class SubtaskCreateSchema(BaseModel):
    performer_id: int = Field(gt=0)

    name: str = Field(default="Новая задача", max_length=100)
    performer_id: int = Field()
    description: str = Field(default="")
    deadline: datetime = Field()
    priority: int = Field(ge=1, le=4, default=1)

class SubtaskUpdateSchema(BaseModel):
    performer_id: int = Field(gt=0)
    
    name: str = Field(default="Новая задача", max_length=100)
    description: str = Field(default="")
    deadline: datetime = Field()
    status: int = Field(ge=1, le=4, default=1)
    priority: int = Field(ge=1, le=4, default=1)