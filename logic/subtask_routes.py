from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .tokens import get_current_user

from .subtasks import SubtaskRepository, SubtaskService
from ..database import get_db
from ..schemas.subtask import SubtaskCreateSchema, SubtaskUpdateSchema

router = APIRouter(prefix="/subtask", tags=["Subtasks"])


def get_task_repository(db: Session = Depends(get_db)):
    return SubtaskRepository(db)

def get_task_service(user_repository: SubtaskRepository = Depends(get_task_repository)):
    return SubtaskService(user_repository)


ServiceDependency = Annotated[SubtaskService, Depends(get_task_service)]
UserDependency = Annotated[dict, Depends(get_current_user)]

@router.get("/all")
async def get_task_subtasks(task_id: int,
                            service: ServiceDependency,
                            user: UserDependency):
    user_id = user["user_id"]
    projects = service.get_task_subtasks(user_id, task_id)

    if projects is None:
        raise HTTPException(status_code=403, detail="Запрещено. Неправомерный запрос на получение задач проекта.")

    return projects

@router.post("/")
async def add_subtask(task_id: int,
                      task_data: SubtaskCreateSchema, 
                      service: ServiceDependency,
                      user: UserDependency):
    user_id = user["user_id"]
    subtask = service.add_subtask(user_id, task_id, task_data)

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
    user_id = user["user_id"]
    subtask = service.update_subtask(user_id, subtask_id, task_data)

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
    user_id = user["user_id"]
    subtask = service.remove_subtask(user_id, subtask_id)

    if subtask is None:
        raise HTTPException(detail=" о шибка таск не дабавлен")
    
    return {"name": subtask.name,
            "description": subtask.description,
            "author_id": subtask.author_id,
            "performer_id": subtask.performer_id,
            "task_id": subtask.task_id,
            "priority": subtask.priority,}
