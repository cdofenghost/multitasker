import datetime
from fastapi import APIRouter, Depends, HTTPException, Response, UploadFile
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from ..schemas.user import UserCredentialSchema
from .users import UserRepository, UserService, UserSchema, UserProfileUpdateSchema
from .attachments import AttachmentService, AttachmentRepository, AttachmentCreateSchema
from ..database import get_db
from ..schemas.project import ProjectCreateSchema, ProjectUpdateSchema
from os.path import exists
from os import mkdir

from .tokens import get_current_user, decode_token

MAX_FILE_SIZE = 10*1024*1024

router = APIRouter(prefix="/profile",
                   tags=["Profile"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/authorize")

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)

def get_attachment_repository(db: Session = Depends(get_db)):
    return AttachmentRepository(db)

def get_attachment_service(user_repository: UserRepository = Depends(get_attachment_repository)):
    return AttachmentService(user_repository)


UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
AttachmentServiceDependency = Annotated[AttachmentService, Depends(get_user_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]

@router.put("/update")
async def change_user_data(user_data: UserProfileUpdateSchema, 
                           service: UserServiceDependency,
                           user: UserDependency):
    return service.update_user_in_profile(user.id, user_data)

@router.put("/update-icon", response_model=UserSchema)
async def change_user_icon(icon: UploadFile,
                           user_service: UserServiceDependency,
                           attachment_service: AttachmentServiceDependency,
                           user: UserDependency):
    if icon.size > MAX_FILE_SIZE:
        raise HTTPException(status_code=400, detail="Размер файла превышает 10МБ")
    
    path = f"testapp/attachments/{user.id}"
    if (not exists(path)):
        mkdir(path)
    
    with open(path + f"/{icon.filename}", "wb+") as save_file:
        save_file.write(icon.file.read())

    attachment_service.add_attachment(AttachmentCreateSchema(user.id, icon.filename))
    return user_service.update_user_in_profile(user.id, UserProfileUpdateSchema(email=user.email, name=user.name, icon=icon.filename))


@router.put("/update-password", response_model=UserSchema)
async def change_user_password(new_password: str,
                               service: UserServiceDependency,
                               user: UserDependency):
    return service.update_user_credentials(user.id, UserCredentialSchema(email=user.email, password=new_password))


@router.post("/logout", response_model=dict)
def logout(user: UserDependency,
           service: UserServiceDependency,
           response: Response):
    locked_in_user = service.get_user(user.id)
    response.delete_cookie("token")

    return {"message": f"Пользователь {locked_in_user.name} разлогинился."}