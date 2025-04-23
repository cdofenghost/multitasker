from fastapi.security import OAuth2PasswordBearer
from fastapi import Request, Security, HTTPException, Depends

import jwt
import datetime
import uuid
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..schemas.user import UserSchema, BaseModel
from ..models.user import User
from ..database import get_db
from ..utils.secret_data import TOKEN_ALGORITHM, SECRET_TOKEN_KEY
from ..models.revoked_token import RevokedToken

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/authorize")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_access_token(user_id: int, email: str) -> str:
    expires = datetime.datetime.now() + datetime.timedelta(minutes=20)
    encode = {'sub': email, 'user_id': user_id, 'exp': expires}

    return jwt.encode(encode, SECRET_TOKEN_KEY, algorithm=TOKEN_ALGORITHM)

async def get_current_user(request: Request,
                           # token: str = Security(oauth2_scheme), 
                           db: Session = Depends(get_db)) -> UserSchema:
    try:
        cookie_token = request.cookies.get("token")

        payload_header = jwt.decode(cookie_token, SECRET_TOKEN_KEY, algorithms=[TOKEN_ALGORITHM])
        # payload_cookie = jwt.decode(cookie_token, SECRET_TOKEN_KEY, algorithms=[TOKEN_ALGORITHM])

        user_id: int = payload_header.get("user_id")
        # user_id: 
    
        if not db.query(RevokedToken).filter(RevokedToken.token == cookie_token).first() is None:
            raise HTTPException(status_code=403, detail="Токен, который вы используете, больше не активен.")
        
        if user_id is None:
            print("Неверный токен")
            raise HTTPException(status_code=401, detail="Неверный токен")
        
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            print("Пользователь не найден")
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        return UserSchema(id=user.id, email=user.email, hashed_password=user.hashed_password, name=user.name, icon=user.icon)
    
    except jwt.ExpiredSignatureError:
        print("Токен истек")
        raise HTTPException(status_code=401, detail="Токен истек")
    except jwt.InvalidTokenError:
        print("Недействительный токен")
        raise HTTPException(status_code=401, detail="Недействительный токен")

def decode_token(token: str):
    return jwt.decode(token, SECRET_TOKEN_KEY, algorithms=[TOKEN_ALGORITHM])

async def revoke_refresh_token(refresh_token: str, db: Session = Depends(get_db)):
    revoked_token = RevokedToken(token=refresh_token, revoked_at=datetime.datetime.now())

    db.add(revoked_token)
    db.commit()
    
    return {"message": "Токен отозван"}

