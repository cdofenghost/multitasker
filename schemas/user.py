from pydantic import BaseModel, EmailStr, Field

class UserSchema(BaseModel):
    id: int = Field()
    email: EmailStr = Field(pattern="^[a-zA-Z0-9-_.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    hashed_password: str = Field()
    name: str = Field(pattern="[А-Яа-яA-Za-z0-9]+", min_length=2, max_length=50)
    icon: str = Field()

class UserProfileSchema(BaseModel):
    id: int = Field()
    email: EmailStr = Field(pattern="^[a-zA-Z0-9-_.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    name: str = Field(pattern="[А-Яа-яA-Za-z0-9]+", min_length=2, max_length=50)
    icon: str = Field()

class UserProfileUpdateSchema(BaseModel):
    email: EmailStr = Field(pattern="^[a-zA-Z0-9-_.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(pattern="^[a-zA-Z0-9!#$%&*+.<=>?@^_]+$", min_length=8, max_length=16)
    name: str = Field(pattern="[А-Яа-яA-Za-z0-9]+", min_length=2, max_length=50)
    icon: str = Field()

class UserCredentialSchema(BaseModel):
    email: EmailStr = Field(pattern="^[a-zA-Z0-9-_.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
    password: str = Field(pattern="^[a-zA-Z0-9!#$%&*+.<=>?@^_]+$", min_length=8, max_length=16)