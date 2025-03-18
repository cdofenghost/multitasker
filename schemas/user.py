from pydantic import BaseModel, EmailStr, Field

class UserIn(BaseModel):
    email: EmailStr = Field(pattern="^[a-zA-Z0-9-_.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(pattern="^[a-zA-Z0-9-_.]+$", min_length=8, max_length=16)
    name: str = Field(pattern="[А-Яа-яA-Za-z]+", min_length=2, max_length=50)