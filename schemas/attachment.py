from pydantic import BaseModel, Field

class AttachmentCreateSchema(BaseModel):
    user_id: int
    path: str

class AttachmentUpdateSchema(BaseModel):
    user_id: int
    path: str

class AttachmentSchema(BaseModel):
    id: int
    user_id: int
    path: str