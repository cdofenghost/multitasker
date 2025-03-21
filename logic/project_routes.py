from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .projects import ProjectRepository, ProjectService
from ..database import get_db
from ..schemas.project import ProjectCreateSchema, ProjectUpdateSchema

from .tokens import get_current_user

router = APIRouter(prefix="/project",
                   tags=["Projects"])

# user_codes = {
#     # "user_email": "code"
# }

def get_project_repository(db: Session = Depends(get_db)):
    return ProjectRepository(db)

def get_project_service(user_repository: ProjectRepository = Depends(get_project_repository)):
    return ProjectService(user_repository)


@router.post("/")
async def add_project(category_id: int, 
                      project_data: ProjectCreateSchema, 
                      service: ProjectService = Depends(get_project_service),
                      user: dict = Depends(get_current_user)):
    user_id = user["user_id"]
    project = service.add_project(user_id, category_id, project_data)

    if project is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на добавление проекта.")
    
    return {"category_id": project.category_id, 
            "name": project.name,
            "description": project.description,
            "icon": project.icon,}


@router.get("/all")
async def get_category_projects(category_id: int,
                                service: ProjectService = Depends(get_project_service),
                                user: dict = Depends(get_current_user)):
    user_id = user["user_id"]
    projects = service.get_projects_by_category_id(user_id, category_id)

    if projects is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение проектов.")

    return projects


@router.put("/")
async def update_project(project_id: int, 
                         project_data: ProjectUpdateSchema, 
                         service: ProjectService = Depends(get_project_service),
                         user: dict = Depends(get_current_user)):
    
    user_id = user["user_id"]
    project = service.update_project(user_id, project_id, project_data)

    if project is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на обновление проекта.")
    
    return {"category_id": project.category_id, 
            "name": project.name,
            "description": project.description,
            "icon": project.icon,}


@router.delete("/")
async def delete_project(project_id: int, 
                         service: ProjectService = Depends(get_project_service),
                         user: dict = Depends(get_current_user)):
    
    user_id = user["user_id"]
    project = service.remove_project(user_id, project_id)

    if project is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на добавление проекта.")
    
    return {"category_id": project.category_id, 
            "name": project.name,
            "description": project.description,
            "icon": project.icon,}
