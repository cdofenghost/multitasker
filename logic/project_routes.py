from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from typing import Annotated

from .users import UserSchema
from .projects import ProjectRepository, ProjectService
from ..database import get_db
from ..schemas.project import ProjectCreateSchema, ProjectUpdateSchema, ProjectSchema

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

@router.post("/{category_id}", response_model=ProjectSchema, status_code=201)
async def add_project(category_id: int, 
                      project_data: ProjectCreateSchema, 
                      service: ServiceDependency,
                      user: UserDependency):
    try:
        project = service.add_project(user.id, category_id, project_data)

    except PermissionError:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на добавление проекта.")
    
    return project


@router.get("/all/{category_id}", response_model=list[ProjectSchema])
async def get_category_projects(category_id: int,
                                service: ServiceDependency,
                                user: UserDependency):
    try:
        projects = service.get_projects_by_category_id(user.id, category_id)

    except PermissionError:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение проектов.")

    return projects

@router.get("/", response_model=ProjectSchema)
async def get_project(project_id: int,
                      service: ServiceDependency,
                      user: UserDependency):
    try:
        projects = service.get_project(user.id, project_id)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Проекта с таким ID не было найдено.")

    return projects

@router.get("/count-tasks", response_model=int)
async def get_tasks_count(project_id: int,
                          service: ServiceDependency,
                          user: UserDependency):
    projects = service.get_tasks_count(user.id, project_id)

    if projects is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение проекта.")

    return projects

@router.put("/", response_model=ProjectSchema)
async def update_project(project_id: int, 
                         project_data: ProjectUpdateSchema, 
                         service: ServiceDependency,
                         user: UserDependency):
    
    try:
        project = service.update_project(user.id, project_id, project_data)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Проекта с таким ID не было найдено.")
    
    except PermissionError:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на обновление проекта.")
    
    return project


@router.delete("/", status_code=204)
async def delete_project(project_id: int, 
                         service: ServiceDependency,
                         user: UserDependency):
    
    try:
        project = service.remove_project(user.id, project_id)

    except NoResultFound:
        raise HTTPException(status_code=404, detail="Проекта с таким ID не было найдено.")
    
    except PermissionError:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на добавление проекта.")
    
