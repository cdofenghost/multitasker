from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from .users import UserRepository, UserService, UserCredentialSchema, UserProfileSchema
from ..database import get_db
from ..utils.sender import send_restoring_mail

from .tokens import generate_access_token, get_current_user

router = APIRouter(prefix="/users",
                   tags=["User"])

# user_codes = {
#     # "user_email": "code"
# }

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)


@router.post("/register")
async def register(user_data: UserCredentialSchema, service: UserService = Depends(get_user_service)):
    user = service.register_user(user_data)

    return {"id": user.id, "name": user.name, "email": user.email}


@router.post("/authorize")
async def authorize(form_data: Annotated[OAuth2PasswordRequestForm, Depends()], service: UserService = Depends(get_user_service)):
    user_data = UserCredentialSchema(email=form_data.username, password=form_data.password)
    result = service.verify_credentials(user_data)

    if result == 404:
        raise HTTPException(status_code=404, detail="Пользователь с таким e-mail не зарегистрирован")

    if result == 403:
        raise HTTPException(status_code=403, detail="Введен неверный пароль")
    
    token = generate_access_token(result.id, result.email)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/get")
async def get_user(user: dict = Depends(get_current_user)):
    return user


@router.put("/change-password")
async def change_password(user_data: UserCredentialSchema, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_email(user_data.email)
    service.update_user_credentials()

    return {"message": f"Пароль сменен на {user_data.password}"}


@router.post("/send-restoring-mail",
             tags=["User"])
async def send_restore_mail(email: str, service: UserService = Depends(get_user_service)):
    existing_user = service.get_user_by_email(email)

    if existing_user is None:
        raise HTTPException(status_code=404, detail="Пользователь с таким e-mail не зарегистрирован")
    
    code = send_restoring_mail(email)

    return {"email": email, "code": code}
