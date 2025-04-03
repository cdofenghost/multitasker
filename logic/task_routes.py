from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .tokens import get_current_user
from .tasks import TaskRepository, TaskService
from ..database import get_db
from ..schemas.task import TaskCreateSchema, TaskUpdateSchema
from .users import UserRepository, UserService

router = APIRouter(prefix="/task", tags=["Tasks"])


def get_task_repository(db: Session = Depends(get_db)):
    return TaskRepository(db)

def get_task_service(user_repository: TaskRepository = Depends(get_task_repository)):
    return TaskService(user_repository)

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
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

@router.get("/allocated")
async def get_allocated_tasks(project_id: int,
                            service: ServiceDependency,
                            user: UserDependency):
    user_id = user["user_id"]
    tasks = service.get_allocated_tasks(user_id)

    if tasks is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение задач проекта.")

    return tasks


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

@router.put("/performer")
async def set_task_performer(task_id: int,
                             performer_email: str,
                             service: ServiceDependency,
                             user: UserDependency,
                             user_service: UserServiceDependency):
    performer = user_service.get_user_by_email(performer_email)

    if performer is None:
        raise HTTPException(status_code=404, detail="Пользователь с таким e-mail не зарегистрирован!")
        
    user_id = user["user_id"]
    is_user_owner = service.check_task_ownership(user_id, task_id)

    if not is_user_owner:
        raise HTTPException(status_code=403, detail="Вы не являетесь автором этой задачи.")
    
    task = service.set_performer(task_id, performer.id)

    if type(task) is dict:
        raise HTTPException(status_code=task['error_code'], detail=task['detail'])
    
    return {"message": f"Пользователь {performer_email} теперь является исполнителем задачи",
            "name": task.name,
            "description": task.description,
            "author_id": task.author_id,
            "performer_id": task.performer_id,
            "project_id": task.project_id,
            "priority": task.priority,}