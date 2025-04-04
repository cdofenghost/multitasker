from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import Annotated

from .users import UserSchema
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

def get_project_service(project_repository: ProjectRepository = Depends(get_project_repository)):
    return ProjectService(project_repository)

ServiceDependency = Annotated[ProjectService, Depends(get_project_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]

@router.post("/")
async def add_project(category_id: int, 
                      project_data: ProjectCreateSchema, 
                      service: ServiceDependency,
                      user: UserDependency):
    project = service.add_project(user.id, category_id, project_data)

    if project is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на добавление проекта.")
    
    return {"category_id": project.category_id, 
            "name": project.name,
            "description": project.description,
            "icon": project.icon,}


@router.get("/all")
async def get_category_projects(category_id: int,
                                service: ServiceDependency,
                                user: UserDependency):
    projects = service.get_projects_by_category_id(user.id, category_id)

    if projects is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение проектов.")

    return projects


@router.put("/")
async def update_project(project_id: int, 
                         project_data: ProjectUpdateSchema, 
                         service: ServiceDependency,
                         user: UserDependency):
    
    project = service.update_project(user.id, project_id, project_data)

    if project is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на обновление проекта.")
    
    return {"category_id": project.category_id, 
            "name": project.name,
            "description": project.description,
            "icon": project.icon,}


@router.delete("/")
async def delete_project(project_id: int, 
                         service: ServiceDependency,
                         user: UserDependency):
    
    project = service.remove_project(user.id, project_id)

    if project is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на добавление проекта.")
    
    return {"category_id": project.category_id, 
            "name": project.name,
            "description": project.description,
            "icon": project.icon,}
