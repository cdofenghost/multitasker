from fastapi import APIRouter, Depends
from pytest import Session
from .users import UserRepository, UserService, UserIn
from ..database import get_db

router = APIRouter(prefix="/users")


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)


@router.post("/register",
             tags=["authorization"])
async def register(user_data: UserIn, service: UserService = Depends(get_user_service)):
    user = service.register_user(user_data)

    return {"id": user.id, "name": user.name, "email": user.email}


@router.post("/register",
             tags=["authorization"])
async def register(user_data: UserIn, service: UserService = Depends(get_user_service)):
    user = service.register_user(user_data)

    return {"id": user.id, "name": user.name, "email": user.email}