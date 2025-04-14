from pydantic import BaseModel, Field

class ProjectSchema(BaseModel):
    id: int = Field()
    name: str = Field(default="Новый проект", max_length=100)
    description: str = Field(default="")
    icon: str = Field(default="testapp/attachments/default-icon.jpg")
    category_id: int = Field()

class ProjectCreateSchema(BaseModel):
    name: str = Field(default="Новый проект", max_length=100)
    description: str = Field(default="")
    category_id: int = Field()

class ProjectUpdateSchema(BaseModel):
    name: str = Field(default="Новый проект", max_length=100)
    description: str = Field(default="")