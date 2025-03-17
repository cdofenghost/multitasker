from fastapi import Depends
from sqlalchemy.orm import Session

from email_validator import validate_email
from passlib.hash import bcrypt

from ..models.user import User
from ..schemas.user import UserIn

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, user: User) -> bool:
        print("Положил")
        self.db.add(user)
        self.db.commit()
        pass

    def find_user(self, user: User) -> User | None:
        pass

    def get_users(self, db: Session) -> list[User]:
        #users = db.query(User).all()
        #return users
        pass
    
    def remove_user(self, user_data: User, db: Session) -> User | None:
        #db.query(User).delete(user_data)
        pass


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def __to_user(self, user_data: UserIn):
        hashed_password = bcrypt.hash(user_data.password)
        return User(name=user_data.name, email=user_data.email, hashed_password=hashed_password)

    def register_user(self, user_data: UserIn):
        print("Обработал")
        user = self.__to_user(user_data)
        self.user_repository.add_user(user)


class UserController:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register(self, user_data: UserIn):
        print("Принял")
        self.user_service.register_user(user_data)



    