from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from .tasks import TaskRepository, TaskService
from ..database import get_db
from ..schemas.task import TaskCreateSchema, TaskUpdateSchema

router = APIRouter(prefix="/tasks")


def get_task_repository(db: Session = Depends(get_db)):
    return TaskRepository(db)

def get_task_service(user_repository: TaskRepository = Depends(get_task_repository)):
    return TaskService(user_repository)


@router.post("/add",
             tags=["Tasks"])
async def add_task(task_data: TaskCreateSchema, 
                   service: TaskService = Depends(get_task_service)):
    task = service.add_task(task_data)

    if task is None:
        raise HTTPException(detail=" о шибка таск не дабавлен")
    
    return {"name": task.name,
            "description": task.description,
            "author_id": task.author_id,
            "performer_id": task.performer_id,
            "project_id": task.project_id,
            "priority": task.priority,}

@router.put("/update",
             tags=["Tasks"])
async def update_task(task_id: int, task_data: TaskUpdateSchema, service: TaskService = Depends(get_task_service)):
    task = service.update_task(task_id, task_data)

    if task is None:
        raise HTTPException(detail=" о шибка таск не абнавлен")
        
    return {"name": task.name,
            "description": task.description,
            "author_id": task.author_id,
            "performer_id": task.performer_id,
            "project_id": task.project_id,
            "priority": task.priority,}


@router.delete("/delete",
             tags=["Tasks"])
async def delete_task(task_id: int, service: TaskService = Depends(get_task_service)):
    task = service.remove_task(task_id)

    if task is None:
        raise HTTPException(detail=" о шибка таск не дабавлен")
    
    return {"name": task.name,
            "description": task.description,
            "author_id": task.author_id,
            "performer_id": task.performer_id,
            "project_id": task.project_id,
            "priority": task.priority,}
