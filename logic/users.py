from sqlalchemy.orm import Session

from email_validator import validate_email
from passlib.hash import bcrypt

from ..models.user import User
from ..schemas.user import UserIn

class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def add_user(self, user: User) -> User:
        print("Положил")
        self.db.add(user)
        self.db.commit()
        return user

    def find_user(self, id: int) -> User | None:
        return self.db.query(User).filter(User.id == id).first()
    
    def get_users(self, db: Session) -> list[User]:
        return db.query(User).all()   
    
    def remove_user(self, id: int, db: Session) -> User | None:
        return db.query(User).filter(User.id == id).delete()
    
    def update_user(self, user: User) -> User:
        self.db.refresh(user)
        self.db.commit()
        return user


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def __to_user(self, user_data: UserIn):
        hashed_password = bcrypt.hash(user_data.password)
        return User(name=user_data.name, email=user_data.email, hashed_password=hashed_password)


    def register_user(self, user_data: UserIn) -> User | None:
        print("Обработал")

        user = self.__to_user(user_data)
        existing_user = self.user_repository.find_user(user.id)

        validated_email = validate_email(check_deliverability=True)

        if existing_user:
            return None
        
        return self.user_repository.add_user(user)

    def find_user(self, id: int):
        return self.user_repository.find_user(id)
    
    def remove_user(self, id: int):
        return self.user_repository.remove_user(id)

    def update_user(self, user_data: UserIn) -> User | None:
        user = self.__to_user(user_data)
        existing_user = self.user_repository.find_user(user.id)

        if existing_user is None:
            return None
        
        return self.user_repository.update_user(user)



    