from pydantic import BaseModel, EmailStr, Field
from datetime import date

class RestoringCodeSchema(BaseModel):
    code_id: int = Field()
    user_email: EmailStr = Field()
    code: int = Field(gt=999, lt=10000)

class RestoringCodeCreateSchema(BaseModel):
    user_email: EmailStr = Field()
    code: int = Field(gt=999, lt=10000)

class RestoringCodeUpdateSchema(BaseModel):
    user_email: EmailStr = Field()
    code: int = Field(gt=999, lt=10000)

class RestoringCodeRevokeSchema(BaseModel):
    user_email: EmailStr = Field()