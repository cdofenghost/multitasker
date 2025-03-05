from fastapi import APIRouter, Body, Depends, HTTPException, Query, Form
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session

from pydantic import EmailStr
from email_validator import validate_email
from passlib.hash import bcrypt

from ..database import get_db
from ..models.user import User
from ..schemas.user import UserIn, DBUser

router = APIRouter(prefix="/users")

def hash_password(password: str) -> str:
    return bcrypt.hash(password)

def user_to_db(db_user: DBUser) -> User:
    return User(email=db_user.email, name=db_user.name, hashed_password=db_user.hashed_password)

def create_db_user(user_in: UserIn) -> DBUser:
    hashed_password = hash_password(user_in.password)
    db_user = DBUser(**user_in.model_dump(), hashed_password=hashed_password)

    return db_user

@router.get("/")
async def get_users(db: Session=Depends(get_db)):
    users = db.query(User).all()
    return users

@router.post("/register",
             tags=["authorization"])
async def register(email: EmailStr = Body(embed=True, pattern="^[a-zA-Z0-9-_.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
                   password: str = Body(embed=True, pattern="^[a-zA-Z0-9-_.]+$", min_length=8, max_length=16),
                   repeatPassword: str = Body(embed=True, pattern="^[a-zA-Z0-9!#$%&*+-.<=>?@^_]+$", min_length=8, max_length=16),
                   db: Session = Depends(get_db)):
    
    try: 
        validated_email = validate_email(email, check_deliverability=True)
    except: 
        raise HTTPException(status_code=404, detail="Sent email is invalid!")
    
    existing_user = db.query(User).filter(User.email == email).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    if password != repeatPassword:
        raise HTTPException(status_code=404, detail="Password did not match repeated password, try typing again.")

    db_user = create_db_user(UserIn(email=email, name="default", password=password))
    new_user = user_to_db(db_user)

    db.add(new_user)
    db.commit()

    return RedirectResponse("/users/login")
        
@router.post("/login",
             tags=["authorization"])
async def login(email: EmailStr = Body(embed=True, pattern="^[a-zA-Z0-9-_.]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"),
                password: str = Body(embed=True, pattern="^[a-zA-Z0-9-_.]+$", min_length=8, max_length=16),
                db: Session = Depends(get_db)):
    user = db.query(User).filter(User.email == email).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User with such email wasn't registered yet. Register before logging in.")
    
    if not bcrypt.verify(password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    
    return {"message": f"logged in as {email}"}

    