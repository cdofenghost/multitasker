from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from .logic import user_routes, category_routes, project_routes, task_routes, subtask_routes, profile_routes, attachment_routes
from .database import get_engine, Base
from .models import user, task, project, subtask, category, restoring_codes, attachment

app = FastAPI(
    title="MultiTasker",
    #exception_handlers=
)

@app.on_event("startup")
def startup():
    print("started up")
    print(Base.metadata.tables)
    Base.metadata.create_all(bind=get_engine())
    
app.mount("/static", StaticFiles(directory="C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/imgs"))

app.include_router(user_routes.router)
app.include_router(category_routes.router)
app.include_router(project_routes.router)
app.include_router(task_routes.router)
app.include_router(subtask_routes.router)
app.include_router(profile_routes.router)
app.include_router(attachment_routes.router)

@app.get("/app", tags=["App"])
async def start():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/app-start.html")

@app.get("/app/tasks", tags=["App"])
async def start():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/tasks-main.html")

@app.get("/app/restore-code", tags=["App"])
async def restore_code():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/restore-code.html")

@app.get("/app/restore-new-password", tags=["App"])
async def restore_new_password():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/restore-newpass.html")

@app.get("/app/restore", tags=["App"])
async def restore():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/restore.html")

@app.get("/app/register", tags=["App"])
async def register():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/register.html")

@app.get("/app/login", tags=["App"])
async def login():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/auth.html")

@app.get("/app/main", tags=["App"])
async def mystuff():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/main.html")

@app.get("/app/profile", tags=["App"])
async def profile():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/profile.html")

@app.get("/app/category/{id}", tags=["App"])
async def join_category(id: int):
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/category.html")

@app.get("/app/category/{id}/edit", tags=["App"])
async def edit_category(id: int):
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/category-edit.html")

@app.get("/app/category/{id}/add-project", tags=["App"])
async def add_project_to_category(id: int):
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/project-create.html")

@app.get("/app/add-category", tags=["App"])
async def add_category():
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/category-create.html")

@app.get("/app/project/{id}")
async def join_project(id: int):
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/project.html")

@app.get("/app/project/{id}/add-task")
async def join_project(id: int):
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/task-create.html")

@app.get("/app/project/{id}/edit")
async def join_project(id: int):
    return FileResponse("C:/Users/Konstantin Denisov/AppData/Local/Programs/Python/Python311/web/testapp/frontend/project-edit.html")