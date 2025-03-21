from fastapi.security import OAuth2PasswordBearer
from fastapi import Security, HTTPException, Depends

import jwt
import datetime
import uuid
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from ..models.user import User
from ..database import get_db
from ..utils.secret_data import TOKEN_ALGORITHM, SECRET_TOKEN_KEY

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/authorize")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def generate_access_token(user_id: int, email: str) -> str:
    expires = datetime.datetime.now() + datetime.timedelta(minutes=20)
    encode = {'sub': email, 'user_id': user_id, 'exp': expires}

    return jwt.encode(encode, SECRET_TOKEN_KEY, algorithm=TOKEN_ALGORITHM)


async def get_current_user(token: str = Security(oauth2_scheme), db: Session = Depends(get_db)):
    try:
        payload = jwt.decode(token, SECRET_TOKEN_KEY, algorithms=[TOKEN_ALGORITHM])
        user_id: int = payload.get("user_id")

        if user_id is None:
            print("Неверный токен")
            raise HTTPException(status_code=401, detail="Неверный токен")
        
        user = db.query(User).filter(User.id == user_id).first()

        if user is None:
            print("Пользователь не найден")
            raise HTTPException(status_code=404, detail="Пользователь не найден")
        
        return {"name": user.name, "user_id": user_id, "email": user.email}
    
    except jwt.ExpiredSignatureError:
        print("Токен истек")
        raise HTTPException(status_code=401, detail="Токен истек")
    except jwt.InvalidTokenError:
        print("Недействительный токен")
        raise HTTPException(status_code=401, detail="Недействительный токен")

# def revoke_refresh_token(refresh_token: str, db: Session):
#     revoked_token = RevokedToken(token=refresh_token, revoked_at=datetime.datetime.utcnow())

#     db.add(revoked_token)
#     db.commit()
    
#     return {"message": "Токен отозван"}
