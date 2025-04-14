from pydantic import BaseModel, Field

class CategorySchema(BaseModel):
    id: int = Field()
    name: str = Field()
    color: str = Field()
    user_id: int = Field()

class CategoryCreateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100, default="Новая категория")
    color: str = Field(pattern="^#(?:[0-9a-fA-F]{3}){1,2}$")

class CategoryUpdateSchema(BaseModel):
    name: str = Field(min_length=1, max_length=100, default="Новая категория")
    color: str = Field(pattern="^#(?:[0-9a-fA-F]{3}){1,2}$")