from pydantic import BaseModel, Field

class ProjectCreateSchema(BaseModel):
    name: str = Field(default="Новый проект", max_length=100)
    description: str = Field(default="")
    icon: str = Field(default="")

class ProjectUpdateSchema(BaseModel):
    name: str = Field(default="Новый проект", max_length=100)
    description: str = Field(default="")
    icon: str = Field(default="")