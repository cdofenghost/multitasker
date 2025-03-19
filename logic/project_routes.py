from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .projects import ProjectRepository, ProjectService
from ..database import get_db
from ..schemas.project import ProjectCreateSchema, ProjectUpdateSchema

router = APIRouter(prefix="/projects")

# user_codes = {
#     # "user_email": "code"
# }

def get_project_repository(db: Session = Depends(get_db)):
    return ProjectRepository(db)

def get_project_service(user_repository: ProjectRepository = Depends(get_project_repository)):
    return ProjectService(user_repository)


@router.post("/add",
             tags=["Projects"])
async def add_project(category_id: int, 
                      project_data: ProjectCreateSchema, 
                      service: ProjectService = Depends(get_project_service)):
    project = service.add_project(project_data)
    
    return {"category_id": project.category_id, 
            "name": project.name,
            "description": project.description,
            "icon": project.icon,}


@router.put("/update",
             tags=["Projects"])
async def update_project(project_id: int, project_data: ProjectUpdateSchema, service: ProjectService = Depends(get_project_service)):
    project = service.update_project(project_id, project_data)

    if project is None:
        raise HTTPException(detail="ашибка абна вления я")
    
    return {"category_id": project.category_id, 
            "name": project.name,
            "description": project.description,
            "icon": project.icon,}


@router.delete("/delete",
             tags=["Projects"])
async def delete_project(project_id: int, service: ProjectService = Depends(get_project_service)):
    project = service.remove_project(project_id)

    if project is None:
        raise HTTPException(detail="ашибка абна вления я")
    
    return {"category_id": project.category_id, 
            "name": project.name,
            "description": project.description,
            "icon": project.icon,}
