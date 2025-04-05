import datetime
from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from typing import Annotated

from .users import UserRepository, UserService, UserSchema, UserProfileUpdateSchema
from ..database import get_db
from ..schemas.project import ProjectCreateSchema, ProjectUpdateSchema

from .tokens import get_current_user, decode_token

router = APIRouter(prefix="/profile",
                   tags=["Profile"])

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/authorize")

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]

@router.put("/update")
async def change_user_data(user_data: UserProfileUpdateSchema, 
                           service: UserServiceDependency,
                           user: UserDependency):
    return service.update_user_in_profile(user.id, user_data)


@router.put("/update-password")
async def change_user_password(category_id: int,
                               service: UserServiceDependency,
                               user: UserDependency):
    pass


@router.post("/logout", response_model=dict)
def logout(user: UserDependency,
           service: UserServiceDependency,
           response: Response):
    locked_in_user = service.get_user(user.id)
    response.delete_cookie("token")

    return {"message": f"Пользователь {locked_in_user.name} разлогинился."}