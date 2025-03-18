from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .users import UserRepository, UserService, UserIn
from ..database import get_db
from ..utils.sender import send_restoring_mail

router = APIRouter(prefix="/users")

# user_codes = {
#     # "user_email": "code"
# }

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)


@router.post("/register",
             tags=["User"])
async def register(user_data: UserIn, service: UserService = Depends(get_user_service)):
    user = service.register_user(user_data)

    return {"id": user.id, "name": user.name, "email": user.email}


@router.post("/authorize",
             tags=["User"])
async def authorize(user_data: UserIn, service: UserService = Depends(get_user_service)):
    result = service.verify_credentials(user_data)

    if result == 404:
        raise HTTPException(status_code=404, detail="Пользователь с таким e-mail не зарегистрирован")

    if result == 403:
        raise HTTPException(status_code=403, detail="Введен неверный пароль")

    return {"id": result.id, "name": result.name, "email": result.email}


@router.put("/change-password",
             tags=["User"])
async def change_password(email: str, new_password: str, service: UserService = Depends(get_user_service)):
    user = service.get_user_by_email(email)
    service.update_user_credentials(UserIn(email=user.email, name=user.name, password=new_password))

    return {"message": f"Пароль сменен на {new_password}"}


@router.post("/send-restoring-mail",
             tags=["User"])
async def send_restore_mail(email: str, service: UserService = Depends(get_user_service)):
    existing_user = service.get_user_by_email(email)

    if existing_user is None:
        raise HTTPException(status_code=404, detail="Пользователь с таким e-mail не зарегистрирован")
    
    code = send_restoring_mail(email)

    return {"email": email, "code": code}
