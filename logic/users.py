from sqlalchemy.orm import Session

from email_validator import validate_email
from passlib.hash import bcrypt

from ..models.user import User
from ..schemas.user import UserCredentialSchema, UserProfileSchema


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
    
    def find_user_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()
    
    def get_users(self) -> list[User]:
        return self.db.query(User).all()   
    
    def remove_user(self, id: int) -> User | None:
        return self.db.query(User).filter(User.id == id).delete()
    
    def update_user(self, user: User) -> User:
        self.db.merge(user)
        self.db.commit()
        return user


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def __to_user(self, user_data: UserCredentialSchema):
        hashed_password = bcrypt.hash(user_data.password)
        return User(email=user_data.email, hashed_password=hashed_password)


    def register_user(self, user_data: UserCredentialSchema) -> User | None:
        user = self.__to_user(user_data)
        existing_user = self.user_repository.find_user(user.id)

        validate_email(user.email, check_deliverability=True)

        if existing_user:
            return None
        
        return self.user_repository.add_user(user)

    def get_user(self, id: int):
        return self.user_repository.find_user(id)
    
    def verify_credentials(self, user_data: UserCredentialSchema) -> User | int:
        existing_user = self.get_user_by_email(user_data.email)
        
        if existing_user is None:
            return 404
        
        if bcrypt.verify(user_data.password, existing_user.hashed_password):
            return existing_user
        
        else:
            return 403

    
    def get_user_by_email(self, email: str):
        return self.user_repository.find_user_by_email(email)
    
    def remove_user(self, id: int):
        return self.user_repository.remove_user(id)

    def update_user_credentials(self, user_data: UserCredentialSchema) -> User | None:
        existing_user = self.user_repository.find_user_by_email(user_data.email)

        if existing_user is None:
            return None
        
        existing_user.hashed_password = bcrypt.hash(user_data.password)
        existing_user.email = user_data.email
        
        return self.user_repository.update_user(existing_user)

    def restore_access(self, email: str) -> User | None:
        existing_user = self.user_repository.find_user_by_email(email)

        if existing_user is None:
            return None




    