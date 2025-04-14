from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Query, Request, Response
from fastapi.security import OAuth2PasswordRequestForm
#from fastapi.security import 
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from email_validator import EmailUndeliverableError

from .exceptions import IncorrectPasswordError

from .restoring_codes import RestoringCodeCreateSchema, RestoringCodeUpdateSchema
from .users import UserRepository, UserService, UserCredentialSchema, UserProfileUpdateSchema, UserSchema
from .restoring_codes import RestoringCodeRepository, RestoringCodeService, RestoringCodeSchema
from ..database import get_db
from ..utils.sender import send_restoring_mail, send_invitation_mail

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
    
    try:
        existing_user = service.get_user_by_email(email=user_data.email)
        raise HTTPException(status_code=400, detail="Пользователь с таким email уже зарегистирован! Попробуйте авторизоваться.")
    
    except NoResultFound:
        try:
            user = service.register_user(user_data)

        except EmailUndeliverableError as e:
            raise HTTPException(status_code=418, detail=e.args[0])

        return {"id": user.id, "name": user.name, "email": user.email}


@router.post("/authorize", response_model=dict)
async def authorize(form_data: UserCredentialSchema, #OAuth2PasswordRequestForm
                    service: ServiceDependency,
                    response: Response):
    try:
        result = service.verify_credentials(form_data)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Пользователь с таким e-mail не зарегистрирован")

    except IncorrectPasswordError:
        raise HTTPException(status_code=403, detail="Введен неверный пароль")
    
    token = generate_access_token(result.id, result.email)
    response.set_cookie("token", token)

    return {"access_token": token, "token_type": "bearer"}


@router.get("/get", response_model=UserSchema)
async def get_user(user: UserSchema = Depends(get_current_user)):
    return user

@router.get("/", response_model=UserSchema)
async def get_user_by_id(user_id: int, service: ServiceDependency, user: UserSchema = Depends(get_current_user)):
    return service.get_user(user_id)

@router.get("/by-email", response_model=UserSchema)
async def get_user_by_email(email: str, service: ServiceDependency, send_notification: bool = False, user: UserSchema = Depends(get_current_user)):
    try:
        user = service.get_user_by_email(email)
        return user
    except NoResultFound:
        if send_notification:
            send_invitation_mail(user, email)
            raise HTTPException(status_code=200, detail="Пользователю было отправлено приглашение на регистрацию.")
        raise HTTPException(status_code=404, detail="Пользователь с таким e-mail'ом не был найден.")

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
@router.put("/change-password", response_model=dict)
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
    
    service.update_user_credentials(user_id, UserCredentialSchema(email=existing_user.email, password=new_password))

    return {"message": f"Пароль сменен на {new_password}"}


@router.post("/send-restoring-mail", response_model=RestoringCodeSchema)
async def send_restore_mail(email: str, 
                            service: ServiceDependency,
                            code_service: CodeServiceDependency):
    existing_user = service.get_user_by_email(email)

    if existing_user is None:
        raise HTTPException(status_code=404, detail="Пользователь с таким e-mail не зарегистрирован")

    code = send_restoring_mail(email)

    try:
        existing_code = code_service.get_code_by_email(user_email=email)
        result = code_service.update_code(RestoringCodeSchema(id=existing_code.id, user_email=email, code=code))

    except NoResultFound:
        result = code_service.add_code(RestoringCodeCreateSchema(user_email=email, code=code))

    return result