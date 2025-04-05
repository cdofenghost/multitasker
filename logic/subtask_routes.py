from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .users import UserRepository, UserService, UserSchema

from .tokens import get_current_user

from .subtasks import SubtaskRepository, SubtaskService
from ..database import get_db
from ..schemas.subtask import SubtaskCreateSchema, SubtaskUpdateSchema

router = APIRouter(prefix="/subtask", tags=["Subtasks"])


def get_task_repository(db: Session = Depends(get_db)):
    return SubtaskRepository(db)

def get_task_service(user_repository: SubtaskRepository = Depends(get_task_repository)):
    return SubtaskService(user_repository)

def get_user_repository(db: Session = Depends(get_db)):
    return UserRepository(db)

def get_user_service(user_repository: UserRepository = Depends(get_user_repository)):
    return UserService(user_repository)

UserServiceDependency = Annotated[UserService, Depends(get_user_service)]
ServiceDependency = Annotated[SubtaskService, Depends(get_task_service)]
UserDependency = Annotated[UserSchema, Depends(get_current_user)]


@router.post("/")
async def add_subtask(task_id: int,
                      task_data: SubtaskCreateSchema, 
                      service: ServiceDependency,
                      user: UserDependency):
    subtask = service.add_subtask(user.id, task_id, task_data)

    if subtask is None:
        raise HTTPException(detail=" о шибка таск не дабавлен")
    
    return {"name": subtask.name,
            "description": subtask.description,
            "author_id": subtask.author_id,
            "performer_id": subtask.performer_id,
            "task_id": subtask.task_id,
            "priority": subtask.priority,}


@router.put("/")
async def update_subtask(subtask_id: int, 
                         task_data: SubtaskUpdateSchema, 
                         service: ServiceDependency,
                         user: UserDependency):
    subtask = service.update_subtask(user.id, subtask_id, task_data)

    if subtask is None:
        raise HTTPException(detail=" о шибка таск не дабавлен")
    
    return {"name": subtask.name,
            "description": subtask.description,
            "author_id": subtask.author_id,
            "performer_id": subtask.performer_id,
            "task_id": subtask.task_id,
            "priority": subtask.priority,}


@router.delete("/")
async def delete_subtask(subtask_id: int, 
                         service: ServiceDependency,
                         user: UserDependency):
    subtask = service.remove_subtask(user.id, subtask_id)

    if subtask is None:
        raise HTTPException(detail=" о шибка таск не дабавлен")
    
    return {"name": subtask.name,
            "description": subtask.description,
            "author_id": subtask.author_id,
            "performer_id": subtask.performer_id,
            "task_id": subtask.task_id,
            "priority": subtask.priority,}

@router.get("/all")
async def get_task_subtasks(task_id: int,
                            service: ServiceDependency,
                            user: UserDependency):
    projects = service.get_task_subtasks(user.id, task_id)

    if projects is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение задач проекта.")

    return projects

@router.get("/allocated")
async def get_allocated_subtasks(project_id: int,
                              service: ServiceDependency,
                              user: UserDependency):
    tasks = service.get_allocated_subtasks(user.id)

    if tasks is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение задач проекта.")

    return tasks

@router.put("/performer")
async def set_subtask_performer(task_id: int,
                                performer_email: str,
                                service: ServiceDependency,
                                user: UserDependency,
                                user_service: UserServiceDependency):
    performer = user_service.get_user_by_email(performer_email)

    if performer is None:
        raise HTTPException(status_code=404, detail="Пользователь с таким e-mail не зарегистрирован!")
        
    is_user_owner = service.check_task_ownership(user.id, task_id)

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