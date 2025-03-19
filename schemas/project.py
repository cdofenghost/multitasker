from pydantic import BaseModel, Field

class Project(BaseModel):
    name: str = Field(default="Новый проект", max_length=100)
    description: str = Field(default="")
    icon: str = Field(default="")