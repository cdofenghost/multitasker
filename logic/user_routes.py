from fastapi import APIRouter, Depends
from pytest import Session
from .users import UserController, UserRepository, UserService, UserIn
from ..database import get_db

router = APIRouter(prefix="/users")


def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)

def get_user_controller(user_service: UserService = Depends(get_user_service)):
    return UserController(user_service)

@router.post("/register",
             tags=["authorization"])
async def register(user_data: UserIn, controller: UserController = Depends(get_user_controller)):
    controller.register(user_data)
    pass