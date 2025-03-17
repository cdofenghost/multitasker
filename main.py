from fastapi import FastAPI
from fastapi.responses import FileResponse
from .routers import users
from .database import get_engine, Base
from .models import user, task, project, subtask, category

app = FastAPI()

@app.on_event("startup")
def startup():
    print("started up")
    print(Base.metadata.tables)
    Base.metadata.create_all(bind=get_engine())

app.include_router(users.router)

@app.get("/register")
async def register():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/public/register.html")

@app.get("/login")
async def login():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/public/login.html")