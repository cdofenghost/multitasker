from fastapi import FastAPI
from fastapi.responses import FileResponse
from .logic import user_routes, category_routes, project_routes, task_routes, subtask_routes
from .database import get_engine, Base
from .models import user, task, project, subtask, category, restoring_codes

app = FastAPI(
    title="MultiTasker"
    #exception_handlers=
)

@app.on_event("startup")
def startup():
    print("started up")
    print(Base.metadata.tables)
    Base.metadata.create_all(bind=get_engine())

app.include_router(user_routes.router)
app.include_router(category_routes.router)
app.include_router(project_routes.router)
app.include_router(task_routes.router)
app.include_router(subtask_routes.router)

@app.get("/register")
async def register():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/public/register.html")

@app.get("/login")
async def login():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/public/login.html")