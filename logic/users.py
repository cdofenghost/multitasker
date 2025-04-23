from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound

from email_validator import validate_email
from passlib.hash import bcrypt

from ..models.user import User
from ..schemas.user import UserCredentialSchema, UserProfileUpdateSchema, UserProfileSchema, UserSchema
from ..utils.utils import generate_name
from ..utils.secret_data import DEFAULT_ICON_PATH
from .exceptions import IncorrectPasswordError

# + таблица ResetCodes
class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def __to_new_user(self, user_data: UserCredentialSchema):
        hashed_password = bcrypt.hash(user_data.password)
        return User(email=user_data.email, name=generate_name(), hashed_password=hashed_password, icon=DEFAULT_ICON_PATH)
    
    # def __to_user(self, user_data: UserProfileSchema):
    #     user = User(id=user_data.id, name=user_data.name, email=user_data.email, icon=user_data.icon)

    #     return user
    

    def add_user(self, user_schema: UserCredentialSchema) -> UserSchema:
        user = self.__to_new_user(user_schema)

        self.db.add(user)
        self.db.commit()

        return UserSchema(id=user.id, name=user.name, email=user.email, hashed_password=user.hashed_password, icon=user.icon)

    def find_user(self, id: int) -> UserSchema:
        user = self.db.query(User).filter(User.id == id).first()

        if user is None:
            raise NoResultFound()
            
        return UserSchema(id=user.id, name=user.name, email=user.email, hashed_password=user.hashed_password, icon=user.icon)
    
    def find_user_by_email(self, email: str) -> UserSchema:
        user = self.db.query(User).filter(User.email == email).first()

        if user is None:
            raise NoResultFound()
        
        return UserSchema(id=user.id, name=user.name, email=user.email, hashed_password=user.hashed_password, icon=user.icon)
    
    def get_users(self) -> list[UserSchema]:
        users = list(self.db.query(User).all())

        return [UserSchema(id=user.id, name=user.name, email=user.email, hashed_password=user.hashed_password, icon=user.icon)
                for user in users]
    
    def remove_user(self, id: int) -> UserSchema:
        user = self.db.query(User).filter(User.id == id).first()

        if user is None:
            raise NoResultFound()
        
        self.db.delete(user)

        return UserSchema(id=user.id, name=user.name, email=user.email, hashed_password=user.hashed_password, icon=user.icon)
    
    def update_user(self, user_id: int, user_schema: UserProfileUpdateSchema | UserCredentialSchema) -> UserSchema:
        user = self.db.query(User).filter(User.id == user_id).first()

        if type(user_schema) is UserCredentialSchema:
            user.email = user_schema.email
            user.hashed_password = bcrypt.hash(user_schema.password)

        if type(user_schema) is UserProfileUpdateSchema:
            user.email = user_schema.email
            user.name = user_schema.name
            user.icon = user_schema.icon

        self.db.merge(user)
        self.db.commit()

        return user
    
    def change_user_role(self, user_id: int, role: str):
        user = self.find_user(user_id)

        user.role = role

        self.db.merge(user)
        self.db.commit()

        return UserSchema(id=user.id, name=user.name, email=user.email, hashed_password=user.hashed_password, icon=user.icon)


class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def register_user(self, user_data: UserCredentialSchema) -> UserSchema:
        validate_email(user_data.email, check_deliverability=True)
        
        return self.user_repository.add_user(user_data)

    def get_user(self, user_id: int) -> UserSchema:
        return self.user_repository.find_user(user_id)
    
    def verify_credentials(self, user_data: UserCredentialSchema) -> UserSchema:
        existing_user = self.get_user_by_email(email=user_data.email)

        if not bcrypt.verify(user_data.password, existing_user.hashed_password):
            raise IncorrectPasswordError
        
        return existing_user
        
    def get_user_by_email(self, email: str) -> UserSchema:
        return self.user_repository.find_user_by_email(email)
    
    def remove_user(self, id: int) -> UserSchema:
        return self.user_repository.remove_user(id)

    def update_user_credentials(self, user_id: int, user_data: UserCredentialSchema) -> UserSchema:
        return self.user_repository.update_user(user_id, user_data)
        
    def update_user_in_profile(self, user_id: int, user_data: UserProfileUpdateSchema) -> UserSchema:
        existing_user = self.user_repository.find_user(user_id)

        return self.user_repository.update_user(user_id=user_id, user_schema=user_data)

    def change_user_role(self, user_id: int, user_role: str) -> UserSchema:
        return self.user_repository.change_user_role(user_id, user_role)





    