from pydantic import BaseModel, Field

class CategoryCreateSchema(BaseModel):
    name: str = Field(max_length=100, default="Новая категория")
    color: str = Field(pattern="^#(?:[0-9a-fA-F]{3}){1,2}$")

class CategoryUpdateSchema(BaseModel):
    name: str = Field(max_length=100, default="Новая категория")
    color: str = Field(pattern="^#(?:[0-9a-fA-F]{3}){1,2}$")