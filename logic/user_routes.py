from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.security import OAuth2PasswordRequestForm
#from fastapi.security import 
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from .restoring_codes import RestoringCodeCreateSchema, RestoringCodeUpdateSchema
from .users import UserRepository, UserService, UserCredentialSchema, UserProfileSchema
from .restoring_codes import RestoringCodeRepository, RestoringCodeService, RestoringCodeSchema
from ..database import get_db
from ..utils.sender import send_restoring_mail

from .tokens import generate_access_token, get_current_user, decode_token

router = APIRouter(prefix="/users",
                   tags=["User"])

# user_codes = {
#     # "user_email": "code"
# }

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)

def get_code_repository(db: Session = Depends(get_db)):
    return RestoringCodeRepository(db)

def get_code_service(code_repository: RestoringCodeRepository = Depends(get_code_repository)):
    return RestoringCodeService(code_repository)

ServiceDependency = Annotated[UserService, Depends(get_user_service)]
UserDependency = Annotated[dict, Depends(get_current_user)]

CodeServiceDependency = Annotated[RestoringCodeService, Depends(get_code_service)]

@router.post("/register")
async def register(user_data: UserCredentialSchema, 
                   service: ServiceDependency):
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


@router.get("/get", response_model=dict)
async def get_user(user: dict = Depends(get_current_user)):
    return user

@router.post("/verify-code")
async def verify_restoring_code(email: str, 
                                input_code: int, 
                                code_service: CodeServiceDependency,
                                service: ServiceDependency):
    
    try:
        existing_code = code_service.get_code_by_email(email)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Пользователь с таким email не запрашивал код или уже ввел его.")

    if existing_code.code is None:
        raise HTTPException(status_code=404, detail="Время действия кода истекло. Запросите новый код.")
    
    if input_code != existing_code.code:
        raise HTTPException(status_code=400, detail="Такого кода не существует")

    user = service.get_user_by_email(email)

    access_token = generate_access_token(user_id=user.id, email=email)

    used_code = code_service.get_code_by_email(user.email)
    code_service.remove_code(used_code)
    
    return {"access_token": access_token, "token_type": "bearer"}


# Токен
@router.put("/change-password")
async def change_password(service: ServiceDependency,
                          code_service: CodeServiceDependency,
                          token: str,
                          new_password: str = Query(min_length=8, max_length=16, pattern="^[A-Za-z0-9!#$%&*+-.<=>?@^_]+$")):
    payload = decode_token(token)

    user_id = payload.get("user_id")

    if user_id is None:
        print("Неверный токен")
        raise HTTPException(status_code=401, detail="Неверный токен")
    
    user = service.get_user(user_id)

    if user is None:
        print("Пользователь не найден")
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    
    existing_user = service.get_user(user_id)

    if existing_user is None:
        raise HTTPException(status_code=404, detail="Возникла ошибка: пользователь не найден")
    
    service.update_user_credentials(UserCredentialSchema(email=existing_user.email, password=new_password))

    return {"message": f"Пароль сменен на {new_password}"}


@router.post("/send-restoring-mail", response_model=RestoringCodeSchema)
async def send_restore_mail(email: str, 
                            service: ServiceDependency,
                            code_service: CodeServiceDependency):
    existing_user = service.get_user_by_email(email)

    if existing_user is None:
        raise HTTPException(status_code=404, detail="Пользователь с таким e-mail не зарегистрирован")

    code = send_restoring_mail(email)

    existing_code = code_service.get_code_by_email(user_email=email)

    if existing_code:
        result = code_service.update_code(RestoringCodeSchema(id=existing_code.id, user_email=email, code=code))
        return result
    
    result = code_service.add_code(RestoringCodeCreateSchema(user_email=email, code=code))

    return result