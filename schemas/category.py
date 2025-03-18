from pydantic import BaseModel, Field

class Category(BaseModel):
    name: str = Field(max_length=100)
    color: str = Field(pattern="^#(?:[0-9a-fA-F]{3}){1,2}$")
    description: str = Field()