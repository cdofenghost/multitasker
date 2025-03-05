from fastapi import Depends, FastAPI, Query
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from .routers import users
from .database import get_engine
from .models.user import Base, User

app = FastAPI()

@app.on_event("startup")
def startup():
    print("started up")
    Base.metadata.create_all(bind=get_engine())

app.include_router(users.router)

@app.get("/register")
def register():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/public/register.html")

@app.get("/login")
def login():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/public/login.html")