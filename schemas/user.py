from pydantic import BaseModel, EmailStr, Field

class UserProfileSchema(BaseModel):
    email: EmailStr = Field(pattern="^[a-zA-Z0-9-_.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(pattern="^[a-zA-Z0-9!#$%&*+.<=>?@^_]+$", min_length=8, max_length=16)
    name: str = Field(pattern="[А-Яа-яA-Za-z0-9]+", min_length=2, max_length=50)
    icon: str = Field()

class UserCredentialSchema(BaseModel):
    email: EmailStr = Field(pattern="^[a-zA-Z0-9-_.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(pattern="^[a-zA-Z0-9!#$%&*+.<=>?@^_]+$", min_length=8, max_length=16)