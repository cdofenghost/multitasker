from fastapi import UploadFile, APIRouter
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse

from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
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

@router.get("/attachments", response_model=AttachmentSchema)
def get_user_attachments(service: ServiceDependency,
                         user: UserDependency):
    return service.get_user_attachments(user.id)

@router.post("/", response_model=AttachmentSchema, status_code=201)
def add_attachment(file: UploadFile,
                   service: ServiceDependency,
                   user: UserDependency):
    
    if file.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Размер файла превышает 10МБ")
    
    relative_path = f"attachments/{user.id}"
    local_path = f"testapp/{relative_path}"
    if (not exists(local_path)):
        mkdir(local_path)
    
    with open(local_path + f"/{file.filename}", "wb+") as save_file:
        save_file.write(file.file.read())

    attachment = AttachmentCreateSchema(user_id=user.id, path=f"{relative_path}/{file.filename}")

    return service.add_attachment(attachment)

@router.get("/", response_class=FileResponse)
def get_attachment(attachment_id: int,
                   service: ServiceDependency,
                   user: UserDependency):
    attachment = service.get_attachment(attachment_id)

    return FileResponse(path=f"testapp/{attachment.path}", media_type='application/octet-stream')

@router.delete("/", status_code=204)
def delete_attachment(attachment_id: int,
                      service: ServiceDependency,
                      user: UserDependency):
    try:
        service.remove_attachment(attachment_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Файл с таким ID не найден.")
