from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .subtasks import SubtaskRepository, SubtaskService
from ..database import get_db
from ..schemas.subtask import SubtaskCreateSchema, SubtaskUpdateSchema

router = APIRouter(prefix="/subtask")


def get_task_repository(db: Session = Depends(get_db)):
    return SubtaskRepository(db)

def get_task_service(user_repository: SubtaskRepository = Depends(get_task_repository)):
    return SubtaskService(user_repository)


@router.post("/",
             tags=["Subtasks"])
async def add_subtask(task_data: SubtaskCreateSchema, service: SubtaskService = Depends(get_task_service)):
    subtask = service.add_subtask(task_data)

    if subtask is None:
        raise HTTPException(detail=" о шибка таск не дабавлен")
    
    return {"name": subtask.name,
            "description": subtask.description,
            "author_id": subtask.author_id,
            "performer_id": subtask.performer_id,
            "task_id": subtask.task_id,
            "priority": subtask.priority,}


@router.put("/",
             tags=["Subtasks"])
async def update_subtask(subtask_id: int, task_data: SubtaskUpdateSchema, service: SubtaskService = Depends(get_task_service)):
    subtask = service.add_subtask(subtask_id, task_data)

    if subtask is None:
        raise HTTPException(detail=" о шибка таск не дабавлен")
    
    return {"name": subtask.name,
            "description": subtask.description,
            "author_id": subtask.author_id,
            "performer_id": subtask.performer_id,
            "task_id": subtask.task_id,
            "priority": subtask.priority,}


@router.delete("/",
             tags=["Subtasks"])
async def delete_subtask(subtask_id: int, service: SubtaskService = Depends(get_task_service)):
    subtask = service.add_subtask(subtask_id)

    if subtask is None:
        raise HTTPException(detail=" о шибка таск не дабавлен")
    
    return {"name": subtask.name,
            "description": subtask.description,
            "author_id": subtask.author_id,
            "performer_id": subtask.performer_id,
            "task_id": subtask.task_id,
            "priority": subtask.priority,}
