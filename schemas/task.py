from pydantic import BaseModel, Field
from datetime import date

class TaskCreateSchema(BaseModel):
    performer_id: int = Field(gt=0)

    name: str = Field(default="Новая задача", max_length=100)
    description: str = Field(default="")
    deadline: date = Field()
    priority: int = Field(ge=1, le=4, default=1)

class TaskUpdateSchema(BaseModel):
    performer_id: int = Field(gt=0)
    
    name: str = Field(default="Новая задача", max_length=100)
    description: str = Field(default="")
    deadline: date = Field()
    priority: int = Field(ge=1, le=4, default=1)