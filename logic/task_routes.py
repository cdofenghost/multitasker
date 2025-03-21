from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .tokens import get_current_user
from .tasks import TaskRepository, TaskService
from ..database import get_db
from ..schemas.task import TaskCreateSchema, TaskUpdateSchema

router = APIRouter(prefix="/task", tags=["Tasks"])


def get_task_repository(db: Session = Depends(get_db)):
    return TaskRepository(db)

def get_task_service(user_repository: TaskRepository = Depends(get_task_repository)):
    return TaskService(user_repository)

ServiceDependency = Annotated[TaskService, Depends(get_task_service)]
UserDependency = Annotated[dict, Depends(get_current_user)]


@router.post("/")
async def add_task(project_id: int,
                   task_data: TaskCreateSchema, 
                   service: ServiceDependency,
                   user: UserDependency):
    user_id = user["user_id"]
    task = service.add_task(user_id, project_id, task_data)

    if task is None:
        raise HTTPException(status_code=403, detail=" о шибка таск не дабавлен")
    
    return {"name": task.name,
            "description": task.description,
            "author_id": task.author_id,
            "performer_id": task.performer_id,
            "project_id": task.project_id,
            "priority": task.priority,}

@router.get("/all")
async def get_project_tasks(project_id: int,
                            service: ServiceDependency,
                            user: UserDependency):
    user_id = user["user_id"]
    projects = service.get_project_tasks(user_id, project_id)

    if projects is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение задач проекта.")

    return projects

@router.put("/")
async def update_task(task_id: int, 
                      task_data: TaskUpdateSchema, 
                      service: ServiceDependency,
                      user: UserDependency):
    user_id = user["user_id"]
    task = service.update_task(user_id, task_id, task_data)

    if task is None:
        raise HTTPException(status_code=403, detail=" о шибка таск не абнавлен")
        
    return {"name": task.name,
            "description": task.description,
            "author_id": task.author_id,
            "performer_id": task.performer_id,
            "project_id": task.project_id,
            "priority": task.priority,}


@router.delete("/")
async def delete_task(task_id: int, 
                      service: ServiceDependency,
                      user: UserDependency):
    user_id = user["user_id"]
    task = service.remove_task(user_id, task_id)

    if task is None:
        raise HTTPException(status_code=403, detail=" о шибка таск не дабавлен")
    
    return {"name": task.name,
            "description": task.description,
            "author_id": task.author_id,
            "performer_id": task.performer_id,
            "project_id": task.project_id,
            "priority": task.priority,}
