from pydantic import BaseModel, Field
from datetime import date

class SubtaskCreateSchema(BaseModel):
    author_id: int = Field(gt=0)
    performer_id: int = Field(gt=0)

    name: str = Field(default="Новый проект", max_length=100)
    description: str = Field(default="")
    deadline: date = Field()
    priority: int = Field(ge=1, le=4, default=1)

class SubtaskUpdateSchema(BaseModel):
    performer_id: int = Field(gt=0)
    
    name: str = Field(default="Новый проект", max_length=100)
    description: str = Field(default="")
    deadline: date = Field()
    priority: int = Field(ge=1, le=4, default=1)