from fastapi import UploadFile, APIRouter
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session
from os.path import exists
from os import mkdir

from ..schemas.attachment import AttachmentCreateSchema, AttachmentSchema

from .users import UserSchema
from .attachments import AttachmentRepository, AttachmentService
from ..database import get_db
from .tokens import get_current_user

MAX_FILE_SIZE = 10*1024*1024
router = APIRouter(prefix="/attachment", tags=["Attachments"])

def get_attachment_repository(db: Session = Depends(get_db)):
    return AttachmentRepository(db)

def get_attachment_service(user_repository: AttachmentRepository = Depends(get_attachment_repository)):
    return AttachmentService(user_repository)

ServiceDependency = Annotated[AttachmentService, Depends(get_attachment_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]

@router.get("/", response_model=AttachmentSchema)
def get_user_attachments(service: ServiceDependency,
                         user: UserDependency):
    return service.get_user_attachments(user.id)

@router.post("/", response_model=AttachmentSchema)
def add_attachment(file: UploadFile,
                   service: ServiceDependency,
                   user: UserDependency):
    
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Размер файла превышает 10МБ")
    
    path = f"testapp/attachments/{user.id}"
    if (not exists(path)):
        mkdir(path)
    
    with open(path + f"/{file.filename}", "wb+") as save_file:
        save_file.write(file.file.read())

    attachment = AttachmentCreateSchema(user_id=user.id, path=path)

    return service.add_attachment(attachment)

@router.delete("/", response_model=AttachmentSchema)
def delete_attachment(attachment_id: int,
                      service: ServiceDependency,
                      user: UserDependency):
    return service.remove_attachment(attachment_id)